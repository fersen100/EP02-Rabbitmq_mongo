FROM python:3-slim

ADD . /todo
WORKDIR /todo

RUN pip3 install -r requirements.txt
RUN pip install pymongo
RUN pip install requests
