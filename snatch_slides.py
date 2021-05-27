from selenium import webdriver
from selenium.webdriver import ActionChains

from docx import Document
from docx.shared import Inches

import time
import datetime
import image_util as iu

#!IMPORTANT, DOESNT WORK IF NOT DONE:
# #Einstellungen > System > Anzeige > Skalierung und Anordnung: Groesse von Text und ...: 100% instead of 125%
# wenn Screenshots sonst rechts abgeschnitten sind!

# This setup is for panopto player
# get the id of sth called "<video id=".." ..>, not easily found by inspector, open div boxes until found.
# change paths, ids here
path = "C:\Program Files (x86)\chromedriver.exe"
link = 'https://videoakademie.ko-ld.de/Panopto/Pages/Viewer.aspx?id=20dc555a-84e3-4ca8-b520-abca00eeb191&start=undefined'
# CSS IDs
video_id = 'primaryVideo'
ffw_id = 'quickFastForwardButton'
play_id = 'playButton'
speed_id = 'playSpeedButton'
speed_setting_id = 'Fastest'
mute_id = 'muteButton'

# set threshold for similarity, depends on size of image! (=size of browser)
thres = 1000000

# set title for word doc
title = 'bv_vl_' + str(datetime.datetime.now().date()) + '.docx'

# region setup chrome and word


class Browser:
    driver = None
    ffw = None
    video = None

    def __init__(self):
        # make error go away :-)
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # kein chrome fenster wird geoeffnet
        # options.add_argument("--headless")
        self.driver = webdriver.Chrome(path, options=options)
        self.driver.set_window_position(0, 0)
        self.driver.set_window_size(1024, 768)
        self.driver.get(link)

        # init webelements
        time.sleep(2)
        self.video = self.driver.find_element_by_id(video_id)
        self.ffw = self.driver.find_element_by_id(ffw_id)

        # start playing muted video at 2x speed
        mute = self.driver.find_element_by_id(mute_id)
        ActionChains(self.driver).click(mute).perform()
        play = self.driver.find_element_by_id(play_id)
        ActionChains(self.driver).click(play).perform()
        speed = self.driver.find_element_by_id(speed_id)
        ActionChains(self.driver).click(speed).perform()
        fastest = self.driver.find_element_by_id(speed_setting_id)
        ActionChains(self.driver).click(fastest).perform()


class Word:
    document = None

    def __init__(self):
        self.document = Document()
        # seitenraender minimal
        sections = self.document.sections
        for section in sections:
            section.top_margin = Inches(0)
            section.bottom_margin = Inches(0)
            section.left_margin = Inches(0)
            section.right_margin = Inches(0)

# endregion


# abfangen:
# ValueError: operands could not be broadcast together with shapes (502,892) (880,1564)
# wenn man groesse des browsers nachtraeglich aendert

def main():
    chrome = Browser()
    word = Word()

    # init prev, prevprev
    time.sleep(2)
    chrome.video.screenshot('sc.png')
    prevprev = iu.rgb_to_gray(iu.load_image('sc.png'))
    time.sleep(2)
    chrome.video.screenshot('sc.png')
    prev = iu.rgb_to_gray(iu.load_image('sc.png'))

    # init timer
    remaining = chrome.driver.find_element_by_id('timeRemaining')
    timer = remaining.text

    while (timer != '0:00'):
        timer = remaining.text

        chrome.video.screenshot('sc.png')

        tmp = iu.rgb_to_gray(iu.load_image('sc.png'))
        n_m_pp = iu.compare_images_manhatten(prevprev, tmp)
        n_m_p = iu.compare_images_manhatten(prev, tmp)
        print("Manhattan norm:", n_m_p)
        print("Manhattan norm:", n_m_pp)
        if((n_m_p > thres) & (n_m_pp > thres)):
            print("new slide")
            word.document.add_picture('sc.png', width=Inches(6.0))
            word.document.save(title)

            # only reset these when new slide is found
            prevprev = prev
            prev = tmp
            time.sleep(2)  # vorher 5
        else:
            ActionChains(chrome.driver).click(chrome.ffw).perform()

    chrome.driver.quit()


if __name__ == '__main__':
    main()
