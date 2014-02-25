#!/usr/bin/env python

import numpy
import sys
import time
import os
import argparse
import random
import math

import echonest.remix.audio as audio
from pyechonest import config
config.ECHO_NEST_API_KEY="WAGGM2UYKJZXOGNZS"


print 'start'
for filename in os.listdir('TrapKit'): 
	print 'inhere'
	print filename
	audiofile = audio.LocalAudioFile('TrapKit/'+filename)
	
