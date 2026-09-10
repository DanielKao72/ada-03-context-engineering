# Métricas de los Experimentos

| Métrica | Experimento A<br>*(Minimal Context)* | Experimento B<br>*(Repository Context)* | Experimento C<br>*(Engineered Context)* |
| :--- | :---: | :---: | :---: |
| **Tests passing** | 15/15 (agregó nuevos casos de prueba) | 4/4 | 4/4 |
| **Tests failing** | 0/15 | 0/4 | 0/4 |
| **Requisitos funcionales cumplidos** | 7/7 | 7/7 | 7/7 |
| **Archivos modificados / creados** | 5 (`customer.py`, `repository.py`, `pytest.ini`, `test_customer.py`, `test_repository.py`) | 2 (`customer.py`, `repository.py`) | 3 (`customer.py`, `repository.py`, `pytest.ini`) *(sin contar `SPEC.md`, `AGENTS.md`)* |
| **Cambios innecesarios** | 2 (Modificó los dos archivos de test) | 0 | 0 |
| **Iteraciones** | 7 iteraciones | 5 iteraciones | 6 iteraciones |
| **Intervenciones humanas** | 12 | 6 | 10 |
| **Problemas introducidos** | 1 (Modificó la suite de pruebas original) | 0 | 0 |
| **Tiempo** | Aproximadamente 3 minutos | Aproximadamente 2 minutos | Aproximadamente 1 min 30 s |
| **Score Context Engineering (/10)** | 8.3 | 9.7 | 10 |

---

# Tabla Comparativa del Score

| Criterio | Puntos Máx. | Experimento A<br>*(Minimal Context)* | Experimento B<br>*(Repository Context)* | Experimento C<br>*(Engineered Context)* |
| :--- | :---: | :---: | :---: | :---: |
| **1. Correctness** | 30 | 30 | 30 | 30 |
| **2. Requirements** | 20 | 20 | 20 | 20 |
| **3. Minimal Change** | 15 | 8 | 15 | 15 |
| **4. Maintainability** | 15 | 12 | 15 | 15 |
| **5. Security/Safety** | 10 | 6 | 10 | 10 |
| **6. Verification** | 10 | 7 | 7 | 10 |
| **Puntaje Total** | **100** | **83** | **97** | **100** |

---


# Reporte Final

## Hipótesis
 
Agregar un contexto a través de artefactos como lo son `AGENTS.md` y `SPEC.md` para especificar la funcionalidad y el comportamiento incrementará la precisión de la implementación, reducirá las intervenciones humanas y el tiempo, y eliminará modificaciones innecesarias. De tal manera que superará al agente con un mínimo de contexto.

---

## Experimental Setup

* **Repositorio Inicial:** Módulo en Python para gestión de clientes (`Customer`) con persistencia en memoria (`CustomerRepository`) y pruebas con `pytest`.
* **Estructura Base:**
  ```text
  ada-03-context-engineering/
  ├── README.md
  ├── src/
  │   ├── customer.py
  │   └── repository.py
  └── tests/
      ├── test_customer.py
      └── test_repository.py
  ```
* **Línea Base (Commit `a0e0118`):** Estado inicial no funcional para la actualización de email (2 pruebas fallando por falta de lógica de normalización a minúsculas y validación de sintaxis).

---

## A — Minimal Context

### Prompt:
```text
Implement the customer email update functionality.

Inspect the repository first. Implement the necessary changes and run the tests.
```

### Resultados:
* **Estado de Tests:** 15 tests pasando (después de que el agente alteró y expandió los archivos de prueba).
* **Archivos Modificados:** 5 archivos (`src/customer.py`, `src/repository.py`, `pytest.ini`, `tests/test_customer.py`, `tests/test_repository.py`).
* **Calidad del Código:** Implementó validación con expresión regular `EMAIL_REGEX` y normalización a minúsculas (`.strip().lower()`).

### Intervención Humana:
* **12 intervenciones:** Autorizaciones requeridas en CLI para comandos de diagnóstico como `pytest`, `python -m pytest`, `git log -p -n 5` (algunas de ellas, más de una vez), creación de `pytest.ini` con PowerShell `Set-Content`, y aprobación de cambios en archivos de dominio, repositorio y tests.

