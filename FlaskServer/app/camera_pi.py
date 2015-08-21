# -*- coding: utf-8 -*-
import time
import io
import threading
from picamera import PiCamera
from picamera.array import PiRGBArray
from PIL import Image
import cv2 as cv
import numpy as np
import StringIO


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    gray = None
    withroi = None
    byt = None
    last_access = 0  # time of last client access to the camera
    main_img = None

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def devideImg(self, img):
        row, cols = img.shape
        width = cols / 5
        high = row / 5
        for i in range(0, 5):
            yield (img[0:high, (i * width):(width * (i + 1))])
        for i in range(0, 3):
            yield (img[(high * (i + 1)):(high * (i + 1) + high), (cols - width):cols])
        for i in range(0, 5):
            yield (img[(row - high):row, ((4 - i) * width):(width * ((4 - i) + 1))])
        for i in range(0, 3):
            yield (img[(high * ((2 - i) + 1)):(high * ((2 - i) + 1) + high), 0:width])

    def get_frame(self, picname):
        Camera.last_access = time.time()
        self.initialize()
        if picname == 'generalview':
            return self.frame
        elif picname == 'gray':
            return self.gray
        elif picname == 'withroi':
            return self.withroi

    @classmethod
    def _thread(cls):
        with PiCamera() as camera:
            # camera setup
            #camera.resolution = (640, 480)
            #camera.hflip = True
            #camera.vflip = True

            camera.resolution = (320, 240)
            camera.framerate = 32
            #rawCapture = PiRGBArray(camera, size=(640, 480))

            # let camera warm up
            #camera.start_preview()
            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):

                # store frame
                stream.seek(0)
                cls.byt = stream.read()

                cls.main_img = Image.open(foo).convert('RGB')
                open_cv_image = np.array(cls.main_img)
                open_cv_image = cv.cvtColor(open_cv_image, cv.COLOR_BGR2RGB)

                ret, jpg = cv.imencode('.jpg', open_cv_image)
                cls.frame = jpg.tobytes()

                #Drive Detection

                gr = cv.cvtColor(open_cv_image, cv.COLOR_BGR2GRAY)
                ret, jpg = cv.imencode('.jpg', gr)
                cls.gray = jpg.tobytes()

                #cls.frame = cls.byt

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                #if time.time() - cls.last_access > 10:
                    #break
        cls.thread = None