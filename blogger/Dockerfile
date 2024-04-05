FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

ARG FLAG

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

RUN echo "Here, grab your flag: TH{${FLAG}}" > /root/flag.txt

EXPOSE 5000

CMD ["python", "service.py"]
