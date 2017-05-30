"""
Corpus Loader

Roger D. Serwy

"""

import os
import pathlib
from collections import namedtuple
import numpy as np
import scipy.signal as sig
from scipy.io import wavfile

# speechfile
#   s - speech waveform
#   e - egg waveform
#   d - degg
#   fs - sample rate
#   file - file name for egg
#   name - key

speechfile = namedtuple('speechfile', 's, e, d, fs, file, name')

class APLAWD:
    def __init__(self, root):
        # walk the root, find all the .egg files
        _eggs = []
        _wavs = []
        for root, dirs, files in os.walk(root):
            _eggs.extend([(i.lower()[:-4],        # omit the .EGG extension
                           os.path.join(root, i), # full path to file
                           )
                          for i in files if i.upper().endswith('.EGG')])
            _wavs.extend([(i.lower()[:-4],        # omit the .WAV extension
                           os.path.join(root, i), # full path to file
                           )
                          for i in files if i.upper().endswith('.WAV')])
        _eggs.sort()
        self._egg_dict = dict(_eggs)
        self._wav_dict = dict(_wavs)
        self._eggs = _eggs

    def load(self, key):
        if isinstance(key, int):
            key = self._eggs[key][0]
        egg_filename = self._egg_dict[key]
        fs, w_egg = wavfile.read(egg_filename)
        w_egg = w_egg / -32768.0

        w_degg = sig.lfilter([1,-1], [1], w_egg)
        w_degg[0] = w_degg[1] # avoid initial spike

        wav_filename = self._wav_dict.get(key, None)
        if wav_filename:
            fs, w_speech = wavfile.read(wav_filename)
            w_speech = w_speech / 32768.0
        else:
            w_speech = 0 * w_egg

        return speechfile(w_speech, w_egg, w_degg, fs, egg_filename, key)

    def keys(self):
        return list(self._egg_dict.keys())

class APLAWD_Markings:
    def __init__(self, root):
        self.root = root

    def load(self, key):
        with open(os.path.join(self.root, key), 'r') as fid:
            m = np.array([int(i) for i in fid.readlines()])
        return m

    def keys(self):
        return os.listdir(self.root)


if __name__ == '__main__':
    markings = APLAWD_Markings('./aplawd_gci')
    key = 'aw15d4'
    m = markings.load(key)
    print('APLAWD waveform: %r' % key)
    print('GCIs at:')
    print(m)




