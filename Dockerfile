FROM fabianbusch/zamia-asr-base:latest

RUN apt-get install -y python-pip && pip install flask

WORKDIR /home/

COPY ./flask_server.py ./
COPY ./kaldi_decode_wav.py ./

RUN mkdir tmp

EXPOSE 5000

CMD export FLASK_APP=flask_server.py && flask run --host=0.0.0.0