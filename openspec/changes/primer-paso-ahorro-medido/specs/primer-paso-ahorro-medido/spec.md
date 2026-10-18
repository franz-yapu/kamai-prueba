# Primer paso con ahorro medido

## ADDED Requirements

### Requirement: Recomendación única del primer paso

El sistema SHALL recomendar una sola ecoinnovación como primer paso para cada negocio, calculada por un motor de reglas con puntaje, y SHALL guardar la recomendación con sus razones y la versión de reglas usada.

#### Scenario: Panadería con el horno como mayor consumo

- **WHEN** un negocio de categoría panadería tiene objetivo ENERGY, presupuesto de S/ 1.200, 4 horas por semana y declara el horno como su mayor consumo
- **THEN** el sistema recomienda «Hornear por tandas»
- **AND** guarda la recomendación con `score`, `reasons[]` y `rulesVersion`

#### Scenario: Ecoinnovación que no cabe en el presupuesto

- **WHEN** una ecoinnovación tiene inversión ALTA y el presupuesto del negocio es menor a S/ 3.000
- **THEN** el sistema no la recomienda como primer paso
- **AND** la sigue mostrando en el catálogo

#### Scenario: Inversión MEDIA con presupuesto intermedio

- **WHEN** una ecoinnovación tiene inversión MEDIA y el presupuesto del negocio es de S/ 1.200
- **THEN** el sistema no la descarta, porque el presupuesto alcanza el piso del nivel MEDIA (S/ 501)
- **AND** le asigna un puntaje de facilidad menor que a una ecoinnovación de inversión BAJA

#### Scenario: Plan trabado

- **WHEN** el negocio tiene un plan de una ecoinnovación en estado `delayed` o sin avance por más de 6 semanas
- **THEN** el sistema no vuelve a recomendar esa ecoinnovación como primer paso
- **AND** recomienda la siguiente con mayor puntaje

#### Scenario: Empate en puntaje

- **WHEN** dos ecoinnovaciones obtienen el mismo puntaje
- **THEN** el sistema elige la de menor complejidad y, si sigue el empate, la de menor inversión

#### Scenario: Negocio nuevo sin facturas

- **WHEN** un negocio nuevo completa su perfil y su diagnóstico sin haber subido facturas
- **THEN** el sistema calcula la recomendación con el perfil, el diagnóstico y el catálogo
- **AND** le pide subir 2 facturas anteriores para tener línea base

### Requirement: Una sola fuente de recomendación

El inicio, el catálogo, el diagnóstico por etapas y el correo de bienvenida SHALL mostrar la misma recomendación vigente guardada y SHALL NOT calcular recomendaciones por su cuenta.

#### Scenario: Los cuatro lugares coinciden

- **WHEN** Inés abre el inicio, el catálogo y el diagnóstico, y recibe el correo de bienvenida
- **THEN** los cuatro muestran «Hornear por tandas» como primer paso

#### Scenario: Recalcular ante cambios

- **WHEN** cambia el perfil, el diagnóstico, una factura o el estado de un plan del negocio
- **THEN** el sistema recalcula la recomendación
- **AND** guarda una nueva versión sin borrar el historial

### Requirement: Explicación con plantilla

El sistema SHALL explicar la recomendación con una plantilla fija llenada con los datos del motor. El modelo de lenguaje MAY reescribir el texto, pero SHALL NOT agregar ni cambiar cifras.

#### Scenario: Pocos casos de otros negocios

- **WHEN** la ecoinnovación recomendada tiene menos de 3 negocios similares con facturas de antes y después
- **THEN** la explicación dice «todavía son pocos casos» y no muestra ningún porcentaje

#### Scenario: Servicio de IA caído

- **WHEN** el proveedor de IA no responde en 8 segundos o responde con error, incluido 402
- **THEN** el sistema muestra la explicación de la plantilla
- **AND** muestra el plan con los pasos del catálogo, sin subtareas generadas

### Requirement: Medición del ahorro por día con tarifa constante

El sistema SHALL medir el ahorro comparando el consumo promedio en kWh por día de las facturas completas posteriores a `completedAt` contra la línea base de las facturas completas anteriores a `startedAt`, y SHALL valorar la diferencia en soles con la tarifa más reciente.

#### Scenario: Febrero no es ahorro

- **WHEN** se compara febrero (1.690 kWh en 28 días) con enero (1.840 kWh en 31 días)
- **THEN** el sistema calcula 60,4 kWh/día contra 59,4 kWh/día, un aumento de 1,7 %
- **AND** no muestra «ahorraste S/ 117»

#### Scenario: Subida de tarifa

- **WHEN** la tarifa pasa de S/ 0,78 a S/ 0,84 por kWh y el consumo por día no cambia
- **THEN** el sistema no muestra ahorro ni gasto atribuible al negocio

#### Scenario: Facturas del periodo de implementación

