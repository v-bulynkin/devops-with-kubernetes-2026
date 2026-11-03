# Stage 1: Build stage
FROM python:3.12-alpine AS builder

# Install build dependencies
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

WORKDIR /build

# Install dependencies into a local directory
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final runtime stage
FROM python:3.12-alpine

# Install runtime dependency for psycopg2
RUN apk add --no-cache libpq

WORKDIR /app

# Copy only the installed python packages from the builder stage
COPY --from=builder /root/.local /root/.local
# Copy application code
COPY . .

# Ensure the local bin directory is in the PATH
ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000

CMD ["python", "app.py"]
