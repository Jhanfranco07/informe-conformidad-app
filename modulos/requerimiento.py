import streamlit as st
from docxtpl import DocxTemplate
import pandas as pd
from datetime import datetime
import base64
import os

def mostrar():
    st.set_page_config(page_title="Requerimiento de Servicios", page_icon="📝", layout="centered")

    st.title("📑 Generador de Documentos de Requerimiento de Servicios")

    # Cargar datos
    df = pd.read_excel("datos/proveedores.xlsx")

    # Mes en español
    meses = {
        "January": "enero", "February": "febrero", "March": "marzo",
        "April": "abril", "May": "mayo", "June": "junio",
        "July": "julio", "August": "agosto", "September": "septiembre",
        "October": "octubre", "November": "noviembre", "December": "diciembre"
    }

    # Selección de proveedor
    with st.expander("👤 Datos del Proveedor", expanded=True):
        nombre_proveedor = st.selectbox("Selecciona un proveedor", ["Selecciona un proveedor"] + df["NOMBRE Y APELLIDOS"].tolist())
        dni = ruc = direccion = celular = servicio = ""
        
        if nombre_proveedor != "Selecciona un proveedor":
            proveedor_info = df[df["NOMBRE Y APELLIDOS"] == nombre_proveedor].iloc[0]
            dni = str(proveedor_info["N° DNI"])
            ruc = str(proveedor_info["N° RUC"])
            direccion = proveedor_info["DIRECCION"]
            servicio = proveedor_info["SERVICIO"]
            celular = str(proveedor_info.get("CELULAR", ""))

            st.text_input("🔢 DNI", value=dni, disabled=True)
            st.text_input("🏢 RUC", value=ruc, disabled=True)
            st.text_area("📍 Dirección", value=direccion, disabled=True)
            st.text_area("🛠️ Servicio", value=servicio, disabled=True)
            st.text_input("📱 Celular", value=celular, disabled=True)

    with st.expander("📝 Información adicional a completar"):
        n_servicio = st.text_input("📌 Nº de requerimiento del servicio")
        dias = st.text_input("⏳ Plazo del servicio (días)", max_chars=2)
        oferta = st.text_input("💰 Monto total ofertado (S/)", placeholder="Ej. 1500.00")
        mes_manual = st.selectbox("📆 Mes del documento", list(meses.values()))

    nombre_empleado = st.text_input("✍️ Tu nombre para el archivo generado")

    if st.button("📄 Generar Documento de Requerimiento"):
        campos = {
            "Proveedor": nombre_proveedor,
            "DNI": dni,
            "RUC": ruc,
            "Dirección": direccion,
            "Celular": celular,
            "Servicio": servicio,
            "Días": dias,
            "Oferta": oferta,
            "N° Servicio": n_servicio,
            "Mes": mes_manual,
            "Nombre": nombre_empleado
        }

        errores = [k for k, v in campos.items() if v.strip() == "" or v == "Selecciona un proveedor"]
        if errores:
            st.error("❌ Corrige los siguientes campos: " + ", ".join(errores))
        else:
            context = {
                "nombre_completo": nombre_proveedor,
                "dni": dni,
                "ruc": ruc,
                "direccion": direccion,
                "celular": celular,
                "servicio": servicio,
                "dias": dias,
                "oferta": oferta,
                "n_servicio": n_servicio,
                "mes": mes_manual
            }

            plantilla = "plantilla/requerimientos_unificada.docx"
            doc = DocxTemplate(plantilla)
            doc.render(context)

            nombre_archivo = f"{nombre_empleado.upper()}_REQUERIMIENTO_{n_servicio}.docx"
            doc.save(nombre_archivo)

            with open(nombre_archivo, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="{nombre_archivo}">📥 Descargar Documento de Requerimiento</a>'
                st.markdown(href, unsafe_allow_html=True)

            os.remove(nombre_archivo)
            st.success("✅ Documento generado correctamente.")
