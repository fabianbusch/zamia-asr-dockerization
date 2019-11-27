FROM debian:10

RUN apt-get update && apt-get install -y apt-transport-https wget gnupg

RUN echo "deb http://goofy.zamia.org/repo-ai/debian/stretch/amd64/ ./" >/etc/apt/sources.list.d/zamia-ai.list

RUN wget -qO - http://goofy.zamia.org/repo-ai/debian/stretch/amd64/bofh.asc | apt-key add -

RUN apt-get update && apt-get install -y kaldi-chain-zamia-speech-de kaldi-chain-zamia-speech-en python-kaldiasr python-nltools pulseaudio-utils pulseaudio