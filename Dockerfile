

FROM debian:latest
MAINTAINER Regner Blok-Andersen <shadowdf@gmail.com>

ADD main.py /app/
ADD requirements.txt /app/

WORKDIR /app/

RUN apt-get update -qq \
&& apt-get upgrade -y -qq \
&& apt-get install -y -qq python-dev python-pip \
&& apt-get autoremove -y \
&& apt-get clean autoclean \
&& pip install -qU pip \
&& pip install -r requirements.txt

CMD python main.py