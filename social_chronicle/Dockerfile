FROM python:latest

WORKDIR /app

COPY . .

RUN pip install --upgrade pip setuptools

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "bot.py"]
