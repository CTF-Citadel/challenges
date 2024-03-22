FROM python:3.8-slim
ARG FLAG
ENV FLAG=${FLAG}
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN python3 /app/encryption.py

CMD ["python", "service.py"]