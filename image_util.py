
from scipy.linalg import norm
from scipy import sum
import numpy as np
from PIL import Image
import matplotlib.image as mpimg

# Module for working with images (rgb/grayscale numpy arrays)

# Funktioniert nicht.
# def load_image(infilename):
#     img = Image.open(infilename)
#     img.load()
#     data = np.asarray(img, dtype="int32")
#     return data  # as numpy array


def load_image(infilename):
    return mpimg.imread(infilename)  # as numpy array


def save_image(npdata, outfilename):
    img = Image.fromarray(np.asarray(
        np.clip(npdata, 0, 255), dtype="uint8"), "L")
    img.save(outfilename)


# Grauwert Spreizung
def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng


def rgb_to_gray(rgb_numpyarr):
    return np.dot(rgb_numpyarr[..., :3], [0.2989, 0.5870, 0.1140])


def compare_images_manhatten(img1, img2):
    # normalize may be unnecessary
    img1 = normalize(img1)
    img2 = normalize(img2)
    # calculate the difference elementwise for numpy arrays
    diff = img1 - img2
    m_norm = sum(abs(diff))  # Manhattan norm
    return m_norm


def compare_images_zero(img1, img2):
    # normalize may be unnecessary
    img1 = normalize(img1)
    img2 = normalize(img2)
    # calculate the difference elementwise for numpy arrays
    diff = img1 - img2
    z_norm = norm(diff.ravel(), 0)  # Zero norm
    return z_norm
