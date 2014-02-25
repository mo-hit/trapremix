#!/usr/bin/env python
# encoding: utf=8
"""
trapify.py

Add drums to a song.

At the moment, only works with songs in 4, and endings are rough, 

By Mohit Gupta, 2014-02-21.

"""
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



# usage="""
# Usage:
#     python drums.py <inputfilename> <outputfilename> <drum intensity> [--samples <samplesdir>] [--beat <beatfile> <beatsinbreak> <barsinbreak>]
#
# Example:
#     python drums.py HereComesTheSun.mp3 HereComeTheDrums.mp3 0.5
#
# """

parser = argparse.ArgumentParser(description="Turn boring sound files into \
                                 Real Trap Shit.")
parser.add_argument("inputfile", metavar='inputfile',
                    help="The input filename")
parser.add_argument("outputfile", metavar='outputfile',
                    help="The output filename")
parser.add_argument("drumintensity", metavar='drumintensity',
                    help="Intensity of drums in the final mix")
parser.add_argument("--samples", nargs='?',
                    help="The directory to look in \
                    for samples.  Defaults to \"samples\"")
parser.add_argument("--beats", nargs='+',
                    help="The directory to look in \
                    for beats.  Defaults to \"beats\"")


def mono_to_stereo(audio_data):
    data = audio_data.data.flatten().tolist()
    new_data = numpy.array((data,data))
    audio_data.data = new_data.swapaxes(0,1)
    audio_data.numChannels = 2
    return audio_data

def split_break(breakfile,n):
    drum_data = []
    start = 0
    for i in range(n):
        start = int((len(breakfile) * (i))/n)
        end = int((len(breakfile) * (i+1))/n)
        ndarray = breakfile.data[start:end]
        new_data = audio.AudioData(ndarray=ndarray,
                                    sampleRate=breakfile.sampleRate,
                                    numChannels=breakfile.numChannels)
        drum_data.append(new_data)
    return drum_data

def extension(file):
    ext = os.path.splitext(file)[-1].lower()
    return ext   

def pickSample(L):
    # using a weighted algorithm to make the numbers at the top of the list more likely to be used (GA algorithm)
    bias = 3
    n = len(L)
    rand = int(n * (bias - math.sqrt(bias*bias - 4.0*(bias-1.0)*random.random())) / 2.0 / (bias-1))

    sample = L.pop(rand)
    # we have the sample we're going to use, take it from (presumably the top) of the list and append it to the end
    L.append(sample)
    return sample

def parse():
    if args.samples:
        samples_dir = args.samples
    else:
        samples_dir = 'samples/'

    if args.beats:
        beats_args = args.beats
        beats_file = beats_args[0]
    else:
        beats_args = ['beats/', 64, 4]
        beats_file = os.path.join(str(beats_args[0]), random.choice(os.listdir(beats_args[0])))

    
    break_parts = int(beats_args[1])
    measures = int(beats_args[2])
    mix = args.drumintensity
    parse_data = [inputfile,outputfile,beats_file,break_parts,measures,mix,samples_dir]  

    return parse_data


def main(input_filename, output_filename, break_filename, break_parts,
            measures, mix, samples_dir):
    print break_filename
    audiofile = audio.LocalAudioFile(input_filename)
    sample_rate = audiofile.sampleRate
    breakfile = audio.LocalAudioFile(break_filename)
    if breakfile.numChannels == 1:
        breakfile = mono_to_stereo(breakfile)
    num_channels = audiofile.numChannels
    drum_data = split_break(breakfile,break_parts)
    hits_per_beat = int(break_parts/(4 * measures))
    bars = audiofile.analysis.bars
    out_shape = (len(audiofile)+100000,num_channels)
    out = audio.AudioData(shape=out_shape, sampleRate=sample_rate,
                            numChannels=num_channels)
    if not bars:
        print "Didn't find any bars in this analysis!"
        print "No output."
        sys.exit(-1)
    for bar in bars[:-1]:
        beats = bar.children()
        for i in range(len(beats)):
            try:
                break_index = ((bar.local_context()[0] %\
                                measures) * 4) + (i % 4)
            except ValueError:
                break_index = i % 4
            tats = range((break_index) * hits_per_beat,
                        (break_index + 1) * hits_per_beat)
            drum_samps = sum([len(drum_data[x]) for x in tats])
            beat_samps = len(audiofile[beats[i]])
            beat_shape = (beat_samps,num_channels)
            tat_shape = (float(beat_samps/hits_per_beat),num_channels)
            beat_data= audio.AudioData(shape=beat_shape,
                                        sampleRate=sample_rate,
                                        numChannels=num_channels)
            for j in tats:
                tat_data= audio.AudioData(shape=tat_shape,
                                            sampleRate=sample_rate,
                                            numChannels=num_channels)
                if drum_samps > beat_samps/hits_per_beat:
                    # truncate drum hits to fit beat length
                    tat_data.data = drum_data[j].data[:len(tat_data)]
                elif drum_samps < beat_samps/hits_per_beat:
                    # space out drum hits to fit beat length
                    #temp_data = add_fade_out(drum_data[j])
                    tat_data.append(drum_data[j])
                tat_data.endindex = len(tat_data)
                beat_data.append(tat_data)
                del(tat_data)
            # account for rounding errors
            beat_data.endindex = len(beat_data)
            mixed_beat = audio.mix(beat_data, audiofile[beats[i]], mix=mix)
            del(beat_data)
            out.append(mixed_beat)

    

            
    finale = bars[-1].start + bars[-1].duration
    last = audio.AudioQuantum(audiofile.analysis.bars[-1].start,
                            audiofile.analysis.duration - 
                              audiofile.analysis.bars[-1].start)
    last_data = audio.getpieces(audiofile,[last])
    out.append(last_data)
    samples_avail = os.listdir(samples_dir)

    #throw down some classic trap samples
    #the outfile should be the same length as the output file, so just go through that file instead
    for section in audiofile.analysis.sections[1:]:

        overlay_sound_file = pickSample(samples_avail)
        soundpath = os.path.join(str(samples_dir), overlay_sound_file)
        print soundpath
        sample = audio.LocalAudioFile(soundpath)

        # Mix the audio
        volume = 0.9
        pan = 0
        startsample = int(section.start * out.sampleRate)
        seg = sample[0:]
        seg.data *= (volume-(pan*volume), volume+(pan*volume)) # pan + volume
        if out.data.shape[0] - startsample > seg.data.shape[0]:
            out.data[startsample:startsample+len(seg.data)] += seg.data[0:]

    out.encode(output_filename);


if __name__=='__main__':
    args = parser.parse_args()
    inputfile = args.inputfile
    outputfile = args.outputfile
    parse_data = parse()
    main(*parse_data)
