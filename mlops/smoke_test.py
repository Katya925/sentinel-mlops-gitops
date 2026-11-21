
# ============================================================
# SENTINEL MLOPS & GITOPS
# SMOKE TESTS POST-DESPLIEGUE
# ============================================================

import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]

BASE_URL = os.getenv(
    "SENTINEL_API_URL",
    "http://127.0.0.1:8000"
).rstrip("/")

EXAMPLE_PATH = (
    BASE_DIR / "tests" / "ejemplo_reclamacion.json"
)


def solicitar(ruta, payload=None):

    headers = {}

    if payload is not None:
        headers["Content-Type"] = "application/json"
        datos = json.dumps(payload).encode("utf-8")
        metodo = "POST"
    else:
        datos = None
        metodo = "GET"

    request = urllib.request.Request(
        BASE_URL + ruta,
        data=datos,
        headers=headers,
        method=metodo
    )

    with urllib.request.urlopen(
        request,
        timeout=15
    ) as response:

        contenido = json.loads(
            response.read().decode("utf-8")
        )

        if response.status != 200:
            raise RuntimeError(
                f"{ruta}: HTTP {response.status}"
            )

        return contenido


def esperar_backend():

    print("Esperando disponibilidad de Sentinel...")

    for intento in range(1, 31):

        try:
            respuesta = solicitar("/health")

            if (
                respuesta.get("status") == "ok"
                and respuesta.get("modelo_cargado") is True
            ):
                print("Backend disponible.")
                return

        except (
            urllib.error.URLError,
            TimeoutError,
            ValueError
        ):
            pass

        print(f"Intento {intento}/30")
        time.sleep(2)

    raise RuntimeError(
        "Backend no disponible tras 60 segundos."
    )


def ejecutar_smoke_tests():

    esperar_backend()

    # --------------------------------------------------------
    # PRUEBA 1 - HEALTH
    # --------------------------------------------------------

    health = solicitar("/health")

    assert health["status"] == "ok"
    assert health["modelo_cargado"] is True

    print("PASS - /health")

    # --------------------------------------------------------
    # PRUEBA 2 - FEATURES
    # --------------------------------------------------------

    features = solicitar("/features")

    assert features["total_variables"] == 32

    print("PASS - /features")

    # --------------------------------------------------------
    # PRUEBA 3 - PREDICCION
    # --------------------------------------------------------

    with open(
        EXAMPLE_PATH,
        encoding="utf-8"
    ) as archivo:
        reclamacion = json.load(archivo)

    resultado = solicitar(
        "/predict",
        reclamacion
    )

    if not isinstance(resultado, dict):
        raise TypeError(
            "La prediccion no devolvio un objeto JSON."
        )

    print("PASS - /predict")

    print(
        "\nSmoke tests completados satisfactoriamente."
    )


if __name__ == "__main__":
    ejecutar_smoke_tests()
