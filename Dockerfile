FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Le commit est fourni au build : le depot git n'est pas copie dans l'image,
# mais le modele doit rester rattachable a un etat precis du code.
ARG GIT_COMMIT=inconnu
ENV AGROPREDICT_COMMIT=$GIT_COMMIT

# Le modele est construit ici, une fois pour toutes. L'application ne
# s'entraine jamais au demarrage : l'image contient un artefact fige.
RUN python data/pipelines/build_final_dataset.py \
    && python -m models.train_model

EXPOSE 8501

# Verification sans curl, absent de l'image slim.
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8501/_stcore/health')" || exit 1

CMD ["streamlit", "run", "streamlit_app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
