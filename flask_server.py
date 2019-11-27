#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from flask import Flask, request
from werkzeug.utils import secure_filename
import subprocess
import json
import os

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

ENGLISH_MODEL_DIR = '/opt/kaldi/model/kaldi-generic-en-tdnn_f'

GERMAN_MODEL_DIR = '/opt/kaldi/model/kaldi-generic-de-tdnn_f'

lang = os.getenv('TRANSCRIPTION_LANGUAGE')

if lang == 'EN':
    model_dir = ENGLISH_MODEL_DIR
elif lang == 'DE':
    model_dir = GERMAN_MODEL_DIR
else:
    print('No language specified. Using default (English) language for transcription.')
    model_dir = ENGLISH_MODEL_DIR

# Example Request: curl -X POST -F audio=@"path/to/file.wav" "http://127.0.0.1:5000/transcribe"

@app.after_request
def apply_caching(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

@app.route("/transcribe", methods=["GET", "POST"])
def handle_transcribe():
    if request.method == "GET":
        return {
            "status": "Ready, but use this API with POST. E.g. curl -X POST -F audio=@'path/to/file.wav' 'http://127.0.0.1:5000/transcribe'"
        }

    if request.files:
        try:
            audiofile = request.files["audio"]
            audiofile.save('./tmp/temp.wav')
        except:
            res = {
                "status": "Could not access the file. Did you send it in the form-field 'audio'?"
            }

        try:
            output = subprocess.check_output(
                "python2 kaldi_decode_wav.py ./tmp/temp.wav -m {0}".format(model_dir), shell=True)
            output = json.loads(output.encode('utf-8', 'ignore'))
            res = {
                "request_id": 1,
                "utterance": output['utterance'],
                "likelyhood": output['likelyhood'],
                "filename": secure_filename(audiofile.filename)
            }
        except:
            res = {
                "status": "Could not transcribe."
            }

    else:
        res = {
            "status": "No file provided."
        }

    return res
