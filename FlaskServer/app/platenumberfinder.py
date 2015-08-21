import cv2 as cv
import numpy as np
from picamera import PiCamera
import time
import io
import numpy as np
from PIL import Image
from picamera.array import PiRGBArray

def main():

    while True:

        with PiCamera() as camera:

            camera.resolution = (320, 240)
            camera.framerate = 32

            time.sleep(2)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg',
                                                 use_video_port=True):

                # store frame
                stream.seek(0)
                byt = stream.read()


                #print 'length,%u' % len(byt)
                #time.sleep(0.1)
                print byt
                #time.sleep(0.5)

                stream.seek(0)
                stream.truncate()


if __name__ == '__main__':
    main()