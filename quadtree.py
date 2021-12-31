import numpy as np
import cv2

from operator import add
from functools import reduce

# quadtree code ripped from
# https://medium.com/analytics-vidhya/transform-an-image-into-a-quadtree-39b3aa6e019a
# for the most part


def split4(image):
    """
    Splits a numpy array into 4, partitioned like a cross in the middle
    
    Parameters: 
        image: numpy array
            must have have least 2 elements in the first 0 axes

    Returns a list of 4 numpy arrays
        [northwest NP, northeast NP, southwest NP, southeast NP]

    Throws ValueError if inputed array is not big enough
    """
    if image.ndim < 2 or image.shape[0] < 2 or image.shape[1] < 2:
        raise ValueError(f"Inputted array with shape {image.shape} is not big enough to split")

    # produces array of 2, split along one axis
    half_split = np.array_split(image, 2)

    # split into 2 along other axis for already split arrays
    res = map(lambda x: np.array_split(x, 2, axis=1), half_split)

    # reduces repeatedly applies the add function to the map, which just
    # puts the 4 subimages all into another array to return
    return reduce(add, res)


def concatenate4(nw, ne, sw, se):
    """
    Merges 4 numpy arrays together

    Parameters:
        nw: numpy array
        ne: numpy array
        sw: numpy array
        se: numpy array

    Returns single numpy array from merging like
        nw ne
        sw se
    """
    # concatenate just merges the arrays, we just do it on the two dimensions
    top = np.concatenate((nw, ne), axis=1)
    bottom = np.concatenate((sw, se), axis=1)
    return np.concatenate((top, bottom), axis=0)


def calculate_mean(img):
    """
    Finds and returns the mean color of an image, in RGBA

    Parameters:
        img: numpy array

    Returns a numpy array with 4 channels, RGBA. If input was RGB, adds A channel

    Raises AttributeError if doesn't have 3 or 4 channels after meaning
    """
    # the image array has 2 dimensions and 2-4 channels for the color
    # we take the mean across the axes 0 and 1 to get our color channel
    pixel = np.mean(img, axis=(0, 1)).astype(np.uint8)

    if pixel.shape[0] == 3:
        # add transparency channel
        return np.append(pixel, 255)
    elif pixel.shape[0] == 4:
        return pixel
    else:
        raise AttributeError("calculate_mean method requires RGB or RGBA")


def check_equal(arr):
    """
    Finds if all elements in a 3 dimensional array are the same

    Parameters:
        arr: numpy array

    Returns Boolean

    Raises ValueError if not 3-dimensional
    """
    if arr.ndim != 3:
        raise ValueError("check_equal requires 3 dimensional numpy array")

    first = arr[0]
    # (x==first) returns a list of booleans
    # we check that all those booleans are satisfied
    # the outer all makes sure the alls all hold through the other dimension
    return all((x == first).all() for x in arr)


def outline(image, option=0):
    """
    Outlines a BGR or BGRA image if at least 3x3

    Parameters:
        image: numpy array
        option: color for outline, default is 0
                if 0, white outline
                if 1, red outline

    Returns numpy array with borders colored if at least 3x3, else returns unchanged

    Raises ValueError for invalid color option
    """
    red_bgr_trans = np.array([36, 28, 237, 255]).astype(np.uint8)
    red_bgr = np.array([36, 28, 237]).astype(np.uint8)
    white_bgr_trans = np.array([255, 255, 255, 255]).astype(np.uint8)
    white_bgr = np.array([255, 255, 255]).astype(np.uint8)

    rows, cols = image.shape[0], image.shape[1]

    # do nothing if not at least 3x3
    if image.shape[0] < 3 or image.shape[1] < 3:
        return image

    if option == 0:
        if image.shape[2] == 4:
            var = white_bgr_trans
        else:
            var = white_bgr
    elif option == 1:
        if image.shape[2] == 4:
            var = red_bgr_trans
        else:
            var = red_bgr
    else:
        raise ValueError("Invalid color option, not 0 or 1")

    image[0, :] = var
    image[rows-1, :] = var
    # technically doubles on the corners, but more readable
    image[:, 0] = var
    image[:, cols-1] = var

    return image


