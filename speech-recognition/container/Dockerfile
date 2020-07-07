FROM python:3.6-slim-jessie
MAINTAINER fanzhihai@inspur.com

RUN mkdir /speech-recognition

COPY speech-recognition /speech-recognition

WORKDIR /speech-recognition
RUN apt update && apt install -y portaudio19-dev gcc 
RUN apt install -y libffi-dev make
RUN pip install --upgrade pip
RUN pip3 install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com pyaudio cffi greenlet pycparser wheel gevent six websocket websocket-client flask

EXPOSE 8000

ENV FLASK_APP speech-recognition.py
ENV PYTHONUNBUFFERED 0

CMD [ "python3", "speech-recognition.py", "&" ]
