FROM ubuntu:latest

RUN apt-get update && \
    apt-get install -y steghide python3 uuid-runtime && \
    rm -rf /var/lib/apt/lists/*

COPY wood.jpg /app/wood.jpg
COPY generate_flag.sh /app/generate_flag.sh

WORKDIR /app

RUN chmod +x generate_flag.sh

EXPOSE 80

CMD ["./generate_flag.sh"]
