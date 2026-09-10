> **Ramas de los Experimentos en GitHub:**  
> El resultado y código generado de cada experimento se encuentra versionado de manera independiente en su propia rama dentro de este repositorio de GitHub:
> - **[`Experiment-A`](../../tree/Experiment-A)**: *Minimal Context*
> - **[`Experiment-B`](../../tree/Experiment-B)**: *Repository Context*
> - **[`Experiment-C`](../../tree/Experiment-C)**: *Engineered Context*

## Índice de Documentación

Todo el análisis y la documentación detallada del experimento se encuentran centralizados en el archivo [`results/experiment-report.md`](results/experiment-report.md):

* 📊 [Métricas de los experimentos](results/experiment-report.md#métricas-de-los-experimentos)
* 📈 [Tabla comparativas](results/experiment-report.md#tabla-comparativa-del-score)
* 📑 [Reporte final](results/experiment-report.md#reporte-final)
* ❓ [Preguntas](results/experiment-report.md#preguntas)
* 🎯 [Pregunta final](results/experiment-report.md#pregunta-final)


# Customer API
Small Python module for managing customer records.

## Structure
- `src/customer.py`: customer domain operations
- `src/repository.py`: in-memory customer repository
- `tests/`: automated tests
- `results/`: reportes y documentación de resultados

## Run tests
```bash
pytest
```