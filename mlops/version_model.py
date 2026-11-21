
# ============================================================
# SENTINEL MLOPS & GITOPS
# VERSIONADO Y TRAZABILIDAD DEL MODELO
# ============================================================

import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "backend" / "sentinel_pipeline.joblib"
METADATA_PATH = BASE_DIR / "backend" / "sentinel_metadata.json"

OUTPUT_DIR = BASE_DIR / "mlops" / "artifacts"
OUTPUT_PATH = OUTPUT_DIR / "model_manifest.json"


def calcular_sha256(ruta):
    """Calcula el hash SHA-256 de un archivo."""

    sha256 = hashlib.sha256()

    with open(ruta, "rb") as archivo:
        for bloque in iter(
            lambda: archivo.read(1024 * 1024),
            b""
        ):
            sha256.update(bloque)

    return sha256.hexdigest()


def obtener_commit():
    """Obtiene el commit asociado a la ejecución."""

    commit_ci = os.getenv("GITHUB_SHA")

    if commit_ci:
        return commit_ci

    resultado = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=BASE_DIR,
        capture_output=True,
        text=True,
        check=True
    )

    return resultado.stdout.strip()


def generar_manifiesto():

    if not MODEL_PATH.is_file():
        raise FileNotFoundError(MODEL_PATH)

    if not METADATA_PATH.is_file():
        raise FileNotFoundError(METADATA_PATH)

    with open(METADATA_PATH, encoding="utf-8") as archivo:
        metadata = json.load(archivo)

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    manifiesto = {
        "proyecto": "Sentinel MLOps & GitOps",
        "modelo": metadata.get("modelo"),
        "version_codigo": obtener_commit(),
        "sha256_modelo": calcular_sha256(MODEL_PATH),
        "sha256_metadatos": calcular_sha256(METADATA_PATH),
        "archivo_modelo": MODEL_PATH.name,
        "variables_entrada": len(
            metadata["variables_entrada"]
        ),
        "umbral_alerta": metadata.get("umbral_alerta"),
        "metricas_validacion": metadata.get(
            "metricas_validacion"
        ),
        "fecha_generacion_utc": datetime.now(
            timezone.utc
        ).isoformat(),
    }

    with open(
        OUTPUT_PATH,
        "w",
        encoding="utf-8"
    ) as archivo:
        json.dump(
            manifiesto,
            archivo,
            indent=2,
            ensure_ascii=False,
            default=str
        )

    print("Manifiesto generado correctamente.")
    print("Commit:", manifiesto["version_codigo"])
    print("SHA-256 modelo:", manifiesto["sha256_modelo"])
    print("Variables:", manifiesto["variables_entrada"])
    print("Archivo:", OUTPUT_PATH)


if __name__ == "__main__":
    generar_manifiesto()
