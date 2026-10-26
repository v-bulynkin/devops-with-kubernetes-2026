FROM python:3.12-alpine

WORKDIR /app

# May be useful for requests/ssl, but in alpine standard libs are usually enough for work
#RUN apk add --no-cache gcc musl-dev libffi-dev

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Directory for cache
RUN mkdir /data

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
