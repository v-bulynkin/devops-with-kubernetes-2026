FROM python:3.12-alpine

ENV PYTHONUNBUFFERED=1
ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app

RUN adduser -D appuser && \
    python -m venv /opt/venv && \
    chown -R appuser:appuser /opt/venv

USER appuser

# Copy only requirements.txt to prevent package installation every time after app.py changed
COPY --chown=appuser:appuser requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser app.py .

CMD ["gunicorn", "--workers", "1", "--bind", "0.0.0.0:5000", "app:app"]
