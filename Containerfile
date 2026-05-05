FROM python:3.13-slim

RUN useradd --create-home app

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./src/

USER app

EXPOSE 8080

WORKDIR /app/src
CMD ["python", "-m", "server"]
