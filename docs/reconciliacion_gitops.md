
# Sentinel MLOps & GitOps
## Reconciliación automatizada del estado deseado

### 1. Objetivo

Implementar y validar un mecanismo de reconciliación
basado en prácticas GitOps que permita comparar el
estado deseado de la infraestructura con el estado
real del servicio Sentinel.

### 2. Arquitectura

La solución utiliza los siguientes componentes:

- Git y GitHub: control de versiones.
- GitHub Container Registry: imágenes versionadas.
- Docker Compose: gestión declarativa del despliegue.
- Python: lógica de reconciliación.
- FastAPI: servicio de inferencia.
- Smoke Tests: validación funcional.
- JSONL: registro de auditoría.

### 3. Estado deseado

El estado deseado se define mediante los archivos:

- releases/staging.json
- releases/production.json

Los manifiestos identifican el repositorio de la
imagen, el tag asociado al commit Git, el ambiente
y el estado de aprobación.

El ambiente production-simulated corresponde
exclusivamente a un laboratorio académico.

### 4. Mecanismo de reconciliación

El script mlops/reconcile_release.py realiza
las siguientes actividades:

1. Carga el manifiesto seleccionado.
2. Valida la referencia de la imagen.
3. Consulta el estado actual del contenedor.
4. Compara la imagen actual con la deseada.
5. Identifica el estado SYNCED u OUT_OF_SYNC.
6. Aplica el estado deseado cuando se autoriza.
7. Verifica la salud del backend.
8. Ejecuta los Smoke Tests.
9. Registra el resultado para auditoría.

### 5. Modos de ejecución

Modo de verificación:

    python mlops/reconcile_release.py --environment staging

Este modo permite detectar diferencias sin
modificar los contenedores.

Modo de reconciliación:

    python mlops/reconcile_release.py --environment staging --apply

Este modo autoriza la aplicación del estado
deseado cuando existe una diferencia.

### 6. Controles de seguridad

- Repositorio de imágenes autorizado.
- Validación del SHA completo del commit Git.
- Restricción al laboratorio simulado.
- Autorización explícita mediante --apply.
- Aislamiento mediante el proyecto Docker
  sentinel-release-lab.
- Verificación de salud posterior al despliegue.
- Registro de resultados para auditoría.

### 7. Prueba 1: detección de diferencias

Condición inicial:

- Estado deseado: imagen declarada en staging.json.
- Estado actual: sin despliegue.

Resultados:

- Estado de salud: absent.
- Estado detectado: OUT_OF_SYNC.
- Acción: check-only.
- Infraestructura sin modificaciones.

Resultado: satisfactorio.

### 8. Prueba 2: reconciliación automatizada

Se ejecutó el reconciliador con el parámetro --apply.

Resultados:

- Estado inicial: OUT_OF_SYNC.
- Aplicación de la imagen declarada.
- Backend: healthy.
- GET /health: PASS.
- GET /features: PASS.
- POST /predict: PASS.
- Estado final: SYNCED.
- Validación funcional: PASS.

Resultado: satisfactorio.

### 9. Prueba 3: idempotencia

Se ejecutó nuevamente el reconciliador utilizando
el mismo manifiesto de staging.

Resultados:

- Estado inicial: SYNCED.
- No se requirió recrear el contenedor.
- Identificador del contenedor sin cambios.
- GET /health: PASS.
- GET /features: PASS.
- POST /predict: PASS.
- Acción registrada: no-change.
- Resultado de auditoría: success.

Resultado: satisfactorio.

La prueba demuestra que el reconciliador evita
recreaciones innecesarias cuando la referencia
de imagen coincide y el contenedor está saludable.

### 10. Auditoría

Los resultados se almacenan en:

mlops/artifacts/reconciliation_audit.jsonl

El registro permite consultar:

- Fecha de ejecución en UTC.
- Ambiente seleccionado.
- Imagen deseada.
- Imagen anterior.
- Identificador de imagen.
- Estado de salud.
- Modo de ejecución.
- Acción realizada.
- Resultado final.
- Errores identificados durante la reconciliación.

### 11. Resultados consolidados

| Prueba | Resultado |
|---|---|
| Detección de diferencias | PASS |
| Aplicación del estado deseado | PASS |
| Healthcheck | PASS |
| Smoke Tests | 3 PASS |
| Idempotencia | PASS |
| Registro de auditoría | Generado |

### 12. Evidencias

- evidencias/42_gitops_deteccion_out_of_sync.png
- evidencias/43_gitops_reconciliacion_exitosa.png
- evidencias/44_gitops_idempotencia.png

### 13. Valor técnico y operativo

La reconciliación permite:

- Reducir intervenciones manuales.
- Mejorar la consistencia de los despliegues.
- Detectar diferencias entre estados.
- Evitar recreaciones innecesarias.
- Facilitar la trazabilidad de cambios.
- Fortalecer la reproducibilidad.
- Conservar registros para auditoría.

### 14. Limitaciones

La implementación corresponde a una reconciliación
automatizada bajo demanda en un laboratorio local.

No se ha implementado un controlador autónomo
de reconciliación continua.

La comparación se realiza mediante referencias
de imágenes y estado de salud.

No se verifica todavía el digest inmutable
de la imagen contra el manifiesto declarado.

El rollback fue validado mediante una simulación
manual controlada, no como recuperación automática
ante fallos.

Los registros JSONL son locales y no constituyen
un mecanismo de auditoría inmutable.

No existe autorización para producción real.

### 15. Conclusión

Sentinel MLOps & GitOps incorpora un mecanismo
funcional de reconciliación bajo demanda basado
en configuración declarativa.

Las pruebas realizadas permitieron demostrar
la detección de diferencias, la aplicación del
estado deseado y la idempotencia.

La implementación complementa el pipeline CI/CD,
el versionado de modelos e imágenes, la promoción
controlada, el rollback y los mecanismos de
observabilidad desarrollados previamente.

Estado: implementación validada en laboratorio.
