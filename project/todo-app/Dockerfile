FROM python:3.12-alpine

WORKDIR /app

COPY app.py requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ENV PORT=5000

CMD ["python", "app.py"]