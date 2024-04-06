# Elysium Realms

> [!NOTE]
>
> This Web-Challenge is about finding a curcial vulnerabiltiy inside a Web-Game-Application.

## Challenge Development

To automate the challenge I first setup a `docker-compose.yml` file which exports the necessary ports and imports the flag via an ARG var. <br/>
```yml
version: '3.9'

services:
  flask:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - FLAG=$FLAG
    ports:
      - "80:5000"
```

The `Dockerfile` sets up a python environment to host the application and import the flag as environment variable. <br/>
```docker
FROM python:latest

ARG FLAG
ENV FLAG=${FLAG}

WORKDIR .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "service.py"]
```

