# Pull base image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PORT=8080
# Set work directory
WORKDIR /app
# Install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
# Copy app folder
COPY app/ /app/
