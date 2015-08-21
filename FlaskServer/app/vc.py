# -*- coding: utf-8 -*-
import cv2 as cv
from picamera.array import PiRGBArray, PiArrayOutput
from picamera import PiCamera
import io

class Camera(object):

    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 30
        #self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        self.rawCapture = PiArrayOutput(self.camera, size=(640, 480))

    def getSnapShot(self):
        stream = io.BytesIO()
        self.camera.capture_continuous(stream, 'jpeg', use_video_port=True)
        return stream.read()

    def getArrayOutput(self):
        return self.camera.capture()