def is_white(pixel):
    """
    Tests if all color channels in given BGR or BGRA pixel is 255, aka white

    Parameters:
        pixel: numpy array, 1D and length 3 or 4

    Returns Boolean
    """
    if pixel.ndim != 1 or (pixel.shape[0] != 3 and pixel.shape[0] != 4):
        raise ValueError("Pixel must be 1 dimensional numpy array with 3-4 elements")

    if pixel.shape[0] == 3:
        return all(pixel == 255)
    elif pixel.shape[0] == 4:
        return all(pixel[:-1] == 255)


def is_whiteish(pixel, constant=100):
    """
    Tests if all color channels in given BGR or BGRA pixel is above a given constant

    Parameters:
        pixel: numpy array, 1D and length 3 or 4
        constant: level of determines whiteish or not, default is 100

    Returns Boolean
    """
    if pixel.ndim != 1 or (pixel.shape[0] != 3 and pixel.shape[0] != 4):
        raise ValueError("Pixel must be 1 dimensional numpy array with 3-4 elements")

    if pixel.shape[0] == 3:
        return all(pixel >= constant)
    elif pixel.shape[0] == 4:
        return all(pixel[:-1] >= constant)


class QuadTree:
    black_bgrt = np.array([0, 0, 0, 255]).astype(np.uint8)
    white_bgrt = np.array([255, 255, 255, 255]).astype(np.uint8)

    def __init__(self, img, limit, level=0):
        """
        Constructor for QuadTree node

        Parameters:
            img: image to quadtree on
            limit: limit to stop recursing on
            level: how deep the node is, default is 0

        Sets instance variables:
            level: int, level of the node
            resolution: tuple, height and width of the node
            is_leaf: Boolean, whether or not node has children
            nw, ne, sw, se: QuadTree, holds child nodes
            img: img given to it
        """
        self.level = level
        self.resolution = img.shape[:2]
        self.img = img

        # if the image is not purely one color, we call for 4 subimages
        if level < limit and not check_equal(img):
            self.is_leaf = False

            split_img = split4(img)
            self.nw = QuadTree(split_img[0], limit, level + 1)
            self.ne = QuadTree(split_img[1], limit, level + 1)
            self.sw = QuadTree(split_img[2], limit, level + 1)
            self.se = QuadTree(split_img[3], limit, level + 1)
        else:
            self.is_leaf = True

    def get_image(self, level, img_id, img=None, has_outline=False):
        """
        Returns image from inserting image into quadtree

        Parameters:
              level: maximum level to recurse
              img_id: id for given image
                    if id matches, then img should be the same
              img: numpy array, default None
              has_outline: option for outlining rectangles
                default is False, 0 for white and 1 for red

        Returns image as numpy array
        """
        if self.is_leaf or self.level == level:
            if is_whiteish(calculate_mean(self.img)):
                if img is None:
                    return np.tile(QuadTree.white_bgrt, (self.resolution[0], self.resolution[1], 1))
                else:
                    key = img_id, self.resolution

                    if key in GIF_dict:
                        return GIF_dict[key]
                    else:
                        # resize takes the dimensions in reverse, kinda annoying
                        resized_frame = cv2.resize(img, self.resolution[::-1], interpolation=cv2.INTER_AREA)
                        GIF_dict[key] = resized_frame
                        return resized_frame
            else:
                if has_outline is False:
                    return np.tile(calculate_mean(self.img), (*self.resolution, 1))
                return outline(np.tile(calculate_mean(self.img), (*self.resolution, 1)), has_outline)

        else:
            return concatenate4(
                self.nw.get_image(level, img_id, img, has_outline),
                self.ne.get_image(level, img_id, img, has_outline),
                self.sw.get_image(level, img_id, img, has_outline),
                self.se.get_image(level, img_id, img, has_outline))


# cache lol
GIF_dict = {}
