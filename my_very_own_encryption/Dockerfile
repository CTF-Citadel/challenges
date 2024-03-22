FROM python:3.8-slim
ARG FLAG
ENV FLAG=${FLAG}
WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x initiate.sh

CMD ["./initiate.sh"]