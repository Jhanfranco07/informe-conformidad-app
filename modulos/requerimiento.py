import streamlit as st
from docxtpl import DocxTemplate
import pandas as pd
from datetime import datetime
import base64
import os


def mostrar():
    st.set_page_config(page_title="Requerimiento de Servicios", page_icon="📝", layout="centered")
    st.markdown("""
        <style>
        .main { background-color: #f8f9fa; }
        .block-container { padding-top: 2rem; }
        .stButton>button { background-color: #0d6efd; color: white; border-radius: 5px; }
        .stTextInput>div>div>input, .stTextArea>div>textarea, .stSelectbox>div>div>div>div { border-radius: 6px; }
        .stExpander { border: 1px solid #dee2e6; border-radius: 8px; padding: 10px; }
        </style>
    """, unsafe_allow_html=True)

    st.title("📄 Requerimiento de Servicios")

    df = pd.read_excel("datos/proveedores1.xlsx")

    meses = {
        "January": "enero", "February": "febrero", "March": "marzo",
        "April": "abril", "May": "mayo", "June": "junio",
        "July": "julio", "August": "agosto", "September": "septiembre",
        "October": "octubre", "November": "noviembre", "December": "diciembre"
    }

    # =========================
    # DATOS DEL PROVEEDOR
    # =========================
    with st.container():
        nombre_proveedor = st.selectbox(
            "🔍 Selecciona un proveedor",
            ["Selecciona un proveedor"] + df["NOMBRE Y APELLIDOS"].tolist()
        )

        # Valores por defecto
        dni = ruc = servicio_base = direccion = celular = banco = cci = ""

        if nombre_proveedor != "Selecciona un proveedor":
            proveedor_info = df[df["NOMBRE Y APELLIDOS"] == nombre_proveedor].iloc[0]

            dni = str(proveedor_info.get("N° DNI", "")).strip()
            ruc = str(proveedor_info.get("N° RUC", "")).strip()
            servicio_base = str(proveedor_info.get("SERVICIO", "")).strip()
            direccion = str(proveedor_info.get("DIRECCION", "")).strip()
            celular = str(proveedor_info.get("CELULAR", "")).strip()
            banco = str(proveedor_info.get("BANCO", "")).strip()

            # ✅ CCI completo en un solo campo (normalizado)
            cci_raw = proveedor_info.get("CCI", "")
            cci = "".join(filter(str.isdigit, str(cci_raw)))  # solo números
            cci = cci.zfill(20) if cci else ""               # rellena a 20 si aplica

        # DNI / RUC (solo lectura)
        st.text_input("🔹 DNI", value=dni, disabled=True)
        st.text_input("🏢 RUC", value=ruc, disabled=True)

        # Servicio editable (prefill con lo leído)
        servicio = st.text_area(
            "🛠️ Servicio",
            value=servicio_base,
            placeholder="Describe el servicio a contratar...",
            help="Puedes editar el texto libremente antes de generar el documento."
        ).strip()

    # =========================
    # INFORMACIÓN ADICIONAL
    # =========================
    with st.container():
        with st.expander("📍 Información adicional a completar", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                n_servicio = st.text_input("📌 Nº de requerimiento del servicio")
                dias = st.text_input("⏳ Plazo del servicio (días)")
            with col2:
                oferta = st.text_input("💰 Monto total ofertado (S/)", placeholder="Ej. 1500.00")
                mes_manual = st.selectbox("📅 Mes del documento", list(meses.values()))

            # ✅ NUEVO: correo digitado (no viene del Excel)
            correo = st.text_input(
                "📧 Correo (se digita manualmente)",
                placeholder="Ej. proveedor@gmail.com"
            ).strip()

    # =========================
    # NOMBRE DEL ARCHIVO
    # =========================
    with st.container():
        nombre_empleado = st.text_input("📄 Tu nombre para el archivo generado").strip()

    # =========================
    # GENERAR DOCUMENTO
    # =========================
    if st.button("📄 Generar Documento de Requerimiento"):
        campos = {
            "Proveedor": nombre_proveedor,
            "DNI": dni,
            "RUC": ruc,
            "Servicio": servicio,
            "Días": dias,
            "Oferta": oferta,
            "Nº Servicio": n_servicio,
            "Mes": mes_manual,
            "Correo": correo,
            "Nombre": nombre_empleado
        }

        errores = [
            k for k, v in campos.items()
            if str(v).strip() == "" or v == "Selecciona un proveedor"
        ]

        if errores:
            st.error("❌ Corrige los siguientes campos: " + ", ".join(errores))
            return

        # ✅ Contexto para DOCX ({{cci}} y {{correo}})
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
            "mes": mes_manual,
            "banco": banco,
            "cci": cci,        # {{cci}}
            "correo": correo,  # {{correo}}
        }

        plantilla = "plantilla/requerimientos_unificada.docx"
        doc = DocxTemplate(plantilla)
        doc.render(context)

        nombre_archivo = f"{nombre_empleado.upper()}_REQUERIMIENTO_{n_servicio}.docx"
        doc.save(nombre_archivo)

        with open(nombre_archivo, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
            href = (
                f'<a href="data:application/octet-stream;base64,{b64}" '
                f'download="{nombre_archivo}">📥 Descargar Documento de Requerimiento</a>'
            )
            st.markdown(href, unsafe_allow_html=True)

        os.remove(nombre_archivo)
        st.success("✅ Documento generado correctamente.")
