#!/usr/bin/env python
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

from time import time
from optparse import OptionParser
from kaldiasr.nnet3 import KaldiNNet3OnlineModel, KaldiNNet3OnlineDecoder


class DecoderWorker:
    def __init__(self, modeldir='/opt/kaldi/model/kaldi-generic-de-tdnn_f'):
        logging.basicConfig(level=logging.DEBUG)
        logging.debug('%s loading model...' % modeldir)
        time_start = time()

        kaldi_model = KaldiNNet3OnlineModel(
            modeldir, acoustic_scale=1.0, beam=7.0, frame_subsampling_factor=3)
        logging.debug('%s loading model... done, took %fs.' %
                      (modeldir, time()-time_start))

        logging.debug('%s creating decoder...' % modeldir)
        time_start = time()
        self.decoder = KaldiNNet3OnlineDecoder(kaldi_model)
        logging.debug('%s creating decoder... done, took %fs.' %
                      (modeldir, time()-time_start))

    def decode(self, wavfile):
        time_start = time()
        logging.debug('starting to decode...')
        if self.decoder.decode_wav_file(wavfile):
            s, l = self.decoder.get_decoded_string()

            logging.debug("%s decoding took %8.2fs, likelyhood: %f" %
                          (wavfile, time() - time_start, l))
            print(s)
            return s

        else:
            logging.error("decoding of %s failed." % wavfile)
            return None
