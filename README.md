# badappleamongus

Produces Bad Apple memes. White space is replaced with custom images which is inserted in a quadtree
structure. The program is set up cycle smoothly through a folder of images once per beat, at the
current song beat of 138 BPM.

The default images are the classic modern piece known as "amogus twerk". They can be replaced by the user
for any frames of their choosing in the GIFFrames folder.

### Examples
*Example frame produced:*

![hqdefault](https://i.imgur.com/AORXQo3.png)

[Link to example video produced from this program](https://youtu.be/HY5lOaCbdmY)

[Another example video here (mild epilepsy warning)](https://youtu.be/JjHOyfuYi_g)


### Setup
To use this script you will need Python 3 installed as well as:
- numpy and cv2, which can be installed by pip
- ffmpeg, including making it an environment variable, instructions 
can be found [here](https://www.wikihow.com/Install-FFmpeg-on-Windows)

### Running
Once you have everything, download this repo. The two things you have to
concern yourself with is the Frames folder and master.py

Frames is where the output images and video will be placed, master.py will
run the script. The output video's name is randomized to avoid collisions,
so sorting the folder time created is probably the best way to find the video.

Once you run master.py, it will ask you if you want to outline the black
tiles produced with a custom color. Make a choice and then the script will
start

### Notes
It is suggested you refrain from touching or moving anything else, on the
off chance something breaks and you have to redownload everything. 

The exception is the GIFFrames folder. The script should support any
frames extracted there, so you can replace the original frames with whatever
you like. Make sure that you have only INDIVIDUAL frames there, the script
will not work with a raw GIF.

Also something to note is that the program will produce images with
a transparency channel. However, this transparency will not be apparent
in the produced video, so any effect is limited to the raw frames.
