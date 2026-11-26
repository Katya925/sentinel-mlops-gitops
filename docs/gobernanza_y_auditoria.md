
# Sentinel MLOps & GitOps
## Gobernanza, auditoría e inteligencia artificial responsable

### 1. Objetivo

Establecer un marco de gobernanza técnica y operativa
para el sistema Sentinel de detección de fraude en
seguros de automóviles.

El marco busca garantizar trazabilidad, reproducibilidad,
seguridad, supervisión humana y control del ciclo de vida
del modelo de inteligencia artificial.

La solución corresponde a un prototipo académico y no
está autorizada para producción real.

### 2. Principios de gobernanza

La solución se fundamenta en los siguientes principios:

- Trazabilidad de las decisiones técnicas.
- Reproducibilidad de los procesos.
- Validación previa al despliegue.
- Seguridad desde el diseño.
- Principio de mínimo privilegio.
- Supervisión humana.
- Gestión preventiva de riesgos.
- Mejora continua basada en evidencias.

### 3. Gobernanza de datos

El proyecto utiliza un conjunto de datos histórico
de reclamaciones de seguros de automóviles.

Se conserva la separación entre entrenamiento,
validación y prueba mediante particiones estratificadas.

Controles implementados:

- Validación de las 32 variables de entrada.
- Identificación de variables faltantes.
- Identificación de variables adicionales.
- Validación de valores nulos.
- Verificación de la estructura JSON.
- Detección de Data Drift mediante Evidently.
- Seguimiento de experimentos mediante MLflow.

En la fase de observabilidad se excluyó PolicyNumber
del análisis refinado de drift por su naturaleza
de identificador.

Esta exclusión corresponde al análisis de drift
y no implica una modificación del modelo entrenado.

El escenario refinado de control no presentó
variables con drift.

El escenario simulado presentó drift en Age y Make.

La detección de drift no constituye por sí sola
evidencia de degradación del desempeño predictivo.

Controles pendientes:

- Validación exhaustiva de tipos y rangos.
- Evaluación de representatividad de los datos.
- Automatización periódica de análisis de drift.
- Evaluación de calidad de etiquetas.
- Análisis de posibles fugas de información.

### 4. Gobernanza del modelo

El modelo utilizado corresponde a Random Forest,
desarrollado durante la primera fase de Sentinel.

Controles implementados:

- Conservación del modelo entrenado.
- Metadatos asociados al modelo.
- Registro del umbral de alerta.
- Validación automatizada de carga e inferencia.
- Verificación de las variables de entrada.
- Validación de probabilidades.
- Identificación del artefacto mediante SHA-256.
- Asociación del manifiesto con el commit Git.
- Publicación del manifiesto en GitHub Actions.

El archivo model_manifest.json permite relacionar
la versión del código con la huella del modelo
y sus metadatos.

El hash SHA-256 permite verificar la identidad
del artefacto frente a una referencia conocida.

No constituye por sí mismo una firma digital
ni una garantía de procedencia confiable.

Controles pendientes:

- Registro formal de versiones en MLflow Model Registry.
- Evaluación comparativa de modelos candidatos.
- Automatización del reentrenamiento.
- Firma de artefactos.
- Validación independiente del modelo.

### 5. Gobernanza del código

Git y GitHub se utilizan como mecanismos de
control de versiones del proyecto.

Controles implementados:

- Historial de commits.
- Repositorio independiente.
- Configuración declarativa mediante YAML y JSON.
- Integración continua mediante GitHub Actions.
- Validación de sintaxis Python.
- Doce pruebas automatizadas de API.
- Validación automatizada de datos y modelo.

Los cambios publicados en la rama main activan
el pipeline automatizado.

Las Pull Requests pueden ejecutar pruebas y
construcciones sin publicar imágenes en GHCR.

Controles pendientes:

- Protección formal de la rama main.
- Revisión obligatoria de Pull Requests.
- Aprobación independiente de cambios.
- Análisis automatizado de vulnerabilidades.

### 6. Gobernanza del despliegue

El pipeline construye y publica imágenes Docker
en GitHub Container Registry.

Cada imagen se etiqueta con el identificador
completo del commit Git.

El despliegue automatizado descarga la imagen
publicada y ejecuta verificaciones funcionales.

Controles implementados:

