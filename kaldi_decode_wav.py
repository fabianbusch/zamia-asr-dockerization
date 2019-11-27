#!/usr/bin/env python2
# -*- coding: utf-8 -*-

#
# Copyright 2016, 2017, 2018, 2019 Guenter Bartsch
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# THIS CODE IS PROVIDED *AS IS* BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, EITHER EXPRESS OR IMPLIED, INCLUDING WITHOUT LIMITATION ANY IMPLIED
# WARRANTIES OR CONDITIONS OF TITLE, FITNESS FOR A PARTICULAR PURPOSE,
# MERCHANTABLITY OR NON-INFRINGEMENT.
# See the Apache 2 License for the specific language governing permissions and
# limitations under the License.
#

#
# py-kaldiasr demonstration program
#
# decode wav file(s) using an nnet3 chain model
#

import sys
import os
import wave
import struct
import logging
import numpy as np
import json

from time import time
from optparse import OptionParser
from kaldiasr.nnet3 import KaldiNNet3OnlineModel, KaldiNNet3OnlineDecoder

# Changed
DEFAULT_MODELDIR = '/opt/kaldi/model/kaldi-generic-en-tdnn_f'

parser = OptionParser("usage: %prog [options] foo.wav [bar.wav ...]")

parser.add_option("-m", "--model-dir", dest="modeldir", type="str", default=DEFAULT_MODELDIR,
                  help="model directory (default: %s)" % DEFAULT_MODELDIR)
parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                  help="enable debug output")

(options, args) = parser.parse_args()

if options.verbose:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

if len(args) < 1:
    parser.print_usage()
    sys.exit(1)

logging.debug('%s loading model...' % options.modeldir)
time_start = time()
kaldi_model = KaldiNNet3OnlineModel(
    options.modeldir, acoustic_scale=1.0, beam=7.0, frame_subsampling_factor=3)
logging.debug('%s loading model... done, took %fs.' %
              (options.modeldir, time()-time_start))

logging.debug('%s creating decoder...' % options.modeldir)
time_start = time()
decoder = KaldiNNet3OnlineDecoder(kaldi_model)
logging.debug('%s creating decoder... done, took %fs.' %
              (options.modeldir, time()-time_start))

for wavfile in args:

    time_start = time()

    if decoder.decode_wav_file(wavfile):
        s, l = decoder.get_decoded_string()

        logging.debug("%s decoding took %8.2fs, likelyhood: %f" %
                      (wavfile, time() - time_start, l))
        output = { 
            "utterance": s.encode('utf-8', 'ignore'), 
            "likelyhood": l 
        }
        print(json.dumps(output))

    else:
        logging.error("decoding of %s failed." % wavfile)
