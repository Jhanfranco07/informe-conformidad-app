import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime
import pandas as pd
import base64
import os

def mostrar():
    st.set_page_config(page_title="Informe Unificado", page_icon="\U0001F4C4", layout="centered")
    st.markdown("""
        <style>
        .main { background-color: #f8f9fa; }
        .block-container { padding-top: 2rem; }
        .stButton>button { background-color: #0d6efd; color: white; border-radius: 5px; }
        </style>
    """, unsafe_allow_html=True)

    meses = {
        "January": "enero", "February": "febrero", "March": "marzo",
        "April": "abril", "May": "mayo", "June": "junio",
        "July": "julio", "August": "agosto", "September": "septiembre",
        "October": "octubre", "November": "noviembre", "December": "diciembre"
    }

    referencias_letras = {"1": "primer", "2": "segundo", "3": "tercer", "4": "cuarto"}

    df = pd.read_excel("datos/proveedores.xlsx")

    st.title("\U0001F4C4 Generador de Informe Único de Conformidad y Actividades")

    col1, col2 = st.columns(2)
    with col1:
        numero = st.text_input("📄 Nº de Informe de Conformidad")
        numero_sustento = st.text_input("📎 Nº de Informe de Actividades")
        gerencia = st.selectbox("🏢 Gerencia solicitante", [
            "Seleccione una opción",
            "GERENCIA DE LICENCIAS Y DESARROLLO ECONÓMICO",
            "GERENCIA DE DESARROLLO URBANO"
        ])
    with col2:
        orden_servicio = st.text_input("📝 Orden de Servicio")
        plazo = st.text_input("⏳ Plazo del servicio (días)")
        referencia = st.selectbox("📌 Referencia del entregable", ["", "1", "2", "3", "4"])

    st.markdown("---")

    with st.expander("📁 Datos del Proveedor", expanded=True):
        nombre_proveedor = st.selectbox("👤 Selecciona el proveedor", ["Selecciona un proveedor"] + df["NOMBRE Y APELLIDOS"].tolist())
        ruc = concepto = nombre_abrev = dni = actividades = ""

        if nombre_proveedor != "Selecciona un proveedor":
            proveedor_info = df[df["NOMBRE Y APELLIDOS"] == nombre_proveedor].iloc[0]
            ruc = str(proveedor_info["N° RUC"])
            concepto = proveedor_info["SERVICIO"]
            actividades = proveedor_info.get("ACTIVIDADES REALIZADAS", "")
            dni = str(proveedor_info["N° DNI"])

            st.text_input("🔢 RUC", value=ruc, disabled=True)
            st.text_area("🧾 Concepto", value=concepto, disabled=True)
            st.text_area("🛠️ Detalle de las actividades realizadas", value=actividades, disabled=True)

            partes = nombre_proveedor.strip().split()
            nombre_abrev = "".join([p[0] for p in partes[:4]]).upper()
            st.text_input("🔠 Nombre abreviado del proveedor", value=nombre_abrev, disabled=True)

    st.markdown("---")

    with st.expander("📅 Fechas del Servicio", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            fecha_orden = st.date_input("📆 Fecha de la Orden de Servicio")
            fecha_inicio = st.date_input("📆 Inicio del servicio")
            fecha_entrega = st.date_input("📆 Fecha de entrega del servicio")
        with col2:
            fecha_termino = st.date_input("📆 Término del servicio")
            fecha = st.date_input("📅 Fecha de emisión del informe", datetime.today())

    st.markdown("---")

    nombre_empleado = st.text_input("✍️ Tu nombre para el archivo generado")

    if st.button("\U0001F4DD Generar Informe Unificado"):
        campos_obligatorios = {
            "Nº Informe": numero,
            "Nº Sustento": numero_sustento,
            "Gerencia": gerencia,
            "Proveedor": nombre_proveedor,
            "RUC": ruc,
            "Concepto": concepto,
            "Orden de Servicio": orden_servicio,
            "Plazo": plazo,
            "Referencia": referencia,
            "Actividades": actividades,
            "Nombre archivo": nombre_empleado
        }

        errores = [campo for campo, valor in campos_obligatorios.items()
                   if valor.strip() == "" or valor in ["Seleccione una opción", "Selecciona un proveedor"]]

        if not ruc.isdigit() or len(ruc) != 11:
            errores.append("RUC (debe tener 11 dígitos)")
        if not plazo.isdigit():
            errores.append("Plazo (solo números)")

        if errores:
            st.error("❌ Corrige los siguientes campos: " + ", ".join(errores))
        else:
            dias = (fecha_termino - fecha_inicio).days + 1
            mes_nombre = meses[fecha.strftime("%B")]
            fecha_formateada = f"{fecha.day} de {mes_nombre} de {fecha.year}"
            referencia_2 = referencias_letras.get(referencia, "")

            context = {
                "numero": numero,
                "numero_sustento": numero_sustento,
                "gerencia": gerencia,
                "proveedor": nombre_proveedor,
                "ruc": ruc,
                "concepto": concepto,
                "orden_servicio": orden_servicio,
                "fecha_orden": fecha_orden.strftime("%d/%m/%Y"),
                "plazo": plazo,
                "f_inicio": fecha_inicio.strftime("%d/%m/%Y"),
                "f_termino": fecha_termino.strftime("%d/%m/%Y"),
                "fecha_entrega": fecha_entrega.strftime("%d/%m/%Y"),
                "dias": dias,
                "referencia": referencia,
                "referencia_2": referencia_2,
                "fecha": fecha_formateada,
                "nombre_abrev": nombre_abrev,
                "dni": dni,
                "actividades": actividades
            }

            plantilla = "plantilla/Plantilla_unificada.docx"
            doc = DocxTemplate(plantilla)
            doc.render(context)

            nombre_archivo = f"{nombre_empleado.upper()}_INFORME_CONFORMIDAD_{numero}.docx"
            doc.save(nombre_archivo)

            with open(nombre_archivo, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="{nombre_archivo}">📥 Descargar Informe de Conformidades y Sustento</a>'
                st.markdown(href, unsafe_allow_html=True)

            os.remove(nombre_archivo)
            st.success("✅ Informe unificado generado correctamente.")