### Score:
* **83 / 100**
* Penalizaciones por cambiar la suite de pruebas, así como no presentar suficiente evidencia de las pruebas aceptadas.

### Observaciones:
El agente exploró autónomamente el repositorio y diagnosticó el error inicial de recolección de `pytest`. Sin embargo, al no contar con límites, optó por reescribir los tests originales (`test_customer.py` y `test_repository.py`), cambió sintaxis de aserciones `try-except` por `pytest.raises` y añadió tests parametrizados con casos adicionales. Aunque la lógica fue correcta, modificar los tests que evalúan la tarea representa un grave riesgo en un entorno de desarrollo real.

---

## B — Repository Context

### Prompt:
```text
Implement the customer email update functionality.

Before making changes:
1. Inspect the repository.
2. Read README.md.
3. Inspect all relevant source files.
4. Inspect the tests.
5. Infer expected behavior from the code and tests.
6. Run tests before changing code.
7. Make the smallest necessary implementation.
8. Run tests again.
9. Explain which repository information influenced the implementation.
```

### Resultados:
* **Estado de Tests:** 4/4 tests originales pasando.
* **Archivos Modificados:** 2 archivos (`src/customer.py`, `src/repository.py`).
* **Calidad del Código:** Implementó `if "@" not in new_email: raise ValueError("invalid-email")` y `customer.email = new_email.lower()`. Delegó la actualización en `repository.py` con `return update_customer_email(customer, new_email, updated_by)`.

### Intervención Humana:
* **6 intervenciones:** Autorizaciones para `git log -p`, ejecución de `pytest`, y aplicación de los parches de código en `customer.py` y `repository.py`.

### Score:
* **97 / 100**
* Penalización menor por no mostrar suficiente evidencia de los test que fueron correctos.

### Observaciones:
El prompt estructurado por pasos guió al agente a intuir los requisitos a partir de los tests existentes y a respetar la política del menor cambio posible (*Minimal Change*). El agente no modificó ningún archivo de test. No obstante, al depender exclusivamente de lo que se encuentrre en el código, su validación de correo electrónico se limitó a verificar la presencia del carácter `"@"`, ya que el test original solo evaluaba `"invalid"`.

---

## C — Engineered Context

### Prompt:
```text
Implement the customer email update functionality.

Follow SPEC.md and AGENTS.md.
Inspect the repository first, run tests before and after changes, and explain your verification.
```

Adicionalmente, se agregaron los siguientes archivos:
* **`SPEC.md`:** Documento formal con objetivo, 7 requerimientos funcionales numerados y criterios de aceptación (formato minúsculas, sintaxis válida, preservación de ID y auditoría, manejo de errores `invalid-email` y `customer-not-found`).
* **`AGENTS.md`:** Guía operativa con directivas de no modificación de tests, principio de cambio mínimo y protocolo de validación pre y post ejecución.

### Resultados:
* **Estado de Tests:** 4/4 tests originales pasando.
* **Archivos Modificados:** 3 archivos (`src/customer.py`, `src/repository.py`, `pytest.ini` para compatibilidad de rutas).
* **Calidad del Código:** Validación sintáctica completa con `EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s\.]+(?:\.[^@\s\.]+)+$")`, validación de tipo `isinstance(new_email, str)`, normalización `.lower()`, actualización estricta de `updated_by` y preservación de inmutabilidad de `customer_id` y `created_by`.

### Intervención Humana:
* **10 intervenciones:** Aprobaciones para ejecutar comandos como `git log`, parches en `customer.py`/`repository.py` y creación de `pytest.ini`.

### Score:
* **100 / 100**

### Observaciones:
El agente leyó y aplicó inmediatamente los límites establecidos en `AGENTS.md` y `SPEC.md`. Ejecutó el ciclo completo de pre-validación (identificando los 2 tests fallidos), aplicó una solución robusta y limpia sin tocar la suite de pruebas, y presentó un reporte final estructurado demostrando el cumplimiento de los criterios de aceptación.

---

## Comparación

