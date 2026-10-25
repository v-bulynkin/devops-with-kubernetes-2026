FROM python:3.12-alpine

ENV PATH="/opt/venv/bin:$PATH"
WORKDIR /app

RUN adduser -D appuser && \
    python -m venv /opt/venv && \
    chown -R appuser:appuser /opt/venv

USER appuser

COPY --chown=appuser:appuser requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY --chown=appuser:appuser app.py .

EXPOSE 5000

CMD ["python", "app.py"]
