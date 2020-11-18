FROM python:3.8-slim

COPY . /
RUN cat /etc/os-release
RUN apt-get update
RUN pip install -r requirements.txt
RUN apt-get install python3-sphinx -y