- **WHEN** una factura cubre días entre `startedAt` y `completedAt`
- **THEN** el sistema no la usa ni como línea base ni como periodo posterior

#### Scenario: Ahorro medido con rango

- **WHEN** la línea base de Inés es 59,7 kWh/día con desviación de 1,5 kWh/día, y sus 2 facturas posteriores promedian 53,1 kWh/día en periodos de 30 días con tarifa de S/ 0,84
- **THEN** el estado es `savings`
- **AND** la app muestra «Ahorraste entre S/ 128 y S/ 204 este mes»

### Requirement: Estados honestos de la medición

El sistema SHALL asignar a cada medición uno de cuatro estados: `insufficient_data`, `no_clear_change`, `savings` o `increase`. El umbral SHALL ser el mayor entre 3 % y dos desviaciones estándar de la línea base divididas entre la línea base.

#### Scenario: Faltan facturas posteriores

- **WHEN** el negocio tiene menos de 2 facturas completas posteriores a `completedAt`
- **THEN** el estado es `insufficient_data`
- **AND** la app dice «Todavía no podemos saberlo» e indica qué factura falta subir

#### Scenario: Falta línea base

- **WHEN** el negocio tiene menos de 2 facturas completas anteriores a `startedAt`
- **THEN** el estado es `insufficient_data`

#### Scenario: Cambio dentro de la variación normal

- **WHEN** el cambio por día es menor que el umbral, en positivo o en negativo
- **THEN** el estado es `no_clear_change`
- **AND** la app dice «Tu consumo no cambió más de lo normal. Puede ser muy pronto.»

#### Scenario: Consumo sube

- **WHEN** el consumo por día sube más que el umbral
- **THEN** el estado es `increase`
- **AND** la app no muestra cifras de ahorro

#### Scenario: Menos de 12 meses de historial

- **WHEN** el negocio tiene menos de 12 meses de facturas
- **THEN** la app avisa que la medición no corrige la temporada

### Requirement: Recálculo sin contar dos veces

El sistema SHALL calcular la medición a partir de las facturas vigentes, las fechas del plan y la versión de reglas, y SHALL NOT acumular sumas parciales.

#### Scenario: Factura editada

- **WHEN** el negocio edita los kWh de una factura usada en una medición
- **THEN** el sistema recalcula la medición desde cero y reemplaza la anterior
- **AND** la app muestra «Actualizado por un cambio en tu factura de <mes>»

#### Scenario: Factura borrada

- **WHEN** el negocio borra una factura y quedan menos de 2 facturas posteriores
- **THEN** el estado cambia a `insufficient_data` y se muestra el motivo

#### Scenario: Mismos datos, mismo resultado

- **WHEN** se recalcula una medición sin que cambien las facturas ni las fechas
- **THEN** el `inputsHash` es igual y el resultado no cambia

### Requirement: Facturas sin verificar

El sistema SHALL guardar facturas cuya foto sea ilegible con los números escritos por el negocio, marcadas como «sin verificar».

#### Scenario: Foto ilegible

- **WHEN** el negocio sube una factura con una foto ilegible
- **THEN** la factura cuenta para la medición que ve el negocio
- **AND** no cuenta para el reporte a aliados hasta ser verificada

### Requirement: Privacidad de los datos de otros negocios

El sistema SHALL mostrar resultados de otros negocios solo como mediana de grupos de al menos 3 negocios con facturas de antes y después, sin datos que identifiquen a ninguno.

#### Scenario: Grupo suficiente

- **WHEN** burletes tiene 4 panaderías con facturas de antes y después
- **THEN** la app muestra «−6 %, según 4 panaderías»

#### Scenario: Grupo pequeño

- **WHEN** hornear por tandas tiene 2 panaderías con facturas de antes y después
- **THEN** la app muestra «pocos casos todavía» y ningún porcentaje

### Requirement: Reporte para aliados

El sistema SHALL ofrecer un reporte agregado que separe el ahorro medido del ahorro declarado y cuente los negocios por estado de medición.

#### Scenario: Reporte trimestral

- **WHEN** un aliado pide el reporte de un trimestre
- **THEN** el sistema devuelve, por sector y región, el ahorro medido en kWh/día y %, el ahorro declarado por separado y cuántos negocios hay en cada estado
- **AND** omite los grupos con menos de 3 negocios

### Requirement: Correo de bienvenida confiable

El sistema SHALL reintentar el envío de un correo que falla hasta 3 veces con espera creciente, y SHALL NOT enviar el mismo correo dos veces a la misma persona.

#### Scenario: Falla el envío

- **WHEN** el proveedor de correo falla al enviar la bienvenida
- **THEN** el sistema reintenta hasta 3 veces
- **AND** la recomendación sigue visible en la app

#### Scenario: Correo que rebota

- **WHEN** un correo rebotó antes
- **THEN** el sistema no vuelve a escribir a esa dirección
