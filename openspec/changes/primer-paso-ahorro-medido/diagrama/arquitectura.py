"""Diagrama de arquitectura: Primer paso con ahorro medido (Kamai).

Muestra datos, integraciones, fallas y que corre donde.
Python solo se usa para DIBUJAR el diagrama. No forma parte del sistema.

Uso:
    pip install diagrams      # requiere Graphviz instalado
    python arquitectura.py    # genera arquitectura.png
"""

from diagrams import Cluster, Diagram, Edge
from diagrams.generic.storage import Storage
from diagrams.onprem.client import User
from diagrams.onprem.database import Mongodb
from diagrams.onprem.network import Internet
from diagrams.programming.flowchart import Decision, Document
from diagrams.programming.framework import React
from diagrams.programming.language import Nodejs

graph_attr = {
    "fontsize": "22",
    "pad": "0.6",
    "splines": "ortho",
    "nodesep": "0.7",
    "ranksep": "1.1",
}

FALLA = {"color": "firebrick", "fontcolor": "firebrick", "style": "dashed"}

with Diagram(
    "Kamai - Primer paso con ahorro medido",
    filename="arquitectura",
    show=False,
    direction="LR",
    graph_attr=graph_attr,
):
    ines = User("Ines\n(dueña de panaderia)")
    aliado = User("Aliados\n(financiadores)")

    # ---------- Corre en el CELULAR (navegador) ----------
    with Cluster("CORRE EN: celular de Ines (navegador)\nReact + Vite, liviano, datos moviles"):
        tarjeta_paso = React("Tarjeta 'Tu primer paso'\n(inicio, catalogo, diagnostico)")
        tarjeta_ahorro = React("Tarjeta 'Tu ahorro'\n(4 estados)")
        subir_factura = React("Subir factura\n(foto + kWh, dias, S/)")

    # ---------- Corre en el SERVIDOR (Docker) ----------
    with Cluster("CORRE EN: servidor de Kamai (contenedores Docker)\nAPI Node.js"):
        api = Nodejs("API REST")

        with Cluster("Modulo recomendacion"):
            reglas = Document("Reglas JSON\n(rulesVersion)")
            motor = Decision("Motor de reglas\nfiltros + puntaje\n-> 1 primer paso")
            plantilla = Document("Plantilla fija\nde explicacion")

        with Cluster("Modulo ahorro"):
            medicion = Decision("measureSavings()\nkWh/dia vs linea base\numbral = max(3%, 2sd)\ntarifa actual")

        with Cluster("Jobs"):
            correo_job = Nodejs("Correo bienvenida\n(lee recomendacion)")
            reporte = Nodejs("Reporte aliados\nmediana, n >= 3\nmedido vs declarado")

    # ---------- Base de datos ----------
    with Cluster("CORRE EN: MongoDB (servidor)"):
        db = Mongodb("profiles, plans\n(startedAt, completedAt)\ninvoices (verificada?)")
        db_rec = Mongodb("recommendations\nsavings_measurements\n(inputsHash)")

    # ---------- Servicios externos ----------
    with Cluster("CORRE EN: servicios externos"):
        ia = Internet("Proveedor IA\n(cupo mensual)")
        mail = Storage("Servicio de\nmensajeria")

    # ---------- Fallas y respuesta ----------
    with Cluster("FALLAS -> que pasa"):
        f_ia = Document("IA no responde / 402\n-> plantilla + pasos\ndel catalogo")
        f_mail = Document("Correo falla\n-> 3 reintentos;\nno repite; no escribe\na correos que rebotaron")
        f_foto = Document("Foto ilegible\n-> se guarda 'sin verificar';\nfuera del reporte")
        f_edit = Document("Edita / borra factura\n-> recalculo desde cero\n(nunca suma doble)")
        f_datos = Document("< 2 facturas\n-> 'Todavia no\npodemos saberlo'")

    # Flujo principal: recomendacion
    ines >> tarjeta_paso >> Edge(label="GET /recommendations/first-step") >> api
    api >> motor
    reglas >> motor
    db >> Edge(label="perfil, diagnostico, planes") >> motor
    motor >> Edge(label="guarda porque") >> db_rec
    motor >> plantilla
    plantilla >> Edge(label="solo redacta, sin cifras\n(timeout 8 s)", style="dashed") >> ia

    # Flujo principal: ahorro
    ines >> subir_factura >> Edge(label="POST /invoices") >> api
    ines >> tarjeta_ahorro >> Edge(label="GET /user-eco-card/:id/savings") >> api
    api >> medicion
    db >> Edge(label="facturas vigentes") >> medicion
    medicion >> db_rec

    # Jobs
    db_rec >> correo_job >> mail
    db_rec >> reporte
    aliado >> Edge(label="GET /partners/savings-report") >> reporte

    # Fallas
    ia >> Edge(**FALLA) >> f_ia
    mail >> Edge(**FALLA) >> f_mail
    subir_factura >> Edge(**FALLA) >> f_foto
    db >> Edge(**FALLA) >> f_edit
    medicion >> Edge(**FALLA) >> f_datos
