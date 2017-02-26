FROM debian:latest

RUN apt-get update -y && apt-get -y install python python-pip build-essential python-dev

ADD . /web
RUN pip install 3to2
RUN pip install -r /web/requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "/web/run.py"]
