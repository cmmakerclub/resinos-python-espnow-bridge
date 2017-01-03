FROM resin/raspberrypi-python:latest
#ENV INITSYSTEM on

# Defines our working directory in container
WORKDIR /usr/src/app

# Copy requirements.txt first for better cache on later pushes
COPY ./requirements.txt /requirements.txt
