
# Sentinel MLOps & GitOps
## Promoción controlada y rollback de versiones

### 1. Objetivo

Demostrar la capacidad de desplegar una versión validada
del backend Sentinel y recuperar una versión anterior
mediante imágenes Docker almacenadas en GHCR.

### 2. Entorno

- Proyecto: Sentinel MLOps & GitOps
- Plataforma: Docker Desktop
- Orquestación: Docker Compose
- Registro: GitHub Container Registry
- Tipo de prueba: Laboratorio local
- Modelo: Random Forest

### 3. Control de versiones

Se utilizaron dos imágenes etiquetadas con
identificadores de commits Git diferentes.

| Versión | Manifiesto | Función |
|---|---|---|
| Reciente | releases/staging.json | Promoción |
| Anterior | releases/production.json | Rollback |

Ambas versiones contaban con ejecuciones satisfactorias
del pipeline CI/CD.

Los identificadores completos de las imágenes
se encuentran en los manifiestos JSON.

### 4. Validación de la versión anterior

Se desplegó inicialmente la imagen declarada
en releases/production.json.

Resultados:

- Backend: Up (healthy)
- GET /health: PASS
- GET /features: PASS
- POST /predict: PASS

Esta versión se estableció como línea base
para la simulación.

### 5. Promoción a staging

Se seleccionó la imagen declarada en
releases/staging.json.

Docker Compose recreó el backend utilizando
la versión reciente.

Resultados:

- Backend: Up (healthy)
- GET /health: PASS
- GET /features: PASS
- POST /predict: PASS
- Imagen desplegada: versión de staging confirmada

La promoción fue satisfactoria.

### 6. Rollback controlado

Se seleccionó nuevamente la versión anterior,
declarada en releases/production.json.

Se recreó el backend mediante Docker Compose.

Resultados:

- Backend: Up (healthy)
- GET /health: PASS
- GET /features: PASS
- POST /predict: PASS
- Imagen desplegada: versión anterior confirmada

El rollback fue satisfactorio.

### 7. Criterios de aceptación

Una versión se considera funcionalmente validada
en este laboratorio cuando:

1. La imagen puede descargarse desde GHCR.
2. El backend alcanza el estado healthy.
3. El endpoint /health responde correctamente.
4. El endpoint /features devuelve 32 variables.
5. El endpoint /predict genera una respuesta válida.
6. La imagen desplegada coincide con la declarada.

### 8. Evidencias

- docs/evidencias/34_rollback_version_anterior_validada.png
- docs/evidencias/35_promocion_staging_exitosa.png
- docs/evidencias/36_rollback_version_anterior_exitoso.png

### 9. Auditoría

La trazabilidad se fundamenta en:

- Commits de Git.
- Etiquetas de imágenes Docker.
- Digests SHA-256 de GHCR.
- Manifiestos declarativos JSON.
- Resultados de GitHub Actions.
- Registros de despliegue.
- Smoke Tests posteriores al despliegue.

### 10. Limitaciones

La simulación se realizó en un entorno educativo local.

La promoción y el rollback fueron ejecutados manualmente.

No se implementó reconciliación automática del estado
deseado ni rollback automático ante fallos.

La denominación production-simulated no representa
un despliegue productivo real.

### 11. Conclusión

La simulación permitió demostrar que Sentinel puede
alternar entre dos versiones previamente validadas
y recuperar una versión anterior conservando la
disponibilidad y funcionalidad del backend.

Este procedimiento fortalece la reproducibilidad,
la trazabilidad y la resiliencia operativa del proyecto.
