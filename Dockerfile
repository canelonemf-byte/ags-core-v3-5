# RECONSTRUIDO en v3.5 (el original de Drive no era legible). No probado: Docker no disponible.
FROM python:3.12-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir -r requirements.txt
COPY app ./app
ENV AGSGPT_DATA_DIR=/srv/data
WORKDIR /srv/app
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
