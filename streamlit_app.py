import os
from io import BytesIO
import tempfile

import streamlit as st
from google.api_core.exceptions import GoogleAPIError  
from app.translator_core import translate_docx

def setup_gcp_from_secrets():
    gcp_cfg = st.secrets.get("gcp")
    if not gcp_cfg:
        return 

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".json") as f:
        f.write(gcp_cfg["key"])
        cred_path = f.name

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = cred_path
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", gcp_cfg["project"])

setup_gcp_from_secrets()


st.set_page_config(page_title="DOCX Translator")
st.title("DOCX Translator - Google API")

uploaded = st.file_uploader("Загрузите .docx", type=["docx"])
target_lang = st.selectbox(
    "Язык перевода",
    options=[("kk", "Қазақша"), ("ru", "Русский")],
    format_func=lambda x: x[1],
)[0]

if st.button("Перевести") and uploaded:
    try:
        with st.spinner("Переводим…"):
            result: BytesIO = translate_docx(
                uploaded,
                target_lang=target_lang,
                gcp_project=os.getenv("GOOGLE_CLOUD_PROJECT"),
            )

        st.success("Готово")
        st.download_button(
            "Скачать",
            data=result,
            file_name=f"translated_{target_lang}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )

    except GoogleAPIError as e:
        st.error("Ошибка:\n\n" + str(e.message))
    except Exception as e:
        st.exception(e)