| Criterio | Puntos Máx. | Experimento A<br>*(Minimal Context)* | Experimento B<br>*(Repository Context)* | Experimento C<br>*(Engineered Context)* |
| :--- | :---: | :---: | :---: | :---: |
| **1. Correctness** | 30 | 30 | 30 | 30 |
| **2. Requirements** | 20 | 20 | 20 | 20 |
| **3. Minimal Change** | 15 | 8 | 15 | 15 |
| **4. Maintainability** | 15 | 12 | 15 | 15 |
| **5. Security/Safety** | 10 | 6 | 10 | 10 |
| **6. Verification** | 10 | 7 | 7 | 10 |
| **Puntaje Total** | **100** | **83** | **97** | **100** |

---

## Análisis de Errores

1. **Error de Alcance e Invasión de Tests en Experimento A:**
   Al no tener una restricción de qué archivos modificar, el modelo asumió un rol de "desarrollador libre" que refactorizó el marco de pruebas. En entornos de integración continua (CI/CD), que un agente modifique los tests evaluadores puede llegar a eliminar la objetividad de la verificación.
2. **Error de Inferencia Insuficiente en Experimento B:**
   En el Experimento B, el agente dependió de los casos de prueba para deducir las reglas de negocio. Dado que `tests/test_customer.py` únicamente contenía `update_customer_email(customer, "invalid", "agent")`, el modelo dedujo que cualquier cadena sin `"@"` era inválida, omitiendo validaciones de formato de dominio, caracteres especiales o puntos.
3. **Manejo del Error de Entorno (`PYTHONPATH` / `pytest`):**
   Tanto en A como en C, el agente resolvió de manera proactiva la configuración de `pytest.ini` (`pythonpath = .`), permitiendo ejecutar `pytest` de manera nativa sin requerir flags adicionales en la terminal.

---

## Análisis de la Calidad del Contexto

* **Contexto Mínimo (Experimento A):** Deja al modelo en un espacio de decisiones no acotado. Aunque los LLMs tienen alta capacidad de razonamiento, la falta de restricciones conduce a redundancia y errores.
* **Contexto en Prompt (Experimento B):** Proporcionar una lista de pasos detallada en el prompt mejora el orden. Sin embargo, es difícil de mantener, no escala a nivel de equipo y está abierto a omisiones funcionales si los archivos del repositorio no son suficientes.
* **Contexto Diseñado (Experimento C):** La separación de responsabilidades en dos archivos (`SPEC.md` para el **QUÉ** y `AGENTS.md` para el **CÓMO**) proporciona la señal más limpia y estructurada. El agente opera como un ejecutor disciplinado, eliminando la ambigüedad y garantizando calidad de software de nivel de producción.

---

## Conclusiones

1. **Context Engineering supera a Prompt Engineering:** Diseñar archivos de contexto versionados en el repositorio (`SPEC.md` y `AGENTS.md`) es superior a intentar escribir prompts cada vez más largos en el chat.
2. **Más contexto no siempre es mejor, pero un contexto estructurado sí:** Un exceso de instrucciones no estructuradas añade "ruido"; en cambio, especificaciones claras y restricciones explícitas (como *"Do not modify tests"*) previenen comportamientos destructivos.
3. **El rol del desarrollador evoluciona:** El ingeniero de software ya no escribe únicamente código línea por línea, sino que actúa como arquitecto del contexto, diseñando las especificaciones, las restricciones y los puntos de control de calidad que guían a los agentes autónomos.

---

## ¿Qué cambiaría?

1. **Mejoras a `AGENTS.md`:**
   * Añadir una regla para la resolución automática de configuración de herramientas (por ejemplo, autorizar la creación de `pytest.ini` si no existe).
   * Definir un formato estándar para el informe de cierre de la tarea (Markdown summary).

---

<a id="preguntas"></a>
## Respuestas a Preguntas de Análisis y Reflexión Final

### 1. ¿Cuál fue tu hipótesis?
Agregar un contexto a través de artefactos como lo son `AGENTS.md` y `SPEC.md` para especificar la funcionalidad y el comportamiento incrementará la precisión de la implementación, reducirá las intervenciones humanas y el tiempo, y eliminará modificaciones innecesarias. De tal manera que superará al agente con un mínimo de contexto.

