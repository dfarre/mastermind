FROM python:3.6-jessie
ENV PYTHONUNBUFFERED 1
RUN apt-get -y update
RUN apt-get -y install postgresql-client
RUN mkdir /code
WORKDIR /code
ADD setup.py /code/
RUN pip install --upgrade pip
RUN pip install --upgrade -e .[dev,test]
RUN pip install tox
ADD . /code/
