FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-server-dev-all build-essential && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

CMD ["python", "run.py"]
