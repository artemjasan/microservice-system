FROM docker.io/python:3.11-alpine

# Set environment variables (adjust as needed)
ENV PYTHONUNBUFFERED 1

# Create a directory for your app and set it as the working directory
RUN mkdir /app

# Copy your project files to the container
COPY ./microservices/user_service/ /app
COPY ./pyproject.toml /app
COPY ./poetry.lock /app


# Install system-level dependencies
RUN apk add --no-cache build-base libffi-dev bash
RUN apk add --no-cache netcat-openbsd

WORKDIR /app

# Upgrade pip and install your Python dependencies
RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry config virtualenvs.create false && poetry install

EXPOSE 8080

CMD uvicorn main:make_app --factory --host 0.0.0.0 --port=8080
