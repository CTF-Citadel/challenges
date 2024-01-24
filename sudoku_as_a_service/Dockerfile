FROM python:3.8-slim

WORKDIR /app

COPY . /app

ARG FLAG
ENV FLAG=${FLAG}

CMD ["python", "service.py"]