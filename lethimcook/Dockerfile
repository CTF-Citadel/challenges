# Use the official Python image as the base image
FROM python:3.9-slim
ARG FLAG
ENV FLAG=${FLAG}
# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask
RUN pip install flask

# Expose port 80
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "app.py"]
