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
./drums_trap.py inputfilename outputfilename mix [ --beats pathtobeatfile breakparts measures ] [ --samples your own samples directory ] 
```
Wrote and tested with mp3 files, however the following formats should also work:
wav, au, ogg, m4a, mp4.

#Acknowledgements
- A lot of the code is from the echonest library examples
- This [reddit thread](http://www.reddit.com/r/hiphopheads/comments/1vxdag/guys_i_need_a_favor/)
- Samples were from this [reddit thread](http://www.reddit.com/r/DJs/comments/1vhaez/sample_pack_not_sure_if_anyone_is_interested_but/)
- Beat loops were from [here](http://www.stayonbeat.com/2013/11/16/free-trap-drum-loops/)