- Construcción condicionada a pruebas exitosas.
- Versionado de imágenes Docker.
- Publicación automatizada en GHCR.
- Despliegue sin reconstrucción de la imagen.
- Healthcheck del backend.
- Smoke Tests posteriores al despliegue.
- Conservación de registros de ejecución.
- Limpieza del entorno temporal.
- Simulación de promoción y rollback.
- Reconciliación automatizada bajo demanda.
- Detección de diferencias entre estados.
- Validación de idempotencia.
- Registro de auditoría de reconciliaciones.


Los manifiestos staging.json y production.json
permiten declarar las versiones seleccionadas
para el laboratorio.

El entorno production-simulated no representa
una autorización para producción real.

Controles pendientes:

- Despliegue persistente.
- Aprobaciones independientes de promoción.
- Despliegue fijado mediante digest inmutable.
- Reconciliación automática del estado deseado.
- Rollback automático ante fallos.

### 7. Seguridad y gestión de accesos

Controles implementados:

- Exclusión de archivos .env mediante .gitignore.
- Exclusión de entornos virtuales y datos derivados.
- Uso del token temporal de GitHub Actions.
- Permisos de lectura como configuración general.
- Permiso packages: write limitado al trabajo
  responsable de publicar imágenes.
- Permiso packages: read para el despliegue.
- Publicación de imágenes limitada a push en main.
- Servicios locales vinculados a 127.0.0.1.

Los modelos serializados mediante Joblib deben
proceder exclusivamente de fuentes confiables.

No deben cargarse artefactos de origen desconocido.

Controles pendientes:

- Escaneo de vulnerabilidades de imágenes.
- Inventario de componentes de software (SBOM).
- Firma y verificación de imágenes.
- Gestión centralizada de secretos.
- Revisión periódica de permisos.

### 8. Monitorización y continuidad operativa

Se reutiliza la arquitectura desarrollada
en Sentinel Observability.

Componentes:

- Prometheus: recopilación de métricas y alertas.
- Grafana: visualización de indicadores.
- OpenTelemetry: instrumentación de trazas.
- Tempo: almacenamiento de trazas.
- Evidently: detección de Data Drift.
- MLflow: seguimiento de experimentos.
- Logs estructurados: diagnóstico operativo.

Indicadores operativos definidos:

| Indicador | Objetivo de laboratorio |
|---|---|
| Disponibilidad | >= 99% |
| Latencia p95 | <= 500 ms |
| Errores HTTP 5xx | < 1% |

Estos objetivos constituyen referencias técnicas.

No se ha demostrado su cumplimiento durante
un periodo mensual de operación productiva.

Se realizaron simulaciones de indisponibilidad
del backend e incremento de latencia durante
la fase de observabilidad.

En la fase MLOps se realizó una simulación
de promoción y rollback entre imágenes
versionadas previamente validadas.

### 9. Auditoría y trazabilidad

La auditoría se fundamenta en la asociación
de los siguientes elementos:

| Elemento | Mecanismo de trazabilidad |
|---|---|
| Código | Commit Git |
| Modelo | Hash SHA-256 |
| Metadatos | Hash SHA-256 |
| Imagen Docker | Tag Git y digest GHCR |
| Pruebas | Registros de GitHub Actions |
| Despliegue | Artefactos y logs |
| Versiones seleccionadas | Manifiestos JSON |
| Incidentes | Runbooks |
| Optimización | Mediciones y evidencias |

Los artefactos de GitHub Actions se conservan
durante el periodo configurado de retención.

Para una operación productiva sería necesario
definir políticas de conservación, acceso,
integridad y protección de registros.

### 10. Optimización basada en evidencias

Se evaluaron diferentes configuraciones de
caché de capas Docker mediante Buildx.

La configuración inicial mode=max presentó
resultados desfavorables.

Posteriormente se evaluó mode=min.

| Indicador | Base | Promedio optimizado |
|---|---:|---:|
| Construcción Docker | 58 s | 20.5 s |
| Tiempo acumulado | 132 s | 81.5 s |

Resultados observados:

- Reducción promedio de construcción: 64.66%.
- Reducción promedio acumulada: 38.26%.

Se confirmó la reutilización de capas Docker
mediante registros CACHED.

Los resultados se limitan a las ejecuciones
evaluadas y no garantizan el mismo rendimiento
en todas las ejecuciones futuras.

No se cuantificaron ahorros económicos reales.

### 11. Inteligencia artificial responsable

Sentinel es una herramienta de apoyo a la
identificación de reclamaciones sospechosas.

