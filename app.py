import streamlit as st
from docxtpl import DocxTemplate
from datetime import datetime
import pandas as pd
import base64
import os

# Configuración visual
st.set_page_config(page_title="Informe Unificado", page_icon="📄", layout="centered")
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .block-container { padding-top: 2rem; }
    .stButton>button { background-color: #0d6efd; color: white; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# Traducción de meses
meses = {
    "January": "enero", "February": "febrero", "March": "marzo",
    "April": "abril", "May": "mayo", "June": "junio",
    "July": "julio", "August": "agosto", "September": "septiembre",
    "October": "octubre", "November": "noviembre", "December": "diciembre"
}

# Datos estáticos
data = {
    "RUC": [
        "10754913253", "10607555589", "10445407297", "1010665091", "10093876160",
        "10735782741", "10727949629", "10755833504", "10752815181", "10727584418",
        "10721544767", "10474310464"
    ],
    "NOMBRE Y APELLIDOS": [
        "GRECIA MARIA VARGAS SALAZAR", "LUZ MERCEDES HUAMAN EVANGELISTA", "DANIEL ESTEBAN SILVA ROMAN",
        "MILAGROS HERMELINDA GONZALES FLORES", "JUAN DAVID CAMPOS CANALES", "YOSELIN LEONELA GOMEZ VEGA",
        "FIORELLA DESSIRE TINOCO VEGA", "NICOLE FERNANDA TINOCO PANEZ", "JHAN FRANCO PEREZ ANCIETA",
        "DANIELA MILAGRITOS QUISPE GUERRA", "LIZET JANINE QUIROZ CARDENAS", "ABIGAIL KAITIZA LA TORRE REYES"
    ],
    "SERVICIO": [
        "SERVICIO DE ASISTENCIA TECNICA EN GESTIÓN DE PROCESOS ADMINISTRATIVOS",
        "SERVICIO DE ANALISIS DE INFORMACION EMPRESARIAL",
        "SERVICIO DE ORIENTACIÓN A LOS CIUDADANOS PARA LA ATENCION EN PLATAFORMA",
        "SERVICIO DE ASISTENTE ADMINISTRATIVO",
        "SERVICIO DE AUXILIAR ADMINISTRATIVO",
        "SERVICIO DE ASISTENCIA EN TEMAS DE ARQUITECTURA",
        "SERVICIO DE REVISION, ANALISIS Y VERIFICACION DE EXPEDIENTES",
        "SERVICIO DE INSPECTOR COMERCIAL",
        "SERVICIO DE MEJORA DE PLANEAMIENTO INFORMÁTICO",
        "SERVICIO DE ASESORIA LEGAL",
        "SERVICIO DE ANALISIS ORGANIZACIONAL",
        "SERVICIO DE ANALISIS DE PROCESOS ADMINISTRATIVOS EN GESTION DOCUMENTAL"
    ]
}
df = pd.DataFrame(data)

# Título
st.title("📄 Generador de Informe Único de Conformidad + Actividades")

# FORMULARIO
numero = st.text_input("Nº de Informe de Conformidad", help="Número correlativo (ej. 1)")
numero_sustento = st.text_input("Nº de Informe de Actividades", help="Número correlativo de sustento")
gerencia = st.selectbox("Gerencia solicitante", [
    "Seleccione una opción",
    "GERENCIA DE LICENCIAS Y DESARROLLO ECONÓMICO",
    "GERENCIA DE DESARROLLO URBANO"
])

nombre_proveedor = st.selectbox("Selecciona el proveedor", ["Selecciona un proveedor"] + df["NOMBRE Y APELLIDOS"].tolist())
ruc = concepto = nombre_abrev = dni = ""

if nombre_proveedor != "Selecciona un proveedor":
    proveedor_info = df[df["NOMBRE Y APELLIDOS"] == nombre_proveedor].iloc[0]
    ruc = proveedor_info["RUC"]
    concepto = proveedor_info["SERVICIO"]

    st.text_input("RUC", value=ruc, disabled=True)
    st.text_area("Concepto", value=concepto, disabled=True, height=80)

    partes = nombre_proveedor.strip().split()
    nombre_abrev = "".join([p[0] for p in partes[:4]]).upper()

    st.text_input("Nombre abreviado del proveedor", value=nombre_abrev, disabled=True)

    if ruc.isdigit() and len(ruc) == 11 and ruc.startswith("10"):
        dni = ruc[2:-1]

orden_servicio = st.text_input("Orden de Servicio")
fecha_orden = st.date_input("Fecha de la Orden de Servicio")
plazo = st.text_input("Plazo del servicio (días)")
fecha_inicio = st.date_input("Inicio del servicio")
fecha_termino = st.date_input("Término del servicio")
fecha_entrega = st.date_input("Fecha de entrega del servicio")
referencia = st.selectbox("Referencia del entregable", ["", "1", "2", "3", "4"])
fecha = st.date_input("Fecha de emisión del informe", datetime.today())
actividades = st.text_area("Detalle de las actividades realizadas", height=200)
nombre_empleado = st.text_input("Tu nombre para el archivo generado")

if st.button("📝 Generar Informe Unificado"):
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
            "fecha": fecha_formateada,
            "nombre_abrev": nombre_abrev,
            "dni": dni,
            "actividades": actividades
        }

        # Renderiza solo UNA plantilla
        plantilla = "Plantilla_unificada.docx"
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

