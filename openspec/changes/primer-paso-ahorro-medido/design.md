# Diseño: Primer paso con ahorro medido

## Contexto

- Frontend React + Vite; API Node.js + MongoDB. Muchas usuarias entran desde el celular con datos móviles limitados.
- Datos de facturas de Inés (luz):

| Periodo | Días | kWh | kWh/día | S/ por kWh |
|---|---|---|---|---|
| Enero | 31 | 1.840 | 59,4 | 0,78 |
| Febrero | 28 | 1.690 | 60,4 | 0,78 |
| Marzo | 31 | 1.910 | 61,6 | 0,81 |
| Abril | 30 | 1.760 | 58,7 | 0,81 |
| Mayo | 31 | 1.880 | 60,6 | 0,81 |
| Junio | 30 | 1.720 | 57,3 | 0,84 |

Promedio: **59,7 kWh/día**. Variación normal entre meses: desviación estándar ≈ 1,5 kWh/día (**≈ 2,6 %**).

## Dónde profundizo y dónde no

- **Profundizo**: medición del ahorro (decisión 3) y fallas/recálculo (decisión 4). Son lo que hoy engaña a Inés y lo que piden los aliados.
- **Suficiente**: recomendación con reglas (decisión 1) y privacidad (decisión 5).
- **Ligero**: tecnologías (decisión 6). La pieza construida es un diagrama de arquitectura.

---

## Decisión 1: La recomendación

### Postura

Un **motor de reglas con puntaje transparente**, en la API. Elige **una** ecoinnovación como primer paso y guarda el porqué.

Para Inés recomienda: **Hornear por tandas y apagar el horno entre ellas.**

### Cómo se calcula

1. **Filtros duros** (descartan):
   - Categoría distinta del objetivo de la persona (aquí: ENERGY).
   - `investment` que no cabe en su presupuesto. Equivalencia acordada con el equipo (supuesto): BAJA ≤ S/ 500, MEDIA ≤ S/ 3.000, ALTA > S/ 3.000. Como el catálogo solo guarda el nivel y no el monto, el filtro usa el **piso** del nivel: pasa si el presupuesto alcanza el monto mínimo del nivel (BAJA: S/ 0, MEDIA: S/ 501, ALTA: S/ 3.001). Ejemplo: con S/ 1.200, una MEDIA pasa el filtro y una ALTA no. La MEDIA que pasa igual queda penalizada en el factor de facilidad del puntaje.
   - `time` que no cabe en sus horas por semana. Supuesto: BAJA ≤ 2 h, MEDIA ≤ 5 h, ALTA > 5 h.
   - Ecoinnovaciones con un plan `delayed` o sin avance de más de 6 semanas **no se vuelven a recomendar como primer paso** (sí quedan visibles en el catálogo).
2. **Puntaje** (0 a 100), con pesos en un archivo de configuración versionado:

| Factor | Peso | Fuente |
|---|---|---|
| Ataca el equipo de mayor consumo que declaró | 35 | Perfil (nuevo campo `mainLoads`: horno, refrigeración, iluminación…) |
| Facilidad (complejidad e inversión) | 30 | Catálogo |
| Tasa de finalización en negocios similares (con n ≥ 3) | 20 | Agregados |
| Afinidad con el diagnóstico (secciones con puntaje bajo) | 15 | Autodiagnóstico |

3. **Desempate**: menor complejidad, luego menor inversión.

### Aplicado a Inés

| Ecoinnovación | ¿Pasa filtros? | Comentario |
|---|---|---|
| Hornear por tandas | ✅ | Ataca el horno, que es su mayor consumo. Inversión BAJA (S/ 0). Cabe en 4 h/semana. |
| Burletes y refrigeradoras | ✅ | Ataca la refrigeración. Más fácil. Queda **segundo paso**. |
| Iluminación LED | ✅ | La iluminación no es su mayor consumo. Puntaje bajo. |
| Aislamiento del horno | ❌ | Inversión ALTA y lleva 7 semanas trabada. |
| Calentador solar | ❌ | Inversión ALTA; no es luz. |

### Por qué tandas y no burletes (alternativa evaluada)

- **A favor de tandas**: el horno es la mayor parte de su factura; no requiere dinero; es un cambio de hábito que puede empezar mañana.
- **En contra**: complejidad MEDIA; solo 3 de 6 panaderías la completaron; solo 2 tienen facturas de antes y después.
- **Cómo lo mitigo**: el plan de tandas se divide en pasos de 1 semana (probar 1 día por semana → 3 días → toda la semana) y el siguiente paso sugerido es burletes, para tener una ganancia en paralelo si tandas se traba.

### Cómo se le explica a Inés

Plantilla fija, con datos del motor. Sin números que no podemos respaldar:

> **Tu primer paso: hornear por tandas.**
> Tu horno es lo que más gasta en tu factura. Hornear en tandas y apagarlo entre una y otra no cuesta nada y te toma unas 2 horas por semana organizarlo.
> Otras panaderías ya lo hicieron, pero todavía son pocas para decirte un porcentaje.
> Después de 2 facturas te diremos cuánto ahorraste tú.

