FROM resin/raspberrypi-python:latest
#ENV INITSYSTEM on

# Defines our working directory in container
WORKDIR /usr/src/app

# Copy requirements.txt first for better cache on later pushes
COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

# switch on systemd init system in container
ENV INITSYSTEM on

COPY . ./
ADD fauxmo.py /usr/src/app

# main.py will run when container starts up on the device
CMD ["python","/usr/src/app/fauxmo.py"]
