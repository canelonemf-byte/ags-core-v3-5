# RECONSTRUIDO en v3.5 (el original de Drive no era legible). No probado: Docker no disponible.
FROM python:3.12-slim
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu \
 && pip install --no-cache-dir -r requirements.txt
COPY app ./app
COPY knowledge ./knowledge
COPY projects.json ./projects.json
ENV AGSGPT_DATA_DIR=/srv/data AGS_REPORTS_DIR=/srv/reports
WORKDIR /srv/app
EXPOSE 8000
# autopilot: docker run ... python -m app.autopilot  (WORKDIR /srv)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
