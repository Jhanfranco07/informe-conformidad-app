import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime
import base64
import os

# Cargar plantilla
TEMPLATE_PATH = "plantilla.docx"

# Título
st.title("Generador de Informes de Conformidad")
st.markdown("Llena el formulario para generar el informe en formato Word.")

# Formulario
with st.form("formulario"):
    numero = st.text_input("Nº de Informe", "001")
    gerencia = st.text_input("Gerencia solicitante", "GERENCIA DE LICENCIAS Y DESARROLLO ECONÓMICO")
    proveedor = st.text_input("Proveedor", "LIZET ...")
    ruc = st.text_input("RUC", "12345678901")
    concepto = st.text_input("Concepto", "SERVICIO DE ANALISIS ORGANIZACIONAL")
    orden_servicio = st.text_input("Orden de Servicio", "XXXX")
    fecha_orden = st.date_input("Fecha de la O.S.")
    plazo = st.text_input("Plazo del servicio", "80")
    fecha_inicio = st.date_input("Inicio del servicio")
    fecha_termino = st.date_input("Término del servicio")
    fecha_entrega = st.date_input("Fecha de entrega")
    referencia = st.text_input("Referencia del entregable", "2-3")
    fecha = st.date_input("Fecha de emisión", datetime.today())
    nombre_empleado = st.text_input("Tu nombre para el archivo generado", "JHAN")

    submitted = st.form_submit_button("Generar Informe")

if submitted:
    dias = (fecha_termino - fecha_inicio).days

    # Traducción manual de meses al español
    meses = {
        "January": "enero", "February": "febrero", "March": "marzo",
        "April": "abril", "May": "mayo", "June": "junio",
        "July": "julio", "August": "agosto", "September": "septiembre",
        "October": "octubre", "November": "noviembre", "December": "diciembre"
    }
    mes_nombre = meses[fecha.strftime("%B")]
    fecha_formateada = f"{fecha.day} de {mes_nombre} de {fecha.year}"

    doc = DocxTemplate(TEMPLATE_PATH)
    context = {
        "numero": numero,
        "gerencia": gerencia,
        "proveedor": proveedor,
        "ruc": ruc,
        "concepto": concepto,
        "orden_servicio": orden_servicio,
        "fecha_orden": fecha_orden.strftime("%d/%m/%Y"),
        "plazo": plazo,
        "fecha_inicio": fecha_inicio.strftime("%d/%m/%Y"),
        "fecha_termino": fecha_termino.strftime("%d/%m/%Y"),
        "fecha_entrega": fecha_entrega.strftime("%d/%m/%Y"),
        "dias": dias,
        "referencia": referencia,
        "fecha": fecha_formateada
    }

    output_path = f"{nombre_empleado.upper()}_CONFORMIDAD_{numero}.docx"
    doc.render(context)
    doc.save(output_path)

    with open(output_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        href = f'<a href="data:application/octet-stream;base64,{b64}" download="{output_path}">Descargar Informe</a>'
        st.success("Informe generado exitosamente.")
        st.markdown(href, unsafe_allow_html=True)

    os.remove(output_path)
