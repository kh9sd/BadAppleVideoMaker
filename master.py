import cProfile
import numpy as np
import cv2
import random
import os
import subprocess
from quadtree import QuadTree
from string import ascii_lowercase, ascii_uppercase


def add_trans_layer(img):
    """
    Adds alpha channel to numpy array if BGR

    Parameters:
        img: numpy array

    Returns numpy array with added 4th channel in axis 2

    Raises ValueError if 2nd axis isn't 3 channel
    """
    if img.shape[2] != 3:
        raise ValueError("Image must be 3 channel to add alpha layer")

    trans_layer = np.tile(255, (img.shape[0], img.shape[1], 1)).astype(np.uint8)
    return np.concatenate((img, trans_layer), axis=2)


def folder_import(folder_path, mode=-1):
    """
    Imports images from folder into list of numpy arrays

    Parameters:
        folder_path: string, path to folder with JUST images in it
        mode: how the image files are read
            1 is cv2.IMREAD_COLOR
            0 is cv2.IMREAD_GRAYSCALE
            -1 is cv2.IMREAD_UNCHANGED

    Returns list of numpy arrays, which array being a BGRA image

    Raises ValueError if images aren't BGRA or BGR
    """
    images = []

    for file in os.listdir(folder_path):
        image = cv2.imread(os.path.join(folder_path, file), mode)

        if mode == 0:  # grayscale, shape is (x,y) not (x,y,z)
            image = add_trans_layer(np.concatenate([image[..., np.newaxis]]*3, axis=2))  # give new axis, dup 3 channels
        elif mode == 1:  # color
            image = add_trans_layer(image)
        elif mode == -1:  # unchanged
            if image.shape[2] == 3:  # if BGR for some reason not BGRA?
                image = add_trans_layer(image)
            elif image.shape[2] == 4:
                pass
            else:
                raise ValueError("Something fucked up, images not read as BGRA or BGR")

        # print(image.shape)
        # print(image)
        # cv2.imshow("shit", image)
        images.append(image)

    return images


def bpm_matching_index(cur_f, bps, fps):
    """
    Finds appropriate index to cycle through GIF array to match a given BPS and FPS
    
    Parameters:
        cur_f: current frame of the video
        bps: beats per second of the video
        fps: frames per second of the video
        
    Also takes length of global GIF_array
    
    Returns int
    """
    # seconds per frame
    spf = 1 / fps
    # seconds for each GIF image
    seconds_per_gimage = 1 / (bps * len(GIF_array))
    # number of frames that fit into a single GIF image
    spacing = seconds_per_gimage / spf

    return int((cur_f // spacing) % len(GIF_array))


if __name__ == "__main__":

    # pr = cProfile.Profile()
    # pr.enable()

    dirname = os.path.dirname(__file__)

    GIF_array = folder_import(os.path.join(dirname, 'GIFFrames'))

    # frames per second when converting the frames to mp4
    FPS = 30
    # beats per second of song, synchronize GIF cycle to it
    BPS = 138 / 60

    vidcap = cv2.VideoCapture("BadApple.mp4")

    try:
        if not os.path.exists('Frames'):
            os.makedirs('Frames')

    except OSError:
        raise OSError('Could not create directory of Frames')

    cur_frame = 0

    while cur_frame < 100:
        ret, frame = vidcap.read()

        if ret:
            quad = QuadTree(frame, 6)
            index = bpm_matching_index(cur_frame, BPS, FPS)
            fr = quad.get_image(6, index, GIF_array[index], 1)
            # :0>4 makes it so it pads 0s at the front to get a length of 4
            name = os.path.join(dirname, "Frames", "frame{:0>4}.png".format(cur_frame))
            print("Printing {}".format(cur_frame))

            cv2.imwrite(name, fr)

            cur_frame += 1
        else:
            break

    print("Done!")
    vidcap.release()
    cv2.destroyAllWindows()

    final_name = ''.join(random.choice(ascii_lowercase + ascii_uppercase) for i in range(10)) + ".mp4"
    os.chdir(os.path.join(dirname, "Frames"))  # basically just running the ffmpeg command below
    subprocess.call(["ffmpeg", "-framerate", "30", "-i",
                     "frame%04d.png", "-c:v", "libx264",
                     "-pix_fmt", "yuv420p", "output.mp4"])
    subprocess.call(["ffmpeg", "-i", "output.mp4", "-i", "badapple.mp3", "-shortest", final_name])
    os.remove("output.mp4")

    # pr.disable()
    # pr.print_stats(sort='tottime')


# ffmpeg command, NO CLUE how this works
# ffmpeg -framerate 30 -i frame%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4

# merge audio and frames in mp4
# ffmpeg -i "output.mp4" -i "badapple.mp3" -shortest done.mp4
