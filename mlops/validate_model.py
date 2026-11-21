
# ============================================================
# SENTINEL MLOPS & GITOPS
# VALIDACIÓN AUTOMATIZADA DEL MODELO
# ============================================================

import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

MODEL_PATH = BASE_DIR / "backend" / "sentinel_pipeline.joblib"
METADATA_PATH = BASE_DIR / "backend" / "sentinel_metadata.json"
EXAMPLE_PATH = BASE_DIR / "tests" / "ejemplo_reclamacion.json"


def validar_modelo():

    # 1. Verificar archivos
    for archivo in [MODEL_PATH, METADATA_PATH, EXAMPLE_PATH]:
        if not archivo.is_file():
            raise FileNotFoundError(
                f"Archivo no encontrado: {archivo}"
            )

    # 2. Cargar metadatos
    with open(METADATA_PATH, encoding="utf-8") as archivo:
        metadata = json.load(archivo)

    variables = metadata["variables_entrada"]

    if len(variables) != 32:
        raise ValueError(
            "El modelo no tiene 32 variables declaradas."
        )

    # 3. Cargar reclamación
    with open(EXAMPLE_PATH, encoding="utf-8") as archivo:
        ejemplo = json.load(archivo)

    if "datos" not in ejemplo:
        raise ValueError(
            "No se encontró la clave 'datos'."
        )

    datos = ejemplo["datos"]

    if not isinstance(datos, dict):
        raise ValueError(
            "'datos' debe contener un objeto."
        )

    if set(datos) != set(variables):
        raise ValueError(
            "Las variables no coinciden con los metadatos."
        )

    X = pd.DataFrame(
        [[datos[col] for col in variables]],
        columns=variables
    )

    # 4. Cargar modelo
    modelo = joblib.load(MODEL_PATH)

    # 5. Verificar capacidad de predicción
    if not hasattr(modelo, "predict"):
        raise TypeError(
            "El modelo no implementa predict()."
        )

    prediccion = modelo.predict(X)

    if len(prediccion) != 1:
        raise ValueError(
            "El modelo no devolvió una predicción válida."
        )

    # 6. Verificar probabilidad, si está disponible
    if hasattr(modelo, "predict_proba"):
        probabilidades = np.asarray(
            modelo.predict_proba(X)
        )

        if probabilidades.shape[0] != 1:
            raise ValueError(
                "Número incorrecto de probabilidades."
            )

        if not np.isfinite(probabilidades).all():
            raise ValueError(
                "Se encontraron probabilidades no válidas."
            )

        if not np.allclose(
            probabilidades.sum(axis=1),
            1.0,
            atol=1e-6
        ):
            raise ValueError(
                "Las probabilidades no suman 1."
            )

    print("Validación del modelo satisfactoria.")
    print("Variables:", len(variables))
    print("Predicción generada:", prediccion[0])
    print("Modelo cargado correctamente.")

    return True


if __name__ == "__main__":
    validar_modelo()
