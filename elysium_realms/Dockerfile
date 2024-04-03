FROM python:latest

ARG FLAG
ENV FLAG=${FLAG}

WORKDIR .

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "service.py"]