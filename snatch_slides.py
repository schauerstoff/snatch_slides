import sys
import os
from enum import Enum
from io import BytesIO
from selenium.webdriver.remote.webelement import WebElement
import win32clipboard
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from openpyxl import load_workbook
import urllib.request
import time

#from scipy.misc import imread
from scipy.linalg import norm
from scipy import sum, average

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from scipy import signal

#!IMPORTANT, DOESNT WORK IF NOT DONE:
# #Einstellungen > System > Anzeige > Skalierung und Anordnung: Groesse von Text und ...: 100% instead of 125%
# wenn Screenshots sonst rechts abgeschnitten sind!

# get the id of sth called "<video id=".." ..>, not easily found by inspector, open div boxes until found.
# change paths here
path = "C:\Program Files (x86)\chromedriver.exe"

# Get Data from Video
# # make error go away :-)
# options = webdriver.ChromeOptions()
# options.add_experimental_option('excludeSwitches', ['enable-logging'])
# # kein chrome fenster wird geoeffnet
# # options.add_argument("--headless")
# driver = webdriver.Chrome(path, options=options)
# driver.set_window_position(0, 0)
# driver.set_window_size(1024, 768)
# driver.get('https://videoakademie.ko-ld.de/Panopto/Pages/Viewer.aspx?id=20dc555a-84e3-4ca8-b520-abca00eeb191&start=undefined')

# Start Playing the Video at 2x speed
# get video length, while 1/2 diese zeit noch nicht vergangen ist, do these

# element = driver.find_element_by_id('primaryVideo')
# time.sleep(5)
# element.screenshot('screenshot1.png')
# time.sleep(5)
# element.screenshot('screenshot2.png')
# driver.quit()


# compare
# def load_image(infilename):
#     img = Image.open(infilename)
#     img.load()
#     data = np.asarray(img, dtype="int32")
#     return data


# def save_image(npdata, outfilename):
#     img = Image.fromarray(np.asarray(
#         np.clip(npdata, 0, 255), dtype="uint8"), "L")
#     img.save(outfilename)


# s1 = load_image("screenshot1.png")
# print(type(s1))
# save_image(s1, "test.png")

def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])


img = mpimg.imread('screenshot1.png')
s1 = rgb2gray(img)
print(type(s1))
# plt.imshow(gray, cmap=plt.get_cmap('gray'), vmin=0, vmax=1)
# plt.show()
img = mpimg.imread('screenshot2.png')
s2 = rgb2gray(img)
print("done")
# NCC too slow


def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng


def main():
    #file1, file2 = sys.argv[1:1+2]
    # read images as 2D arrays (convert to grayscale for simplicity)
    img1 = s2
    img2 = s1
    # compare
    n_m, n_0 = compare_images(img1, img2)
    print("Manhattan norm:", n_m)  # , "/ per pixel:", n_m/img1.size)
    print("Zero norm:", n_0)  # , "/ per pixel:", n_0*1.0/img1.size)


def compare_images(img1, img2):
    # normalize to compensate for exposure difference, this may be unnecessary
    # consider disabling it
    img1 = normalize(img1)
    img2 = normalize(img2)
    # calculate the difference and its norms
    diff = img1 - img2  # elementwise for numpy arrays
    m_norm = sum(abs(diff))  # Manhattan norm
    z_norm = norm(diff.ravel(), 0)  # Zero norm
    return (m_norm, z_norm)


main()

# Values for same picture, only moved cursor
# Manhattan norm: 8325.966396323738
# Zero norm: 138.0

# Values for different picture
# Manhattan norm: 9913029.394698184
# Zero norm: 158730.0

#Paste in Word