### Negocio nuevo (sin facturas)

- El motor funciona igual: usa perfil, diagnóstico y catálogo.
- Le pide subir **2 facturas anteriores** antes de empezar, para tener línea base. Si no las tiene, la medición queda en «todavía no podemos saberlo» hasta tener datos.

### Cómo logro que los 4 lugares digan lo mismo

- Una sola colección `recommendations`: `{ businessId, ecoCardId, score, reasons[], rulesVersion, createdAt, status }`.
- El inicio, el catálogo, el diagnóstico por etapas y el correo de bienvenida **solo leen** la recomendación vigente. Ninguno calcula por su cuenta.
- Se recalcula cuando cambia el perfil, el diagnóstico, una factura o el estado de un plan.
- El catálogo puede seguir ordenando el resto, pero la tarjeta «Tu primer paso» siempre muestra la recomendación guardada.

### Alternativas descartadas

| Alternativa | Por qué no |
|---|---|
| Modelo de ranking o de aprendizaje automático | 23 panaderías y entre 1 y 11 casos. Aprendería ruido y no se puede explicar. |
| Que el modelo de lenguaje elija | No es reproducible, no se puede auditar y puede inventar ahorros. |
| Mostrar las 3 primeras | Inés ya eligió mal entre varias. Una sola recomendación con su porqué reduce la duda. |
| Recomendar aislamiento por su −18 % | 1 solo caso medido; inversión y complejidad ALTA; ya está trabada. |

---

## Decisión 2: Cuánta inteligencia artificial

| Parte | Técnica | Por qué |
|---|---|---|
| Elegir el primer paso | **Reglas con puntaje** | Pocos datos; debe ser explicable y auditable. |
| Medir el ahorro | **Modelo estadístico simple**: línea base con media y desviación estándar de kWh/día | Separa un cambio real del ruido normal entre meses. |
| Explicación al usuario | **Plantilla fija**; modelo de lenguaje opcional solo para reescribir el texto, nunca para poner cifras | Si la IA falla, la plantilla funciona igual. |
| Subtareas del plan | Proveedor de IA existente | Ya existe; con fallback a los pasos del catálogo. |

**Cuándo subir de nivel**: con más de ~30 casos medidos por ecoinnovación y sector, evaluar un modelo que estime el ahorro esperado. No antes.

---

## Decisión 3: Cómo se mide el ahorro

### Contra qué comparo

- **Línea base**: promedio de **kWh por día** de las facturas completas **antes** de `startedAt` del plan. Mínimo 2, ideal 3 o más.
- **Periodo de transición**: las facturas que se cruzan con el periodo de implementación (entre `startedAt` y `completedAt`) **no cuentan** ni como antes ni como después.
- **Después**: facturas completas posteriores a `completedAt`. Para cambios de hábito, como tandas, «completado» significa que lo aplica toda la semana.

### Correcciones

| Problema | Corrección |
|---|---|
| Meses con distinta cantidad de días (febrero) | Comparar **kWh por día**, nunca el total del mes. |
| La tarifa sube (+8 %) | El ahorro en soles = kWh/día ahorrados × días del periodo × **tarifa actual**. La subida de tarifa no se cuenta como gasto suyo ni como ahorro. |
| Temporada | Con menos de 12 meses no puedo corregirla: lo **digo** en la pantalla. Con 12 meses o más, comparo contra el mismo mes del año anterior. |

### Fórmulas

```
kwhDia(f)      = f.kwhConsumed / días(f)
base           = media(kwhDia de facturas antes)
sd             = desviación estándar de esas facturas
despues        = media(kwhDia de facturas después)
cambio%        = (despues - base) / base
umbral%        = max(3 %, 2 × sd / base)
ahorroSoles    = (base - despues) × díasDelPeriodo × tarifaActual
rangoSoles     = (base - despues ± sd) × díasDelPeriodo × tarifaActual
```

Con los datos de Inés: 2 × 1,5 / 59,7 ≈ **5,2 %**. Ese es su umbral: un cambio menor puede ser solo variación normal.

### Alternativa descartada: medir con un aparato

| Opción | Por qué no (por ahora) |
|---|---|
| Comprar un medidor inteligente | Cuesta dinero, y el objetivo es que el negocio ahorre. |
| Foto semanal del medidor que ya tiene | Gratis, pero le quita tiempo. Queda como opción futura. |

Con la factura mensual dividida entre sus días basta. La desventaja: el resultado tarda unos 2 meses en verse, y por eso existe el estado «todavía no podemos saberlo».

### Estados

