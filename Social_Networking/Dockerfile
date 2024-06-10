# Use the official Python image from the Docker Hub
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /usr/src/app

# Install dependencies
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project into the Docker image
COPY . /usr/src/app/

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