### 2. ¿Cuál experimento produjo el mejor resultado y por qué?
El Experimento C (Engineered Context). Produjo un puntaje de 100/100, implementó una validación robusta, cumplió el 100% de los requisitos, no tocó la suite de pruebas y ejecutó un protocolo riguroso de pre y post verificación en el menor tiempo.

### 3. ¿Qué errores aparecieron en A y no en C?
En A apareció la modificación no autorizada de `tests/test_customer.py` y `tests/test_repository.py`. En C, las restricciones de `AGENTS.md` evitaron completamente este error.

### 4. ¿Qué información del repositorio fue más útil?
La definición de la clase `Customer` en `src/customer.py` y los tests existentes en `tests/`, los cuales evidenciaron los nombres exactos de atributos (`created_by`, `updated_by`), las excepciones esperadas (`ValueError("invalid-email")`, `ValueError("customer-not-found")`) y la estructura de retorno.

### 5. ¿Qué aportó `SPEC.md`?
Aportó la especificación formal de los requerimientos de negocio, desde la obligación de normalizar a minúsculas, validar sintácticamente el email, preservar inmutables el ID y creador, actualizar el actor de auditoría y los criterios de aceptación explícitos.

### 6. ¿Qué función tuvo `AGENTS.md`?
Estableció las reglas de comportamiento del agente (**CÓMO**), desde el orden de inspección antes de editar, regla del cambio mínimo seguro, prohibición de tocar tests sin autorización y obligación de verificar con `pytest` antes y después de codificar.

### 7. ¿Más contexto significa necesariamente mejor contexto?
No. Más contexto sin estructura añade "ruido" y puede provocar alucinaciones o confusiones. Lo más importante es la estructura, separación de responsabilidades y qué tan conciso es el contexto.

### 8. ¿Qué información fue redundante?
Instrucciones repetitivas en el prompt cuando ya existían archivos de contexto en el repositorio, o la reescritura de tests en A que duplicaba la validación que el framework de testing ya ejecutaba.

### 9. ¿Qué intervención humana fue necesaria?
Aprobaciones de ejecución de comandos en el CLI (`pytest`, comandos de shell) y confirmación de cambios de código propuestos por el agente.

### 10. ¿Qué cambiarías en `SPEC.md` y `AGENTS.md`?
En `AGENTS.md`, estandarizaría el manejo de archivos de configuración como `pytest.ini`.

### 11. ¿Qué aprendiste sobre la responsabilidad del desarrollador al usar agentes?
El desarrollador es el máximo responsable de la calidad, seguridad y arquitectura del software. El uso de agentes no elimina la necesidad de nuestra carrera, sino al contrario, exige que el desarrollador sea capaz de diseñar especificaciones claras, puntos de control de calidad estrictas y auditar críticamente el código generado.

---



# Pregunta Final

> **¿Por qué un desarrollador que utiliza agentes de código necesita aprender Context Engineering y no solamente mejores prompts?**  

Aprender únicamente *Prompt Engineering* limita el potencial de los agentes de IA. Las tareas tienden a ser difíciles de escalar, ya que se reducen a conversaciones aisladas que pueden perderse al reiniciar una sesión, en lugar de integrarse como agentes que forman parte del ciclo de vida del software.

Por otro lado, el *Context Engineering* permite diseñar una arquitectura de información persistente, versionable y colaborativa dentro del propio repositorio, mediante artefactos como `SPEC.md`, `AGENTS.md`, configuraciones de linters y suites de pruebas.

En este enfoque, los agentes no se limitan a responder instrucciones, sino que navegan estructuras complejas de archivos, utilizan herramientas, analizan dependencias y toman decisiones arquitectónicas. Sin un contexto diseñado formalmente y con límites claros, requisitos bien definidos y mecanismos de control de calidad, los agentes son más propensos a generar alucinaciones, interpretar incorrectamente los requerimientos o tomar decisiones inconsistentes con la arquitectura del sistema.

En este sentido, el *Context Engineering* transforma el rol del desarrollador, deja de ser un simple "redactor de prompts" para convertirse en un verdadero arquitecto de sistemas asistidos por IA, responsable de diseñar el entorno, las reglas y el contexto que permiten a los agentes trabajar de forma consistente, segura y escalable.