| Estado | Cuándo | Qué ve Inés |
|---|---|---|
| `insufficient_data` | Menos de 2 facturas antes o menos de 2 facturas completas después | «Todavía no podemos saberlo. Sube tu factura de ___ y te contamos.» |
| `no_clear_change` | \|cambio%\| < umbral% | «Tu consumo no cambió más de lo normal. Puede ser muy pronto.» |
| `savings` | cambio% ≤ −umbral% | «Ahorraste entre S/ X y S/ Y este mes.» |
| `increase` | cambio% ≥ +umbral% | «Tu consumo subió. Revisemos juntas qué cambió.» |

Ejemplo de febrero con estas reglas: solo hay una factura antes (enero), así que el estado es **«todavía no podemos saberlo»** (`insufficient_data`). Aunque hubiera línea base, +1,7 % por día está por debajo del umbral de Inés (5,2 %), así que sería **sin cambio claro**. En ningún caso «ahorraste S/ 117».

### Qué ve Inés vs. qué ven los aliados

| Inés | Aliados |
|---|---|
| Un rango en soles por mes, con lenguaje simple | Ahorro **medido** (kWh/día y %) separado del ahorro **declarado** (formulario de impacto percibido) |
| Un solo estado claro | Cuántos negocios están en cada estado |
| Su propio dato | Solo agregados con mínimo 3 negocios por grupo |

---

## Decisión 4: Qué pasa cuando algo falla

| Falla | Qué ve Inés | Qué hace el sistema |
|---|---|---|
| IA no responde o responde 402 (sin cupo) | El plan con los pasos del catálogo, sin subtareas. Mensaje: «Las ideas extra no están disponibles ahora.» | Tiempo límite de 8 s; no reintenta en bucle. La recomendación y la medición **no dependen** de la IA. |
| El correo no sale | Nada distinto: la recomendación ya está en la app. | Reintento con espera creciente (máximo 3). Registro por persona y plantilla para no repetir. No escribe a correos que rebotaron. |
| Foto de factura ilegible | La factura se guarda con los números que ella escribió. Etiqueta «sin verificar». | No bloquea. Sí cuenta para su vista, pero **no cuenta para el reporte a aliados** hasta verificarla. |
| Edita una factura | La cifra se actualiza y aparece «actualizado por cambio en tu factura de ___». | Se recalcula desde cero (ver abajo). |
| Borra una factura | Igual que editar. | Borrado lógico; recálculo desde cero. |

### Recálculo sin contar dos veces

- La medición **no se guarda como suma acumulada**. Es una función pura de: facturas vigentes + fechas del plan + versión de reglas.
- Cada medición guardada (`savings_measurements`) incluye `inputsHash` (hash de las facturas usadas). Si el hash cambia, se recalcula y se reemplaza.
- Así, una misma factura nunca cuenta dos veces y la app y el reporte nunca muestran cifras distintas del mismo dato.
- Un cambio de estado (por ejemplo, de `savings` a `insufficient_data` tras borrar) se muestra con su motivo.

---

## Decisión 5: Datos de otros negocios

- **Mínimo 3 negocios** con facturas de antes y después para mostrar un porcentaje. Con menos, el texto dice «pocos casos todavía» y no muestra número.
- Se muestra la **mediana** y la cantidad de negocios: «−6 %, según 4 panaderías».
- Nunca se muestra el nombre, la ciudad exacta ni datos individuales.
- Grupos amplios: sector + región (Perú y Bolivia juntos), no por ciudad.
- Por qué 3 y no 5: con 5, ninguna ecoinnovación de energía para panaderías tendría un dato útil hoy (burletes tiene 4). Con 3 se evita identificar a un negocio sin quedarse sin información.

Aplicado hoy: burletes (4) y LED (5) muestran número; tandas (2) y aislamiento (1) no.

---

## Decisión 6: Tecnologías

| Parte | Elección | Por qué |
|---|---|---|
| API | Node.js existente; módulos `recommendation` y `savings` | Mismo stack del equipo, sin nuevo lenguaje que mantener. |
| Cálculos | Funciones puras en TypeScript + `simple-statistics` | Fáciles de probar. |
| Base de datos | MongoDB: colecciones `recommendations` y `savings_measurements`; índices por `businessId` | Ya existe. |
| Reglas | Archivo JSON versionado (`rulesVersion`) | Ajustar pesos sin desplegar código. |
| Frontend | React; dos tarjetas livianas; sin librerías de gráficos pesadas | Datos móviles limitados. |
| Despliegue | Contenedores Docker en el entorno actual de la API | Sin infraestructura nueva. |
| Pruebas | Vitest con los datos del caso (Inés); pruebas de contrato para la IA y el correo | Ver `tasks.md`. |
| Diagrama | Librería `diagrams` de Python (solo para dibujarlo) | No forma parte del sistema. |

## Supuestos a validar con el equipo

1. Equivalencias de inversión y tiempo en soles y horas.
2. Que se pueda agregar `mainLoads` al perfil.
3. Que los aliados acepten «ahorro medido» con un mínimo de 2 facturas antes y 2 después.
4. Que el campo `costPerKwh` de la factura más reciente refleje la tarifa actual.
