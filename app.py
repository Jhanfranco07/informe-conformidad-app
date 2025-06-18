import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime
import base64
import os

# Estilo visual
st.set_page_config(page_title="Generador asasade Documentos", page_icon="📝", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .block-container { padding-top: 2rem; }
    .stButton>button { background-color: #0d6efd; color: white; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# Traducción manual de meses al español
meses = {
    "January": "enero", "February": "febrero", "March": "marzo",
    "April": "abril", "May": "mayo", "June": "junio",
    "July": "julio", "August": "agosto", "September": "septiembre",
    "October": "octubre", "November": "noviembre", "December": "diciembre"
}

# Selección de tipo de documento
st.title("📝 Generador de Documentos Institucionales")
tipo_doc = st.selectbox("Selecciona el tipo de documento que deseas generar:", ["Informe de Conformidad", "Informe de Actividades"])

if tipo_doc == "Informe de Conformidad":
    st.header("📄 Informe de Conformidad")
    st.markdown("Llena el formulario para generar el informe en formato Word.")

    with st.form("formulario_conformidad"):
        numero = st.text_input("Nº de Informe")
        gerencia = st.selectbox("Gerencia solicitante", ["Seleccione una opción", "GERENCIA DE LICENCIAS Y DESARROLLO ECONÓMICO", "GERENCIA DE DESARROLLO URBANO"])
        proveedor = st.text_input("Proveedor")
        ruc = st.text_input("RUC")
        concepto = st.text_input("Concepto")
        orden_servicio = st.text_input("Orden de Servicio")
        fecha_orden = st.date_input("Fecha de la O.S.")
        plazo = st.text_input("Plazo del servicio")
        fecha_inicio = st.date_input("Inicio del servicio")
        fecha_termino = st.date_input("Término del servicio")
        fecha_entrega = st.date_input("Fecha de entrega")
        referencia = st.text_input("Referencia del entregable")
        fecha = st.date_input("Fecha de emisión", datetime.today())
        nombre_empleado = st.text_input("Tu nombre para el archivo generado")

        submitted = st.form_submit_button("Generar Informe")

    if submitted:
        campos_obligatorios = {
            "Nº de Informe": numero,
            "Gerencia": gerencia,
            "Proveedor": proveedor,
            "RUC": ruc,
            "Concepto": concepto,
            "Orden de Servicio": orden_servicio,
            "Plazo": plazo,
            "Referencia": referencia,
            "Nombre para el archivo": nombre_empleado
        }

        errores = [campo for campo, valor in campos_obligatorios.items() if valor.strip() == "" or valor == "Seleccione una opción"]

        if errores:
            st.error(f"❌ Por favor completa los siguientes campos obligatorios: {', '.join(errores)}")
        else:
            dias = max((fecha_termino - fecha_inicio).days, 1)
            mes_nombre = meses[fecha.strftime("%B")]
            fecha_formateada = f"{fecha.day} de {mes_nombre} de {fecha.year}"

            TEMPLATE_PATH = "plantilla_conformidad.docx"
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
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="{output_path}">📥 Descargar Informe</a>'
                st.success("Informe generado exitosamente.")
                st.markdown(href, unsafe_allow_html=True)

            os.remove(output_path)

elif tipo_doc == "Informe de Actividades":
    st.header("📑 Informe de Actividades")
    st.info("Esta sección está en desarrollo. Muy pronto podrás generar informes automáticos de actividades.")

