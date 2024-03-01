FROM python:3.11-slim

WORKDIR /app

RUN apt update && \
    apt install -y git zip

COPY requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY templates/ ./templates
COPY samples/ ./samples
COPY service.py \
entrypoint.sh \
./

RUN chmod +x entrypoint.sh

ARG FLAG
ENV FLAG=${FLAG}

EXPOSE 1337

CMD ["./entrypoint.sh"]
