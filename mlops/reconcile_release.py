#===========================================================
# SENTINEL MLOPS & GITOPS
# RECONCILIACION DEL ESTADO DESEADO
# ==========================================================

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

PROJECT_NAME = "sentinel-release-lab"
COMPOSE_FILE = BASE_DIR / "compose.release.yaml"

AUDIT_DIR = BASE_DIR / "mlops" / "artifacts"

EXPECTED_IMAGE = "ghcr.io/katya925/sentinel-backend"


def ejecutar(comando, entorno=None):

    resultado = subprocess.run(
        comando,
        cwd=BASE_DIR,
        env=entorno,
        capture_output=True,
        text=True,
        check=True
    )

    return resultado.stdout.strip()


def cargar_manifiesto(ambiente):

    ruta = BASE_DIR / "releases" / f"{ambiente}.json"

    with open(ruta, encoding="utf-8") as archivo:
        manifiesto = json.load(archivo)

    imagen = manifiesto["image"]
    tag = manifiesto["tag"]

    if imagen != EXPECTED_IMAGE:
        raise ValueError("Repositorio de imagen no autorizado.")

    if not re.fullmatch(r"[a-f0-9]{40}", tag):
        raise ValueError("El tag debe ser un SHA Git completo.")

    if manifiesto.get("approved_for_production") is not False:
        raise ValueError("Solo se permite el laboratorio simulado.")

    return f"{imagen}:{tag}"


def obtener_estado_actual(entorno):

    contenedor = ejecutar(
        [
            "docker", "compose",
            "-p", PROJECT_NAME,
            "-f", str(COMPOSE_FILE),
            "ps", "-a", "-q", "backend"
        ],
        entorno
    )

    if not contenedor:
        return None, None, "absent"

    informacion = ejecutar(
        ["docker", "inspect", contenedor],
        entorno
    )

    datos = json.loads(informacion)[0]

    imagen = datos["Config"]["Image"]
    image_id = datos["Image"]

    estado = datos["State"]

    salud = estado.get("Health", {}).get(
        "Status", estado["Status"]
    )

    return imagen, image_id, salud


def guardar_auditoria(registro):

    AUDIT_DIR.mkdir(parents=True, exist_ok=True)

    ruta = AUDIT_DIR / "reconciliation_audit.jsonl"

    with open(ruta, "a", encoding="utf-8") as archivo:
        archivo.write(
            json.dumps(registro, ensure_ascii=False) + "\n"
        )

    print("Registro de auditoria:", ruta)


def reconciliar(ambiente, aplicar):

    deseada = cargar_manifiesto(ambiente)

    entorno = os.environ.copy()
    entorno["SENTINEL_IMAGE"] = deseada

    registro = {
        "fecha_utc": datetime.now(timezone.utc).isoformat(),
        "ambiente": ambiente,
        "imagen_deseada": deseada,
        "modo": "apply" if aplicar else "check"
    }

    try:

        actual, actual_id, salud = obtener_estado_actual(
            entorno
        )

        registro["imagen_anterior"] = actual
        registro["imagen_id_anterior"] = actual_id
        registro["salud_anterior"] = salud

        print("=== SENTINEL GITOPS ===")
        print("Ambiente:", ambiente)
        print("Imagen deseada:", deseada)
        print("Imagen actual:", actual or "Sin despliegue")
        print("Estado de salud:", salud)

        if actual == deseada and salud == "healthy":

            print("Estado: SYNCED")
            print("No se requiere recrear el contenedor.")

            registro["accion"] = "no-change"

        else:

            print("Estado: OUT_OF_SYNC")

            if not aplicar:

                print("Modo verificacion: sin cambios.")
                registro["accion"] = "check-only"
                registro["resultado"] = "out-of-sync"

                return

            print("Aplicando estado deseado...")

            subprocess.run(
                [
                    "docker", "compose",
                    "-p", PROJECT_NAME,
                    "-f", str(COMPOSE_FILE),
                    "up", "-d",
                    "--no-build",
                    "--force-recreate",
                    "--wait",
                    "--wait-timeout", "120"
                ],
                cwd=BASE_DIR,
                env=entorno,
                check=True
            )

            registro["accion"] = "reconcile"

        final, final_id, salud_final = obtener_estado_actual(
            entorno
        )

        if final != deseada or salud_final != "healthy":
            raise RuntimeError(
                "El estado final no coincide con el deseado"
            )

        print("Ejecutando Smoke Tests...")

        entorno["SENTINEL_API_URL"] = (
            "http://127.0.0.1:8000"
        )

        subprocess.run(
            [
                sys.executable,
                str(BASE_DIR / "mlops" / "smoke_test.py")
            ],
            cwd=BASE_DIR,
            env=entorno,
            check=True
        )

        registro["imagen_final"] = final
        registro["imagen_id_final"] = final_id
        registro["salud_final"] = salud_final
        registro["resultado"] = "success"

        print ("Estado final: SYNCED")
        print ("Validación funcional: PASS")

    except Exception as error:

        registro["resultado"] = "failed"
        registro["error"] = str(error)

        raise

    finally:

        guardar_auditoria(registro)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Reconciliador GitOps de Sentinel"
    )

    parser.add_argument(
        "--environment",
        choices=["staging", "production"],
        required=True
    )

    parser.add_argument(
        "--apply",
        action="store_true",
        help="Aplicar el estado deseado"
    )

    argumentos = parser.parse_args()

    reconciliar(
        argumentos.environment,
        argumentos.apply
    )