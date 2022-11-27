FROM rsolano/debian-vnc-python

COPY . /app

WORKDIR /app

RUN apt-get update \
    && apt-get install -y zip \
    && pip3 install pygame \
    && unzip pplay-PPlay_v1.1.zip  \
    && mv ./pplay-PPlay_v1.1/PPlay /usr/lib/python3/dist-packages
