FROM armindocachada/tensorflow2-opencv4-raspberrypi4:2.2_4.5.0

#RUN apt-get --allow-releaseinfo-change update && apt-get upgrade -y
RUN apt-get install -y fswebcam

## Flask API and other denpendencies installed from pip3
COPY requirements.txt /
RUN pip3 install -r /requirements.txt

## Add TF dependencies
RUN echo 'export OBJECT_DETECTION_API_PATH=/tensorflow/models/research/object_detection' >> /root/.bashrc
RUN cd /tensorflow/models/research && echo "export PYTHONPATH=$PYTHONPATH:`pwd`:`pwd`/slim:`pwd`/object_detection" >> /root/.bashrc

## Install and compile pygame
#RUN apt-get install -y libsdl2-dev
#ENV HOME "/home"
#RUN cd $HOME && git clone https://github.com/Clark1216/Fundamental_libs-pygame.git pygames
#RUN cd $HOME/pygames && python3 setup.py install
#RUN pip3 install pygame

## Set time zone
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
RUN echo 'Asia/Shanghai' > /etc/timezone

CMD ["tail","-f","/dev/null"]
