trapremix
=========

Adds hip-hop beats and samples commonly found in southern hip-hop to songs. Very rough script as it is my first time using python. Drum syncing can be off sometimes, looking for ways to improve that. Feel free to do whatever you want with it


#Requirements

Requires the Echonest python library to work. If you have pip, Run:
```
sudo pip install remix
```

Otherwise see: http://echonest.github.io/remix/

#Use
Clone the folder and navigate to it. 
Run:
```
./drums_trap.py inputfilename outputfilename mix [ --beats pathtobeatfile breakparts measures ] [ --samples samplesdirectory ] 
```
- pathtobeatfile being a specific beat file you would like to use, otherwise it will use a random loop from the ones provided.
- breakparts are the subdivision of the hits in the drum loop (64 for all the ones provided)
- measures are the number of measures in the drum loop (4 for all the ones provided)
- samplesdirectory is if you want to use your own custom samples

Wrote and tested with mp3 files, however the following formats should also work:
wav, au, ogg, m4a, mp4. I left my API key in the code if you want to try it out. If you want to use it for your own purposes please create your own Echonest developer account and use your own key. 
I left the run_samples.py in the project to run through samples and make sure they are compatible with the echonest library (some of mine failed)

#Acknowledgements
- A lot of the code is from the echonest library examples
- This [reddit thread](http://www.reddit.com/r/hiphopheads/comments/1vxdag/guys_i_need_a_favor/)
- Samples were from this [reddit thread](http://www.reddit.com/r/DJs/comments/1vhaez/sample_pack_not_sure_if_anyone_is_interested_but/)
- Beat loops were from [here](http://www.stayonbeat.com/2013/11/16/free-trap-drum-loops/)

