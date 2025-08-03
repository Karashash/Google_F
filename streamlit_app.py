import os
from io import BytesIO

import streamlit as st
from dotenv import load_dotenv

from app.translator_core import translate_docx

load_dotenv()

st.set_page_config(page_title="DOCX Translator")
st.title("DOCX Translator Google API")

gcp_project = st.text_input(
    "ID проекта",
    value=os.getenv("GCP_PROJECT", ""),
    placeholder="translator-467314",
)


uploaded = st.file_uploader("docx файл", type=["docx"])
target_lang = st.selectbox(
    "Язык перевода",
    options=[("kk", "Қазақша"), ("ru", "Орыс")],
    format_func=lambda x: x[1]
)[0]

if st.button("Перевести") and uploaded and gcp_project:
    with st.spinner("загрузка"):
        result_file: BytesIO = translate_docx(
            uploaded,
            target_lang=target_lang,
            gcp_project=gcp_project,
        )
    st.success("Готово")
    st.download_button(
        "Скачать",
        data=result_file,
        file_name=f"translated_{target_lang}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )
