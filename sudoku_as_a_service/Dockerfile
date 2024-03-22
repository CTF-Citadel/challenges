FROM python:3.8-slim
ARG FLAG
ENV FLAG=${FLAG}
WORKDIR /app

COPY . /app

CMD ["python3", "service.py"]