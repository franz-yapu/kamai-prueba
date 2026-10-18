# Tareas: Primer paso con ahorro medido

## 1. Datos

- [ ] 1.1 Agregar al perfil `mainLoads`, `budget` y `weeklyHours`
- [ ] 1.2 Agregar al plan `startedAt`, `completedAt` e historial de estados
- [ ] 1.3 Agregar a la factura `currency`, `verificationStatus` y borrado lógico (`deletedAt`)
- [ ] 1.4 Crear colección `recommendations` con índice por `businessId`
- [ ] 1.5 Crear colección `savings_measurements` con índice por `businessId` y `userEcoCardId`
- [ ] 1.6 Migración: llenar `startedAt`/`completedAt` de planes existentes con sus fechas de cambio de estado

## 2. Motor de recomendación

- [ ] 2.1 Archivo de reglas JSON versionado (pesos, equivalencias de inversión y tiempo)
- [ ] 2.2 Filtros duros: categoría, presupuesto, horas, planes trabados
- [ ] 2.3 Puntaje: mayor consumo, facilidad, finalización en negocios similares (n ≥ 3), diagnóstico
- [ ] 2.4 Desempate por complejidad e inversión
- [ ] 2.5 Guardar recomendación con `reasons[]` y `rulesVersion`
- [ ] 2.6 Recalcular ante cambios de perfil, diagnóstico, factura o plan
- [ ] 2.7 Endpoint `GET /recommendations/first-step`
- [ ] 2.8 Pruebas con los datos de Inés: debe salir «Hornear por tandas»; aislamiento y calentador descartados

## 3. Explicación

- [ ] 3.1 Plantilla fija con datos del motor (incluye «pocos casos» cuando n < 3)
- [ ] 3.2 Reescritura opcional con el modelo de lenguaje, validando que no cambie cifras
- [ ] 3.3 Tiempo límite de 8 s y uso de la plantilla ante error o 402
- [ ] 3.4 Pruebas de contrato con el proveedor de IA simulado (éxito, demora, 402)

## 4. Medición del ahorro

- [ ] 4.1 Función pura `measureSavings(facturas, plan, reglas)`
- [ ] 4.2 kWh por día, línea base, periodo de transición excluido
- [ ] 4.3 Umbral = max(3 %, 2 × desviación / línea base)
- [ ] 4.4 Cuatro estados: `insufficient_data`, `no_clear_change`, `savings`, `increase`
- [ ] 4.5 Ahorro en soles con tarifa más reciente y rango (± 1 desviación)
- [ ] 4.6 `inputsHash` y recálculo desde cero al editar o borrar facturas
- [ ] 4.7 Endpoint `GET /user-eco-card/:id/savings`
- [ ] 4.8 Pruebas con los datos de Inés:
  - [ ] Febrero vs. enero → no es ahorro (+1,7 % por día)
  - [ ] Subida de tarifa sola → sin ahorro ni gasto
  - [ ] 1 factura posterior → `insufficient_data`
  - [ ] 53,1 kWh/día después → `savings`, entre S/ 128 y S/ 204
  - [ ] Borrar factura → vuelve a `insufficient_data`
  - [ ] Mismos datos → mismo resultado

## 5. Privacidad y reporte para aliados

- [ ] 5.1 Agregados por sector y región con mínimo 3 negocios y mediana
- [ ] 5.2 Excluir facturas «sin verificar» del reporte
- [ ] 5.3 Endpoint `GET /partners/savings-report` (medido y declarado por separado)
- [ ] 5.4 Pruebas: grupo de 2 → sin número; grupo de 4 → mediana y cantidad

## 6. Correo de bienvenida

- [ ] 6.1 Leer la recomendación guardada en lugar de las 3 fijas
- [ ] 6.2 Reintentos (máximo 3) con espera creciente
- [ ] 6.3 Registro por persona y plantilla para no repetir; no escribir a correos que rebotaron

## 7. Frontend (React, pensado para el celular)

- [ ] 7.1 Tarjeta «Tu primer paso» en inicio, catálogo y diagnóstico (misma fuente)
- [ ] 7.2 Tarjeta «Tu ahorro» con los 4 estados y textos simples
- [ ] 7.3 Aviso «sin verificar» en facturas con foto ilegible
- [ ] 7.4 Aviso «actualizado por un cambio en tu factura»
- [ ] 7.5 Sin librerías de gráficos pesadas; probar con conexión lenta

## 8. Entrega

- [ ] 8.1 Diagrama de arquitectura (librería `diagrams` de Python, solo para dibujar)
- [ ] 8.2 Despliegue en contenedores Docker en el entorno actual
- [ ] 8.3 Validar supuestos con el equipo (equivalencias, `mainLoads`, criterio de los aliados)
