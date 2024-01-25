FROM ubuntu

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    tor

WORKDIR /app

COPY . /app

RUN echo 'HiddenServiceDir /var/lib/tor/hidden_service/' >> /etc/tor/torrc
RUN echo 'HiddenServicePort 80 127.0.0.1:80' >> /etc/tor/torrc

RUN service tor restart

CMD ["bash"]
