from docx import Document
from docx.shared import Inches
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

from selenium.webdriver import ActionChains

#!IMPORTANT, DOESNT WORK IF NOT DONE:
# #Einstellungen > System > Anzeige > Skalierung und Anordnung: Groesse von Text und ...: 100% instead of 125%
# wenn Screenshots sonst rechts abgeschnitten sind!

# get the id of sth called "<video id=".." ..>, not easily found by inspector, open div boxes until found.
# change paths, ids here
path = "C:\Program Files (x86)\chromedriver.exe"

# region SETUP


# def setup():
# make error go away :-)
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
# kein chrome fenster wird geoeffnet
# options.add_argument("--headless")
driver = webdriver.Chrome(path, options=options)
driver.set_window_position(0, 0)
driver.set_window_size(1024, 768)
driver.get('https://videoakademie.ko-ld.de/Panopto/Pages/Viewer.aspx?id=20dc555a-84e3-4ca8-b520-abca00eeb191&start=undefined')
# Start Playing the Video at 2x speed
play = driver.find_element_by_id('playButton')
time.sleep(2)
ActionChains(driver).click(play).perform()
# Stummschalte!!
speed = driver.find_element_by_id('playSpeedButton')
ActionChains(driver).click(speed).perform()
fastest = driver.find_element_by_id('Fastest')
ActionChains(driver).click(fastest).perform()

element = driver.find_element_by_id('primaryVideo')
document = Document()


# Paste in Word example
# document = Document()
# document.add_picture('screenshot1.png', width=Inches(6.0))
# document.add_picture('screenshot2.png', width=Inches(6.0))
# document.save('demo.docx')

# endregion

# region IMAGE PROCESSING

# load as numpy array


def load_image(infilename):
    img = Image.open(infilename)
    img.load()
    data = np.asarray(img, dtype="int32")
    return data


def save_image(npdata, outfilename):
    img = Image.fromarray(np.asarray(
        np.clip(npdata, 0, 255), dtype="uint8"), "L")
    img.save(outfilename)


def normalize(arr):
    rng = arr.max()-arr.min()
    amin = arr.min()
    return (arr-amin)*255/rng


def rgb2gray(rgb):
    return np.dot(rgb[..., :3], [0.2989, 0.5870, 0.1140])

# NCC too slow


# Values for same picture, only moved cursor
# Manhattan norm: 8325.966396323738
# Zero norm: 138.0

# Values for different pictures
# Manhattan norm: 9913029.394698184
# Zero norm: 158730.0
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

# endregion

# region MAIN
# get video length, while 1/2 diese zeit noch nicht vergangen ist, do these??


time.sleep(10)
# init prev
element.screenshot('sc.png')
prevprev = None  # vgl mit letzten beiden bildern!
prev = rgb2gray(mpimg.imread('sc.png'))
while True:
    time.sleep(5)
    element.screenshot('sc.png')

    tmp = rgb2gray(mpimg.imread('sc.png'))
    n_m, n_0 = compare_images(prev, tmp)
    print(n_0)
    if(n_0 > 100000):  # threshold not quite gud yet
        print("jaa")
        document.add_picture('sc.png', width=Inches(6.0))
        document.save('vl_am_date.docx')
    prev = tmp

# driver.quit()

# img = mpimg.imread('screenshot1.png')
# s1 = rgb2gray(img)
# img = mpimg.imread('screenshot2.png')
# s2 = rgb2gray(img)
# img1 = s2
#     img2 = s1
#     # compare
#     n_m, n_0 = compare_images(img1, img2)
#     print("Manhattan norm:", n_m)  # , "/ per pixel:", n_m/img1.size)
#     print("Zero norm:", n_0)  # , "/ per pixel:", n_0*1.0/img1.size)
