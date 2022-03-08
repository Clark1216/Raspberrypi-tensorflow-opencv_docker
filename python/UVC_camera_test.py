#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import tensorflow as tf
from object_detection.utils import visualization_utils as viz_utils
import matplotlib.pyplot as plt
#from PIL import Image, ImageDraw, ImageFont
import time
import six.moves.urllib as urllib
import os
import tarfile
from time import sleep

import io



import os
import sys
import re

from datetime import datetime
from PIL import Image


import requests
import json
from six import BytesIO

# Load the COCO Label Map
elapsed = []

def Camera_Searching():
    camera_id_list = []
    for device in range(0,10):
        stream = cv2.VideoCapture(device)
        
        grabbed = stream.grab()
        stream.release()
        if not grabbed:
            continue
        
        camera_id_list.append(device)
    print('Available camera IDs are {}'.format(camera_id_list))
    if camera_id_list:
        print('Choose the most likely UVC cam id: {}'.format(camera_id_list[0]))
        return camera_id_list[0]
    else:
        print('No available UVC modules!')
        return camera_id_list
    
def Camera_Setting(dev_num):
    #setting attributes
    fps = "15"
    brightness = "64"
    contrast = "12"
    saturation = "55"
    white_balance_temperature_auto = "1"
    white_balance_temperature = "5000"
    backlight_compensation = "3"
    exposure_auto = "3"
    exposure_absolute = "179"
    exposure_auto_priority = "0"
    #setting commands
    os.system("v4l2-ctl -d /dev/video{} --set-parm={}".format(dev_num,fps))
    os.system("v4l2-ctl -d /dev/video{} --set-ctrl={}={}".format(dev_num,'brightness',brightness))
    os.system("v4l2-ctl -d /dev/video{} --set-ctrl={}={}".format(dev_num,'contrast',contrast))
    os.system("v4l2-ctl -d /dev/video{} --set-ctrl={}={}".format(dev_num,'saturation',saturation))
    os.system("v4l2-ctl -d /dev/video{} --set-ctrl={}={}".format(dev_num,'white_balance_temperature_auto',white_balance_temperature_auto))
    os.system("v4l2-ctl -d /dev/video{} --set-ctrl={}={}".format(dev_num,'white_balance_temperature',white_balance_temperature))
    os.system("v4l2-ctl -d /dev/video{} --set-ctrl={}={}".format(dev_num,'backlight_compensation',backlight_compensation))
    os.system("v4l2-ctl -d /dev/video{} --set-ctrl={}={}".format(dev_num,'exposure_auto',exposure_auto))
    os.system("v4l2-ctl -d /dev/video{} --set-ctrl={}={}".format(dev_num,'exposure_absolute',exposure_absolute))
    os.system("v4l2-ctl -d /dev/video{} --set-ctrl={}={}".format(dev_num,'exposure_auto_priority',exposure_auto_priority))
    print('Camera setting finished.')

def uvc_capture(filepath,dev_num):
    ##kindly notice command "/dev/video0" using physical address, do not use "/dev/video0"
    ## Comment below 1 line if default setting for camera is needed
    #Camera_Setting(dev_num)
    commands = "fswebcam -d /dev/video{} --no-banner -r 1280x720 {}".format(dev_num,filepath)
    capture = os.system(commands)

######################
###### Main Body #####
######################
if __name__ == '__main__':

    filepath='/app/imputdata/cam_test.jpg'
    print("Camera connecting")
    dev_num = Camera_Searching()
    print("Camera starting")
    uvc_capture(filepath,dev_num)
    image_rgb_np =cv2.imread(filepath)
    gray_img = cv2.cvtColor(image_rgb_np, cv2.COLOR_BGR2GRAY)
    h, w = image_rgb_np.shape[:2]
    m = np.reshape(gray_img, [1, w*h])
    print("mean value of greyscale",m.sum()/(w*h))



