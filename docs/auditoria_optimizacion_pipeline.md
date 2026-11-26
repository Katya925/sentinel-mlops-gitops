
# Sentinel MLOps & GitOps
## Auditoría y optimización del pipeline CI/CD

### 1. Objetivo

Evaluar el rendimiento del pipeline automatizado
de Sentinel MLOps & GitOps, identificar oportunidades
de optimización y documentar mejoras basadas en
mediciones reales.

### 2. Línea base de rendimiento

Se registraron las duraciones de una ejecución
satisfactoria de GitHub Actions.

| Trabajo | Duración |
|---|---:|
| Pruebas automatizadas | 39 s |
| Construcción Docker | 58 s |
| Despliegue y Smoke Tests | 35 s |
| Suma de duraciones | 132 s |

La suma representa el tiempo acumulado de los
trabajos, no necesariamente el tiempo transcurrido
total del workflow.

### 3. Análisis inicial

La construcción Docker presentó la mayor duración
individual, con 58 segundos.

Representa aproximadamente el 43.9% de la suma
de duraciones de los tres trabajos.

Se identifica como primera oportunidad de
optimización la reutilización de capas Docker
mediante mecanismos de caché.

### 4. Hipótesis de optimización

La incorporación de caché de capas Docker podría
reducir el tiempo de construcción en ejecuciones
posteriores cuando existan capas reutilizables.

La mejora deberá evaluarse mediante mediciones
antes y después del cambio.

### 5. Metodología de evaluación

1. Conservar la ejecución actual como línea base.
2. Implementar una optimización controlada.
3. Ejecutar nuevamente GitHub Actions.
4. Registrar las nuevas duraciones.
5. Calcular la variación porcentual.
6. Evaluar reproducibilidad y estabilidad.
7. Documentar resultados y limitaciones.

### 6. Estado

Línea base registrada.
Optimización concluida. Resultados documentados en los apartados siguientes.

### 7. Experimentación con Docker Buildx

Se incorporó Docker Buildx con almacenamiento de
caché de capas mediante GitHub Actions.

Inicialmente se utilizó la configuración mode=max.

Las dos ejecuciones realizadas presentaron tiempos
de construcción de 82 y 91 segundos, superiores
a los 58 segundos de la línea base.

Se identificaron mensajes de importación y
exportación de caché, pero no se observó evidencia
de reutilización efectiva de capas en la segunda
ejecución.

### 8. Revisión técnica del Dockerfile

Se revisó la estructura del Dockerfile del backend.

La instalación de dependencias se realiza antes
de copiar el código de la aplicación y el modelo,
lo que favorece la reutilización de capas.

No se identificó la necesidad de modificar el
Dockerfile durante este experimento.

### 9. Ajuste de la estrategia de caché

Se sustituyó mode=max por mode=min para limitar
la exportación a las capas de la imagen resultante.

Configuración seleccionada:

```yaml
cache-from: type=gha,scope=sentinel-backend
cache-to: type=gha,mode=min,scope=sentinel-backend
```

Se confirmó la reutilización de capas mediante
los mensajes CACHED en la primera ejecución
con mode=min.

### 10. Resultados experimentales

Todas las duraciones se expresan en segundos.

| Trabajo | Base | MAX 1 | MAX 2 | MIN 1 | MIN 2 |
|---|---:|---:|---:|---:|---:|
| Pruebas automatizadas | 39 | 35 | 43 | 36 | 34 |
| Construcción Docker | 58 | 82 | 91 | 16 | 25 |
| Despliegue y Smoke Tests | 35 | 29 | 28 | 24 | 28 |
| Total acumulado | 132 | 146 | 162 | 76 | 87 |

### 11. Indicadores de mejora

Se utilizó el promedio de las dos ejecuciones
con mode=min para evitar seleccionar únicamente
el resultado más favorable.

| Indicador | Base | Promedio MIN | Reducción |
|---|---:|---:|---:|
| Pruebas automatizadas | 39 s | 35 s | 10.26% |
| Construcción Docker | 58 s | 20.5 s | 64.66% |
| Despliegue y Smoke Tests | 35 s | 26 s | 25.71% |
| Tiempo acumulado | 132 s | 81.5 s | 38.26% |

Fórmula utilizada:

Reducción (%) = ((Base - Promedio) / Base) * 100

La reducción promedio acumulada fue de
50.5 segundos por ejecución.

### 12. Decisión técnica

Se decidió conservar Docker Buildx con mode=min.

La decisión se fundamenta en los resultados
observados y en la evidencia de reutilización
de capas Docker.

La configuración mode=max no presentó beneficios
de rendimiento en las ejecuciones evaluadas.

### 13. Valor operativo

La reducción del tiempo de construcción permite
acelerar el ciclo de integración y despliegue.

Los beneficios potenciales incluyen:

- Menor tiempo de espera durante las iteraciones.
- Retroalimentación técnica más rápida.
- Mayor eficiencia del proceso de CI/CD.
- Menor consumo potencial de recursos de ejecución.
- Mayor agilidad en la validación de versiones.

No se cuantificaron ahorros económicos reales.

### 14. Limitaciones del experimento

El número de ejecuciones evaluadas es reducido.

Los tiempos pueden verse afectados por:

- Variabilidad de los runners de GitHub Actions.
- Disponibilidad de capas previamente almacenadas.
- Condiciones de red.
- Publicación y descarga de imágenes desde GHCR.
- Sobrecarga de inicialización de Docker Buildx.

Los resultados representan mejoras observadas
en el laboratorio y no garantizan tiempos
equivalentes en todas las ejecuciones futuras.

La suma de duraciones de los trabajos no equivale
necesariamente al tiempo total del workflow.

### 15. Evidencias

- evidencias/37_auditoria_pipeline_baseline.png
- evidencias/38_docker_cache_primera_ejecucion.png
- evidencias/39_docker_cache_segunda_ejecucion.png
- evidencias/40_docker_cache_mode_min.png
- evidencias/40a_reutilizacion_capas_docker.png
- evidencias/41_docker_cache_mode_min_confirmacion.png

### 16. Conclusión

El proceso de optimización permitió identificar
una configuración inicialmente desfavorable,
analizar sus resultados y ajustar la estrategia.

Con mode=min se observó una reducción promedio
del 64.66% en el tiempo de construcción Docker
y del 38.26% en el tiempo acumulado del pipeline.

La decisión técnica se sustentó en mediciones
reales, experimentación y evidencias verificables.

Estado: experimento de optimización concluido.
