## raspberrypi-docker-tensorflow-opencv

I will be adding a proper Readme.md to this repository very soon. 
Suffice to say that I am trying to build a docker container with version 2.3 of Tensorflow and also will be adding OpenCV and FFMPEG.

If you are looking for answers before I get to build the Readme.md I recommend you to watch how I built this repository on

Below is modified and tested from The original [Step-By-Step Instructions](https://spltech.co.uk/how-to-run-object-detection-with-tensorflow-2-on-the-raspberry-pi-using-docker/) and [Youtube video](https://www.youtube.com/watch?v=uENGyDXnI2M&list=PL3OV2Akk7XpAOAeD8BbqpHcELoxihaMvc):

### Setup
These are the main steps you need to complete:
* Install and configure the PI Camera if you haven’t yet. See this separate guide I created to install it:
* How to Install a Raspberry PI Camera
* Install Docker(Instructions below)
* Download this github repository and follow the setup instructions
* Setup X11 forwarding to camera
* Download model from model Zoo
* Run example

#### Installing Docker
Installing Docker in the Raspberry PI is very easy. But before you do that, it is always best that you get all the latest updates on your Raspberry PI. So let’s do that first:
```
sudo apt update
sudo apt upgrade
```
