FROM ubuntu:18.04
ENV PYTHONUNBUFFERED 1
RUN apt-get -y update
RUN apt-get -y install git python3-pip python3-dev postgresql-client
RUN mkdir /code
WORKDIR /code
ADD setup.py /code/
RUN pip3 install --upgrade pip
RUN pip3 install -e .[dev,test]
RUN pip3 install tox
ADD . /code/