La predicción del modelo no constituye una
determinación definitiva de fraude.

Las alertas deben ser revisadas por personal
autorizado antes de adoptar decisiones que
puedan afectar a los asegurados.

Principios aplicados:

- Supervisión humana.
- Uso proporcional de las predicciones.
- Transparencia sobre las limitaciones.
- Prevención de decisiones adversas automáticas.
- Protección de la información.
- Evaluación continua de riesgos.

No se ha realizado una evaluación exhaustiva
de equidad entre grupos demográficos.

No se declara cumplimiento regulatorio
ni autorización para producción.

### 12. Matriz de riesgos

| Riesgo | Impacto potencial | Control |
|---|---|---|
| Data Drift | Degradación predictiva | Evidently |
| Datos inválidos | Inferencias incorrectas | Validación de esquema |
| Modelo alterado | Pérdida de integridad | SHA-256 |
| Error de código | Fallo funcional | Pytest y CI |
| Despliegue defectuoso | Indisponibilidad | Healthcheck y Smoke Tests |
| Versión incorrecta | Pérdida de trazabilidad | Tags y manifiestos |
| Latencia elevada | Degradación del servicio | Prometheus y alertas |
| Exposición de credenciales | Acceso no autorizado | Exclusiones y permisos |
| Falsos positivos | Afectación al asegurado | Revisión humana requerida |
| Sesgo algorítmico | Decisiones inequitativas | Evaluación pendiente |

Los controles reducen determinados riesgos,
pero no garantizan su eliminación.

### 13. Responsabilidades propuestas

| Rol | Responsabilidad |
|---|---|
| Data Scientist | Evaluación y calidad del modelo |
| ML Engineer | Pipeline y versionado |
| DevOps Engineer | Infraestructura y despliegue |
| Responsable de operación | Monitoreo e incidentes |
| Responsable de riesgos | Validación de controles |
| Analista de fraude | Revisión de alertas |
| Product Owner | Valor de negocio y prioridades |

Estos roles representan una propuesta de
segregación de responsabilidades para una
futura operación organizacional.

En el laboratorio académico las actividades
fueron realizadas como parte del proyecto.

### 14. Documentación relacionada

- arquitectura_observabilidad.md
- indicadores_slo.md
- alertas_y_automatizacion.md
- resultados_incidentes.md
- promocion_y_rollback.md
- auditoria_optimizacion_pipeline.md
- evidencias/

### 15. Conclusión

Sentinel MLOps & GitOps incorpora controles
de gobernanza a lo largo del ciclo de vida
de una solución de inteligencia artificial.

La integración continua, el versionado,
la monitorización, el despliegue controlado
y la auditoría fortalecen la reproducibilidad
y la resiliencia operativa.

La solución constituye una base tecnológica
para evolucionar hacia una operación MLOps
con mayores niveles de automatización,
seguridad y control.

El proyecto conserva su carácter académico
y requiere controles adicionales antes de
considerar un despliegue productivo real.

### 16. Actualización de controles GitOps

Se implementó y validó un mecanismo de
reconciliación automatizada bajo demanda
mediante el script:

mlops/reconcile_release.py

Los controles incorporados permiten:

- Consultar el estado deseado declarado en JSON.
- Detectar diferencias respecto al estado actual.
- Aplicar la versión declarada mediante autorización
  explícita con el parámetro --apply.
- Verificar la salud del servicio.
- Ejecutar Smoke Tests posteriores al despliegue.
- Evitar recreaciones innecesarias del contenedor.
- Registrar los resultados en formato JSONL.

Resultados de validación:

| Control | Resultado |
|---|---|
| Detección OUT_OF_SYNC | Satisfactorio |
| Reconciliación del estado deseado | Satisfactorio |
| Estado final SYNCED | Confirmado |
| Smoke Tests | 3 PASS |
| Idempotencia | Confirmada |
| Registro de auditoría | Generado |

Evidencias:

- evidencias/42_gitops_deteccion_out_of_sync.png
- evidencias/43_gitops_reconciliacion_exitosa.png
- evidencias/44_gitops_idempotencia.png

Documentación complementaria:

- reconciliacion_gitops.md

La reconciliación se ejecuta bajo demanda
en un entorno de laboratorio local.

Continúan pendientes la reconciliación autónoma
continua, la verificación mediante digests
inmutables y el rollback automático ante fallos.

La solución mantiene su carácter académico
y no está autorizada para producción real.
