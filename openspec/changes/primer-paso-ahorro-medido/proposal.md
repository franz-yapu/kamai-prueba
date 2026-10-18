# Primer paso con ahorro medido

## Por qué

- Kamai tiene más de 40 ecoinnovaciones, pero no le dice a un negocio **por cuál empezar**. Hoy cuatro lugares (inicio, catálogo, diagnóstico por etapas y correo de bienvenida) recomiendan cosas distintas, y no se guarda por qué.
- El ahorro que se muestra es la resta entre las dos últimas facturas, y **engaña**. Ejemplo real del caso: en febrero Kamai le dijo a Inés «ahorraste S/ 117», pero febrero tuvo 3 días menos y, **por día, consumió 1,7 % más**. Además, la tarifa subió 8 % entre enero y junio.
- El embudo se rompe: de cada 10 negocios que eligen una ecoinnovación, 3 la completan y solo 1 deja facturas de antes y después. Sin eso, los aliados que financian el programa no ven ahorro medido.
- Inés siguió la primera recomendación que vio (aislamiento térmico del horno: inversión y complejidad ALTA) y lleva 7 semanas sin avanzar.

## Meta

1. Que cada negocio vea un **ahorro real** en su factura en sus primeros 90 días en Kamai.
2. Que Kamai reporte a los aliados un **ahorro medido**, separado del ahorro declarado.

Indicadores (las metas numéricas se definen con el equipo; línea base actual: 3 de 10 completan y 1 de 10 mide):

- % de negocios con línea base (2 o más facturas) al elegir su primer paso.
- % que completa su primer paso en 90 días.
- % con una medición válida (estado distinto de «todavía no podemos saberlo»).

## Qué cambia

1. **Un solo motor de recomendación**, con reglas versionadas, que elige la primera ecoinnovación y **guarda el porqué**. Los cuatro lugares de Kamai leen la misma recomendación guardada.
2. **Explicación honesta y simple**, generada con una plantilla. El modelo de lenguaje es opcional y solo mejora la redacción.
3. **Medición del ahorro** con kWh por día, tarifa constante, línea base de varios meses y un margen estadístico. Estados claros: ahorro medido, sin cambio claro, consumo subió o «todavía no podemos saberlo».
4. **Vínculo entre el plan y las facturas** por fechas (inicio y fin de la ecoinnovación).
5. **Reporte agregado para aliados**, sin exponer a ningún negocio (mínimo 3 negocios por grupo).
6. **Comportamiento definido ante fallas**: IA caída, correo que no sale, foto ilegible, factura editada o borrada.

## Alcance

- Energía eléctrica (luz). El modelo sirve igual para agua más adelante.
- Panaderías como caso piloto, con reglas genéricas por categoría y por equipo de mayor consumo.
- Aplica a negocios nuevos (sin facturas) y existentes.

## Fuera de alcance

- Entrenar modelos de aprendizaje automático o de ranking: con 23 panaderías y entre 1 y 11 casos por ecoinnovación no hay datos suficientes.
- Lectura automática (OCR) de las fotos de facturas.
- Agregar montos de inversión al catálogo y el filtro por país.
- Corrección por clima (grados-día).
- Rediseño visual general de la app.
- Integración con medidores eléctricos.

## Impacto

- **Datos**: perfil (equipos de mayor consumo, presupuesto y horas disponibles), plan (historial de estados, `startedAt`, `completedAt`), factura (moneda, estado de verificación, borrado lógico). Colecciones nuevas: `recommendations` y `savings_measurements`.
- **API**: `GET /recommendations/first-step`, `GET /user-eco-card/:id/savings`, `GET /partners/savings-report`.
- **Frontend**: tarjeta «Tu primer paso» y tarjeta «Tu ahorro», pensadas para el celular.
- **Correo de bienvenida**: deja de sugerir tres fijas y usa la recomendación guardada.
