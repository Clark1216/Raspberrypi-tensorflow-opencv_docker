# raspberrypi-docker-tensorflow-opencv

I will be adding a proper Readme.md to this repository very soon.
Suffice to say that I am trying to build a docker container with version 2.3 of Tensorflow and also will be adding OpenCV and FFMPEG.

If you are looking for answers before I get to build the Readme.md I recommend you to watch how I built this repository on

Below is modified and tested from The original [Step-By-Step Instructions](https://spltech.co.uk/how-to-run-object-detection-with-tensorflow-2-on-the-raspberry-pi-using-docker/) and [Youtube video](https://www.youtube.com/watch?v=uENGyDXnI2M&list=PL3OV2Akk7XpAOAeD8BbqpHcELoxihaMvc):

## Prerequisites
**Test History:**

| Raspberry Model                                                                              | RAM w/ GPU Memory Allocation | Raspberry Pi OS | Results |
| ----                                                                                       | ----           | ----         | ---- |
| 4B  | 1G / 64M     | Debian 10.11 "Buster" | Fail (due to insufficient RAM)
| 4B  | 4G w/ 256M    | Debian 10.11 "Buster" | Pass
| 4B | 4G w/ 256M | Debian 11.0 "Bullseyes" | Fail (due to longer support Picamera libs)



## Setup
These are the main steps you need to complete:
* Install and configure the PI Camera if you haven’t yet. See this separate guide I created to install it:
* How to Install a Raspberry PI Camera
* Install Docker(Instructions below)
* Download this github repository and follow the setup instructions
* Setup X11 forwarding to camera
* Download model from model Zoo
* Run example

### Installing Docker
Installing Docker in the Raspberry PI is very easy. But before you do that, it is always best that you get all the latest updates on your Raspberry PI. So let’s do that first:
```
sudo apt update
```
```
sudo apt upgrade
```
```
sudo reboot
```
And now we are ready to install docker:
```
curl -fsSL get.docker.com -o get-docker.sh && sh get-docker.sh
```
Add your user to the Docker Group, taking example that your username is pi:
```
sudo usermod -aG docker pi
```
And let's reboot again, then double check that docker is really installed:
```
sudo reboot
```
```
docker version
```
Last step is to install docker-compose on the Raspberry PI
To get docker-compose up and running, we will need python 3 and pip. So let’s install it first:
```
sudo apt update
```
```
sudo apt install python3 python3-pip
```
Now we can install docker-compose with pip and test it after installation:
```
pip3 install docker-compose
```
```
sudo reboot
```
```
docker-compose version
```
### Raspberry PI Camera Setup
If you have no idea about installing the PiCameraV2, kindly refer to this [guide](https://spltech.co.uk/raspberry-pi-camera-tutorial-how-to-install-a-raspberry-pi-camera/)

### Starting the camera docker container
After giit cloning this [repository](https://github.com/Clark1216/Raspberrypi-tensorflow-opencv_docker), Run the container:
```
cd Raspberrypi-tensorflow-opencv_docker
```
```
docker-compose up -d
```
It might take a while as it will download the docker container from docker hub.
If it cannot build docker image automatically, try:
```
docker build -t tensorflow2-opencv4-rpi4:1.0 .
```
### Enabling access to X11 Server
The camera docker container needs to connect to the X11 server running on the Raspberry PI. We need to allow it to do so. Best way is to disable the user permission and allow all clients to use:
```
xhost +
```
To validate that the docker container is able to open a window with a view of the Picamera let’s try python example3.py:
```
docker exec -it camera_based_person_counter bash
```
```
cd /app/
```
```
python3 example3.py
```
If your camera is working then you should be able to see a window displaying what your camera is capturing.

If you are using UVC camera, try either one below instead:
```
fswebcam -d /dev/video1 --no-banner -r 1280x720 "./output.jpg"
```
```
cd /app/
```
```
python3 UVC_camera_test.py
```

### Download detection model and Test Object Detection
Now that we know that the camera is working, we can test object detection.
To start object detection on the raspberry pi open a terminal again.
```
docker exec -it camera_based_person_counter bash
```
```
cd /app
```
```
python3 object_detection_camera.py
```
Then it will automatically download model if there is no existing one.
The model loading will usually take 3 minutes. If all goes well you should see a window popup with a view of the camera with annotation from object detection.

Eventually, enjoy trying person counter code and its API as well:
```
python3 camera_based_person_counter.py
```
```
python3 camera_based_person_counter_API.py
```

Alternatively, remove and recreate the container by uncommenting the 2nd to last line in `docker-compose.yml` to activate autostart of API upon each reboot:
```
command: bash -c "cd /app/ && python3 camera_based_person_counter_API.py"
```

---
## Unsolved issue log for reference of developers
1. Log-2022-02-22:

In the new Rpi4 OS 4.1 released by Jan 2022, PiRGBArray and Picamera has import error in regardless of original docker or our own complied docker, shown as below:
```
Traceback (most recent call last):
  File "example.py", line 2, in <module>
    from picamera.array import PiRGBArray
  File "/usr/local/lib/python3.7/dist-packages/picamera/__init__.py", line 72, in <module>
    from picamera.exc import (
  File "/usr/local/lib/python3.7/dist-packages/picamera/exc.py", line 41, in <module>
    import picamera.mmal as mmal
  File "/usr/local/lib/python3.7/dist-packages/picamera/mmal.py", line 47, in <module>
    from .bcm_host import VCOS_UNSIGNED
  File "/usr/local/lib/python3.7/dist-packages/picamera/bcm_host.py", line 47, in <module>
    _lib = ct.CDLL('libbcm_host.so')
  File "/usr/lib/python3.7/ctypes/__init__.py", line 356, in __init__
    self._handle = _dlopen(self._name, mode)
OSError: libbcm_host.so: cannot open shared object file: No such file or directory
```
**Comment:** This problem looks very similar to [this post](https://raspberrypi.stackexchange.com/questions/114035/picamera-and-ubuntu-20-04-arm64) indicating that Picamera is no longer fully supported but this is not sensible as the OS is independent with the docker, hence it seems weird. Guessing will be OS's 32bit or 64bit issue, which can be verified later.

---
## About
This work is on top of [work](https://github.com/armindocachada/raspberrypi-docker-tensorflow-opencv) from armindocachada for acedemic research.

### Built With

* [Docker](https://docs.docker.com/) - Containerization Engine for Deployment
* [Python Flask](http://flask.pocoo.org/docs/1.0/) - Python Web-Framework

### Authors

* **Guanliang Zhao, M.Sc.** - *Programe, full stack* - EEE School, Nanyang Technological University, Singapore
* **Dr Pengfei Du** - *Initial work, Supervision* - [A*Star SIMTech, Singapore](https://www.a-star.edu.sg/simtech)

### License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
