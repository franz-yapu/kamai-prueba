# Kamai: Primer paso con ahorro medido

Prueba técnica de Franz Jhonny Yapu Mamani para el puesto de Especialista Fullstack Web en Agora Partnerships.

## Contenido

| Archivo | Qué es |
|---|---|
| `openspec/changes/primer-paso-ahorro-medido/proposal.md` | Por qué, meta y alcance |
| `openspec/changes/primer-paso-ahorro-medido/design.md` | Decisiones, alternativas descartadas y supuestos |
| `openspec/changes/primer-paso-ahorro-medido/specs/primer-paso-ahorro-medido/spec.md` | Requisitos con escenarios WHEN/THEN |
| `openspec/changes/primer-paso-ahorro-medido/tasks.md` | Tareas de implementación |
| `openspec/changes/primer-paso-ahorro-medido/diagrama/arquitectura.png` | Implementación parcial elegida: diagrama de arquitectura |
| `openspec/changes/primer-paso-ahorro-medido/diagrama/arquitectura.py` | Código que genera el diagrama (`pip install diagrams`, requiere Graphviz) |

## Resumen

- **Primer paso para Inés:** hornear por tandas (ataca el horno, su mayor consumo, sin inversión). Burletes como segundo paso.
- **IA:** reglas con puntaje para recomendar; estadística simple para medir; el modelo de lenguaje solo redacta, nunca pone cifras.
- **Ahorro:** kWh por día, tarifa constante, línea base de varios meses y umbral de variación normal. Si no hay datos: «todavía no podemos saberlo».
- **Privacidad:** datos de otros negocios solo en grupos de 3 o más.
