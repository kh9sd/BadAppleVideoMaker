# badappleamongus

TODO: description of what this does

### Example
![hqdefault](https://user-images.githubusercontent.com/41244296/147705872-c63355dd-8fbb-41a2-b2a8-09aefaa19d4c.jpg)

[Link to example video produced from this program](https://youtu.be/sa2PF5ubspY)


### Setup
To use this script you will need Python 3 installed as well as:
- numpy and cv2, which can be installed by pip
- ffmpeg, all the way up to making it an environment variable, instructions 
can be found [here](https://www.wikihow.com/Install-FFmpeg-on-Windows)

### Running
Once you have everything, download this repo. The two things you have to
concern yourself with is the Frames folder and master.py

Frames is where the output images and video will be placed, master.py will
run the script

Once you run master.py, it will ask you if you want to outline the black
tiles produced with a custom color. Make a choice and then the script will
start

### Notes
It is suggested you refrain from touching or moving anything else, on the
off chance something breaks and you have to redownload everything. 

The exception is the GIFFrames folder. The script should support any
frames extracted there, so you can replace the original frames with whatever
you like. Make sure that you have INDIVIDUAL frames there, the script
will not work with a raw GIF.

Also something to note is that the program will produce images with
a transparency channel. However, I very much doubt this transparency is 
relevant in the produced video, so any effect is limited to the raw pngs.
