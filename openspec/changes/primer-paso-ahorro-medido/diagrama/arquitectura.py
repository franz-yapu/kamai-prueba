"""Diagrama de arquitectura: Primer paso con ahorro medido (Kamai).

Python solo se usa para DIBUJAR el diagrama. No forma parte del sistema.

Uso:
    pip install diagrams      # requiere Graphviz instalado
    python arquitectura.py    # genera arquitectura.png
"""

from diagrams import Cluster, Diagram, Edge
from diagrams.onprem.client import User
from diagrams.onprem.database import Mongodb
from diagrams.onprem.network import Internet
from diagrams.programming.framework import React
from diagrams.programming.language import Nodejs
from diagrams.generic.storage import Storage
from diagrams.programming.flowchart import Document, Decision

graph_attr = {"fontsize": "20", "pad": "0.5", "splines": "spline", "nodesep": "0.6", "ranksep": "0.9"}

with Diagram(
    "Kamai - Primer paso con ahorro medido",
    filename="arquitectura",
    show=False,
    direction="LR",
    graph_attr=graph_attr,
):
    ines = User("Negocio (Ines)\ncelular, datos limitados")
    aliado = User("Aliados\n(financiadores)")

    with Cluster("Frontend - React + Vite"):
        tarjeta_paso = React("Tarjeta\n'Tu primer paso'\n(inicio, catalogo,\ndiagnostico)")
        tarjeta_ahorro = React("Tarjeta\n'Tu ahorro'\n(4 estados)")

    with Cluster("API - Node.js (Docker)"):
        api = Nodejs("Endpoints REST")

        with Cluster("Modulo recomendacion"):
            reglas = Document("Reglas JSON\nversionadas")
            motor = Decision("Motor de reglas\nfiltros + puntaje")

        with Cluster("Modulo ahorro"):
            medicion = Decision("measureSavings()\nkWh/dia, linea base,\numbral, 4 estados")

        plantilla = Document("Plantilla fija\n(explicacion)")
        reporte = Nodejs("Reporte aliados\nmin. 3 negocios")
        correo = Nodejs("Correo bienvenida\n3 reintentos")

    with Cluster("MongoDB"):
        db = Mongodb("profiles, plans,\ninvoices")
        db_rec = Mongodb("recommendations\nsavings_measurements")

    ia = Internet("Proveedor IA\n(opcional, 8 s)")
    mail = Storage("Proveedor\nde correo")

    ines >> tarjeta_paso >> api
    ines >> tarjeta_ahorro >> api
    api >> Edge(label="GET /recommendations/first-step") >> motor
    reglas >> motor
    motor >> db_rec
    motor >> plantilla
    plantilla >> Edge(style="dashed", label="solo redacta, sin cifras") >> ia
    api >> Edge(label="GET /user-eco-card/:id/savings") >> medicion
    db >> Edge(label="facturas vigentes") >> medicion
    medicion >> Edge(label="inputsHash") >> db_rec
    db >> motor
    aliado >> Edge(label="GET /partners/savings-report") >> reporte
    db_rec >> reporte
    db_rec >> correo >> mail
