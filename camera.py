import picamera
import picamera.array                           # This needs to be imported explicitly
import time
import cv2
import numpy as np                              



class Camera:
    def __init__(self):
        camera = picamera.PiCamera()
        camera.resolution = (640, 480)
        camera.vflip = False 
        camera.hflip = True   
        

    def capture(self):
        rawframe = picamera.array.PiRGBArray(camera, size = (640, 480))

        # Allow the camera to warm up
        time.sleep(1)

        # Capture a single frame and store it in the array we created before
        # Note that we chose the RGB format
        camera.capture(rawframe, format = 'rgb')

        # Clear the rawframe in preparation for the next frame
        # This way, you can use the same rawframe for the next image capture if you need to
        # You need this if you want to place the camera.capture in a loop
        rawframe.truncate(0)
 
        # Create a numpy array representing the image   
        return rawframe.array
