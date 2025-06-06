FROM python:3.11-slim

# эт установка зависимостей
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

# установка pip и копирование
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# копирую всеееее
COPY . .

# запускаю
CMD ["fastapi", "dev", "app/main.py"]
