FROM python:3.12-alpine

WORKDIR /app

# Install system dependencies for psycopg2
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev \
    && pip install --no-cache-dir flask flask-sqlalchemy psycopg2

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
