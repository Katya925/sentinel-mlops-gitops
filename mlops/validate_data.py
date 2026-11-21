
# ============================================================
# SENTINEL MLOPS & GITOPS
# VALIDACIÓN AUTOMATIZADA DE DATOS
# ============================================================

import json
from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[1]

METADATA_PATH = BASE_DIR / "backend" / "sentinel_metadata.json"

EXAMPLE_PATH = BASE_DIR / "tests" / "ejemplo_reclamacion.json"


def validar_datos():

    # Cargar metadatos
    with open(METADATA_PATH, encoding="utf-8") as archivo:
        metadata = json.load(archivo)

    variables = metadata["variables_entrada"]

    # Cargar reclamación de ejemplo
    with open(EXAMPLE_PATH, encoding="utf-8") as archivo:
        reclamacion = json.load(archivo)

    # Extraer las variables del objeto "datos"        
    if "datos" not in reclamacion:
        raise ValueError(
            "El JSON no contiene la clave 'datos',"
        )
    
    reclamacion = reclamacion["datos"]

    if not isinstance(reclamacion,dict):
        raise ValueError(
            "La clave 'datos' debe contener un objeto JSON."
        )

    # Verificar variables faltantes y adicionales
    faltantes = set(variables) - set(reclamacion)
    adicionales = set(reclamacion) - set(variables)

    if faltantes:
        raise ValueError(
            f"Variables faltantes: {sorted(faltantes)}"
        )

    if adicionales:
        raise ValueError(
            f"Variables adicionales: {sorted(adicionales)}"
        )

    # Convertir a DataFrame respetando el orden del modelo
    df = pd.DataFrame(
        [[reclamacion[col] for col in variables]],
        columns=variables
    )

    # Verificar valores nulos
    if df.isnull().any().any():
        raise ValueError(
            "Se encontraron valores nulos en la reclamación."
        )

    # Verificar estructura
    if df.shape[1] != 32:
        raise ValueError(
            f"Se esperaban 32 variables; se encontraron {df.shape[1]}."
        )

    print("Validación de datos satisfactoria.")
    print("Registros:", df.shape[0])
    print("Variables:", df.shape[1])

    return True


if __name__ == "__main__":
    validar_datos()
