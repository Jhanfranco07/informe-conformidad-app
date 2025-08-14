import streamlit as st
from modulos import conformidad, requerimiento

st.set_page_config(page_title="Generador de Documentos", page_icon="📄")

st.title("📑 Generador de Documentos")
st.markdown("---")

opcion = st.sidebar.radio("Selecciona un módulo:", [
    "Informe de Conformidad y Requerimiento",
    "Documento de Requerimiento"
])

if opcion == "Informe Unificado de Conformidad":
    conformidad.mostrar()
elif opcion == "Documento de Requerimiento":
    requerimiento.mostrar()




