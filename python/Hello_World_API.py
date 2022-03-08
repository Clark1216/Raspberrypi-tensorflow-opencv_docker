from flask import Flask, render_template, flash, redirect, url_for, request, session,jsonify
from flask import send_file
#import requests
from time import sleep

from PIL import Image
from datetime import datetime

#!/usr/bin/env python
# -*- coding: utf-8 -*-

#from PIL import Image, ImageDraw, ImageFont
import time
import six.moves.urllib as urllib
import os
import tarfile
from time import sleep
import cv2
import io

import sys
import re
import numpy as np
import cv2
import tensorflow as tf
sys.path.append('/tensorflow/models/research')
sys.path.append('/tensorflow/models/research/slim')
sys.path.append('/tensorflow/models/research/object_detection')
from object_detection.utils import visualization_utils as viz_utils
import matplotlib.pyplot as plt

from datetime import datetime
from PIL import Image


import requests
import json
from six import BytesIO

from picamera.array import PiRGBArray
from picamera import PiCamera

from threading import Timer

#BSD License need to declare for picamera,https://opensource.org/licenses/BSD-3-Clause
app = Flask(__name__)

def Camera_Setting():
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
    os.system("v4l2-ctl -d /dev/video0 --set-parm={}".format(fps))
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl={}={}".format('brightness',brightness))
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl={}={}".format('contrast',contrast))
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl={}={}".format('saturation',saturation))
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl={}={}".format('white_balance_temperature_auto',white_balance_temperature_auto))
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl={}={}".format('white_balance_temperature',white_balance_temperature))
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl={}={}".format('backlight_compensation',backlight_compensation))
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl={}={}".format('exposure_auto',exposure_auto))
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl={}={}".format('exposure_absolute',exposure_absolute))
    os.system("v4l2-ctl -d /dev/video0 --set-ctrl={}={}".format('exposure_auto_priority',exposure_auto_priority))
    print('Camera setting finished.')

def downloadModel(MODEL_URL):
    firstpos = MODEL_URL.rfind("/")
    lastpos = MODEL_URL.rfind(".")
    MODEL_NAME = MODEL_URL[firstpos + 1:lastpos]
    MODEL_FILE = MODEL_NAME + '.tar.gz'

    print("Preparing to download tensorflow model {}".format(MODEL_FILE))
    print("Is file downloaded? %s " % os.path.isfile(MODEL_FILE))
    if not os.path.isfile(MODEL_FILE):
        opener = urllib.request.URLopener()
        opener.retrieve(MODEL_URL, MODEL_FILE)
        tar_file = tarfile.open(MODEL_FILE)
        for file in tar_file.getmembers():
            file_name = os.path.basename(file.name)
            tar_file.extract(file, os.getcwd())

def uvc_capture(filepath):
    #kindly notice command "/dev/video0" using physical address, do not use "/dev/video0" 
    commands = "fswebcam -d /dev/video0 --no-banner -r 1280x720 {}".format(filepath)
    capture = os.system(commands)

def loadTensorflowModel():
    start_time = time.time()
    tf.keras.backend.clear_session()
    detect_fn = tf.saved_model.load(
        '/tensorflow/models/research/object_detection/test_data/ssd_mobilenet_v2_320x320_coco17_tpu-8/saved_model/')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print('Elapsed time: ' + str(elapsed_time) + 's')
    return detect_fn

def doinference(image_np):
    input_tensor = np.expand_dims(image_np, 0)
    start_time = time.time()
    detections = detect_fn(input_tensor)
    end_time = time.time()
    elapsed.append(end_time - start_time)

    plt.rcParams['figure.figsize'] = [42, 21]
    label_id_offset = 1
    image_np_with_detections = image_np.copy()
    viz_utils.visualize_boxes_and_labels_on_image_array(
        image_np_with_detections,
        detections['detection_boxes'][0].numpy(),
        detections['detection_classes'][0].numpy().astype(np.int32),
        detections['detection_scores'][0].numpy(),
        category_index,
        use_normalized_coordinates=True,
        max_boxes_to_draw=200,
        min_score_thresh=.40,
        agnostic_mode=False)

    return [image_np_with_detections,detections['detection_classes'][0].numpy().astype(np.int32), detections['detection_scores'][0].numpy()]

def corefunction(filepath,outputpath):
    
#     filepath='/app/imputdata/1.jpg'
#     outputpath="/app/outputdata/1.jpg"
    print("Camera starting")
    uvc_capture(filepath)
    image_rgb_np =cv2.imread(filepath)
    #frame = piFrame.array
    #image_rgb_np = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    gray_img = cv2.cvtColor(image_rgb_np, cv2.COLOR_BGR2GRAY)
    h, w = image_rgb_np.shape[:2]
    m = np.reshape(gray_img, [1, w*h])
    if m.sum()/(w*h) > 10:
        image_rgb_np_with_detections, category_index, score= doinference(image_rgb_np)
        image_bgr_np_with_detections = cv2.cvtColor(image_rgb_np_with_detections, cv2.COLOR_RGB2BGR)
        print("saving output image")
        cv2.imwrite(outputpath,image_bgr_np_with_detections)
        count=0
        for i in range(len(score)):
            if score[i]>0.45 and category_index[i]==1:
                count=count+1
    #             print('-----------------')
    #             print('TOTAL HUMAN NUMBER IS')
    #             print(i, end=" ")
    #             print(' ')
    #             print('-----------------')
    #     print(category_index)
    #     print(score)
        print('COUNT NUMBER IS------------------------')
        print(count)
        print('------------------------------')
        return count
    else:
        print('Pic is too dark, gery value is only {}'.format(m.sum()/(w*h)))
        return -1

################################
###  Function Def:        ######
###   Preprocess & Decode QR ###
################################
def decoder(threshold,file_path1,file_path2):#Input is the binarization threshold

    #Path below is only for testing and debugging
    file_path_static = '/home/pi/Desktop/DuDu_Bench/Successful_Sample2_A0169.png'
        
#######################
###  Preprocessing ####
#######################
    img_tmp = Image.open(file_path1)
    img_tmp_BL = img_tmp.convert('L')#Convert to gray img

    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
            
    #Binarize the image
    img_tmp_BIN = img_tmp_BL.point(table,'1')
    img_tmp_BIN.save(file_path2)

@app.route('/')
def index():
    return str('Hello, pls contact A*STAR developer Dr. Du Pengfei')

@app.route('/get_image')
def get_image():
##Below 4 lines are stricting criteria: only send desired images in get mode. Toggle between below 4 lines and 5th line to swtich.
#     if request.args.get('type') == '1':
#         filename = './outputdata/Astar.jpeg'
#     else:
#         filename = './outputdata/error.jpeg'
    filename = './outputdata/Astar.jpeg'
    
    if os.path.isfile(filename):
        return send_file(filename, mimetype='image/jpeg')
    else:
        return str('There is no image file that can be transfered in the target directory')

if __name__ == '__main__':     
    app.run(debug=True, port=83, host='127.0.0.1')
    # app.run(debug=True, port=83, host='172.20.115.125')
   