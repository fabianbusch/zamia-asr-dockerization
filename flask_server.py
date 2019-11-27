#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request
from werkzeug.utils import secure_filename
import subprocess
import json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Example Request: curl -X POST -F audio=@"path/to/file.wav" "http://127.0.0.1:5000/transcribe"


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
                "python kaldi_decode_wav.py ./tmp/temp.wav", shell=True)
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
