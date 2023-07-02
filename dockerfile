# syntax=docker/dockerfile:1

FROM python:3.8-slim

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

WORKDIR /app/app

CMD ["python", "app.py"]

# sudo docker build --tag network_interface .
# sudo docker run -p 5000:5000 network_interface