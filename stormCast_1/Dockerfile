# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the confidential.zip file into the container
COPY confidential.zip /app/confidential.zip

# Make port 80 available to the world outside this container
EXPOSE 8000

# Define environment variable
ARG FLAG
ENV FLAG=${FLAG}

# Run main.py when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
