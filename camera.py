"""
This is a python module for the camera on the Smith Lab weather station.

Needs to:
- Update to the website with a couple of frames per second for live streaming
"""
# example code to take a picture
import os
from picamera2 import Picamera2
import time

camera = Picamera2()

camera_config = camera.create_still_configuration()
camera.configure(camera_config)

camera.start()
time.sleep(2)

# Capture Image
parent_folder = os.chdir(f'/home/surp')
image_path = "images"
save_path = os.path.join(parent_folder, image_path)

if save_path.exists():
    print('yay!')
else:
    os.mkdir(save_path)


camera.capture_file(image_path)
