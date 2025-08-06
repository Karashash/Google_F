# Қарашаш
## DOCX Translator - Google API

Streamlit
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export GOOGLE_APPLICATION_CREDENTIALS="$PWD/gt-key.json"  
export GCP_PROJECT=<project-id>
streamlit run streamlit_app.py
```

Docker
http://localhost:8501
```bash
docker run -p 8501:8501 \
  -v "$(pwd)/gt-key.json:/gcp/key.json:ro" \
  -e GOOGLE_APPLICATION_CREDENTIALS=/gcp/key.json \
  -e GCP_PROJECT=<project-id> \
  docx-translator
```
