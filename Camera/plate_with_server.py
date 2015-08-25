# Echo server program
import socket
import multiprocessing as mp
from multiprocessing.managers import BaseManager
import picamera
import time
import cv2 as cv
from picamera.array import PiRGBArray
from PIL import Image
import StringIO
import numpy as np
import pytesseract
import re
import copy
import os


HOST = '127.0.0.1'        # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(1)


class PlaitNumberFinder(object):
    """Estimator of string of plait number. OpenCV 3.0.0"""

    def __init__(self):
        self.readedImg = 0
        self.sourceImg = 0
        self.greyImg = 0
        self.treshImg = 0
        self.plaitNumberImage = 0
        self.plaitNumberResizedImage = 0
        self.cascadeHaar = 0
        self.plaitNumberHigh = 1
        self.plaitNumberWidth = 1
        self.camera = 0
        self.snapShot = 0
        self.rawCapture = 0
        self.newStandart = None
        self.oldStandart = None
        self.allDigit = None
        self.fps = 0
        self.fpsCount = 0
        self.curTime = time.time()

    def initCamera(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 60
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))

        time.sleep(0.1)

    def getSnapShot(self):
        return self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True)

    def printImg(self, *args):
        i = 1
        for img in args:
            cv.imshow("img%u" % i, img)
            i += 1

    def setHaarCascade(self, cascadeHaar):
        self.number_cascade = cv.CascadeClassifier(cascadeHaar)

    def detectPlaitNumber(self, img):
        plaitNumber = self.number_cascade.detectMultiScale(img, 1.3, 5)
        for (x, y, w, h) in plaitNumber:
            self.plaitNumberImage = img[y:y + h, x:x + w]
            height, width = self.plaitNumberImage.shape[:2]
            self.plaitNumberImage = cv.resize(self.plaitNumberImage, (width * 100 / height, 100),
                                              interpolation=cv.INTER_CUBIC)
            return self.plaitNumberImage

    def doGrayImg(self, img):
        return cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    def findEdges(self, grayImg, k1, k2):
        return cv.Canny(grayImg, k1, k2)

    def doThreshold(self, grayImg, k1, k2):
        return cv.threshold(grayImg, k1, k2, cv.THRESH_BINARY)[1]

    def findContours(self, treshImage):
        rows, cols = treshImage.shape
        if rows > 0 and cols > 0:
            image, contours, hierarchy = cv.findContours(treshImage, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
            if isinstance(contours, type(None)):
                print("contours not found")
                return 0
            return contours
        return None

    def findPoligons(self, contours, grayImg):
        if not isinstance(contours, type(None)):
            for cnt in contours:
                rect = cv.minAreaRect(cnt)
                k = rect[1]

                if 4.0 < float(k[1] / (k[0] + 0.0000001)) < 8.0 and k[0] > 50:
                    rows, cols = grayImg.shape
                    M = cv.getRotationMatrix2D((cols / 2, rows / 2), rect[2] + 90, 1)
                    grayImg = cv.warpAffine(grayImg, M, (cols, rows))
                    h, w = rect[1]
                    x = rect[0][0] - w / 2
                    y = rect[0][1] - h / 2
                    self.plaitNumberHigh = h
                    self.plaitNumberWidth = w
                    return(grayImg[y:y + h, x:x + w])
        return 0

    def findLinesHough(self, edgesImg):
        lines = cv.HoughLines(edgesImg, 1, np.pi / 180, 200)
        if isinstance(lines, type(None)):
            print("lines no found")
            return 0

    def estLine(lines):
        t = []
        l = []
        for line in lines:
            for rho, theta in line:
                l.append(rho)
                t.append(theta)
        return t, l

    def findLines(self, lines, img, edges):
        t, l = self.estLine(lines)
        rows, cols, depth = img.shape
        M = cv.getRotationMatrix2D((cols / 2, rows / 2), (t[0] - 1.57079637) * 180 / np.pi, 1)
        res = cv.warpAffine(img, M, (cols, rows))
        lines = cv.HoughLines(res, 1, np.pi / 180, 200)
        t, l = self.estLine(lines)
        return img[min(l):max(l), ]

    def getPlaitNumberByLiterals(self, contours, img, k1):

        count = 0
        x_mass = []
        x_massSorted = []

        #self.plaitNumberHigh = 64
        #self.plaitNumberWidth = 300

        if self.plaitNumberHigh is 1 or self.plaitNumberWidth is 1:
            self.plaitNumberHigh = 50
            self.plaitNumberWidth = 300

        numberForParsing = np.zeros((45, 45), np.uint8)
        if not isinstance(contours, type(None)):
            for cnt in contours:
                x, y, w, h = cv.boundingRect(cnt)

                minH = int(self.plaitNumberHigh * 0.6)
                maxH = int(self.plaitNumberHigh * 0.9)

                minW = int(self.plaitNumberWidth * 0.01)
                maxW = int(self.plaitNumberWidth * 0.2)

                if h in range(minH, maxH) and w in range(minW, maxW):
                    #self.plaitNumberResizedImage = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 1)
                    x_mass.append(x)
                    count += 1
                    literal = img[y:y + h, x:x + w]
                    literal = cv.resize(literal, (30, 45))
                    tmp, literal = cv.threshold(literal, k1, 255, cv.THRESH_BINARY)
                    cv.imwrite("literals\%u.jpg" % count, literal)

                    im = Image.open("literals\%u.jpg" % count)
                    im.save("literals\%u.png" % count)
                    im = Image.open("literals\%u.png" % count)
                    im = im.convert("P")

        tmp = x_mass[:]
        tmp.sort()

        for i in range(0, tmp.__len__()):
            if i < (tmp.__len__() - 1):
                d = tmp[i + 1] - tmp[i]
                if d < 10:
                    x_mass.remove(tmp[i + 1])

        if 8 < x_mass.__len__() < 7:
            return "None"
        numberForParsing = np.zeros((55, (40 * x_mass.__len__() + 6), 3), np.uint8)
        rows, cols, depth = numberForParsing.shape
        numberForParsing[0:0 + rows, 0:0 + cols] = 255

        for i in range(0, x_mass.__len__()):
            x_massSorted.append(x_mass.index(min(x_mass)) + 1)
            x_mass[x_mass.index(min(x_mass))] = 1000000
            tmp = cv.imread('literals\%u.jpg' % x_massSorted[i])
            x = 40 * i + 3
            numberForParsing[5:50, x:x + 30] = tmp
        return numberForParsing

    def saveImgInJPG(self, name, img):
        cv.imwrite(name, img)

    def openJPGsavePNG(self, nameJPG, namePNG):
        im = Image.open(nameJPG)
        im.save(namePNG)

    def openImgInPNG(self, name):
        im = Image.open(name)
        return im.convert("P")

    def parseImgByTess(self, img):
        return pytesseract.image_to_string(img)

    def resizeImg(self, img, w, h):
        return cv.resize(img, (w, h), interpolation=cv.INTER_CUBIC)

    def calcFps(self):
        self.fpsCount += 1
        if time.time() - self.curTime > 1:
            self.fps = self.fpsCount
            self.fpsCount = 0
            self.curTime = time.time()
        return self.fps


def decode(img):
    h, w, depth = img.shape
    H = 320 * h / w
    if H < 300:
        img = cv.resize(img, (320, H), interpolation=cv.INTER_CUBIC)
    else:
        img = cv.resize(img, (320, 240), interpolation=cv.INTER_CUBIC)
    #jpg = Image.fromarray(img)
    #tmpFile = StringIO.StringIO()
    #jpg.save(tmpFile, "JPEG")
    #tmpData = tmpFile.getvalue()
    ret, jpg = cv.imencode('.jpg', img)
    tmpData = jpg.tobytes()
    return tmpData


class ImgData(object):

    def __init__(self):
        self.frame = np.zeros((240, 320, 3), np.uint8)
        self.plateImg = np.zeros((240, 320, 3), np.uint8)
        self.plateThreash = np.zeros((240, 320, 3), np.uint8)
        self.DivadeImg = np.zeros((240, 320, 3), np.uint8)

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ImgData, cls).__new__(cls)
        return cls.instance

    def setFrame(self, frame):
        self.frame = frame

    def getFrame(self):
        if isinstance(self.frame, type(None)):
            return 0
        else:
            return decode(self.frame)

    def setPlateImg(self, frame):
        self.plateImg = frame

    def getPlateImg(self):
        if isinstance(self.plateImg, type(None)):
            return 0
        else:
            return decode(self.plateImg)

    def setPlateThreash(self, frame):
        self.plateThreash = frame

    def getPlateThreash(self):
        if isinstance(self.plateThreash, type(None)):
            return 0
        else:
            return decode(self.plateThreash)

    def setDivadeImg(self, frame):
        self.DivadeImg = frame

    def getDivadeImg(self):
        if isinstance(self.DivadeImg, type(None)):
            return 0
        else:
            return decode(self.DivadeImg)


def server(data):
    while True:
        print('Server has been started')
        conn, addr = s.accept()
        print(('Connected by', addr))

        while True:
            try:
                tmp = conn.recv(20)

                if tmp == 'generalview':
                    img = data.getFrame()
                elif tmp == 'platenumber':
                    img = data.getPlateImg()
                elif tmp == 'platenumberthreash':
                    img = data.getPlateThreash()
                #elif tmp == 'generalviewwithroi':
                #    img = data.getDivadeImg()
                else:
                    img = data.getFrame()

                if img:
                    conn.sendall(img)
                else:
                    img = data.getFrame()
                    conn.sendall(img)
            except:
                print('Connection error')
                conn.close()
                print('Server has been stoped')
                break


def gDivadeImg(img):
    row, cols, depth = img.shape
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


def configurateDetector(path, drive, leave, time):
    base, ext = os.path.splitext(path)
    config = open("{}{}".format(base, ext), mode='r')
    for i in range(0, 16):
        tmp = config.readline()
        if tmp.find('__True__') > 0:
            drive[i] = True
        else:
            drive[i] = False
    tmp = config.readline()
    for i in range(0, 16):
        tmp = config.readline()
        if tmp.find('__True__') > 0:
            leave[i] = True
        else:
            leave[i] = False
    time = os.path.getmtime(path)
    config.close()
    print("Detector is reconfigurated")
    return time


def getLastModifieTime(path):
    return os.path.getmtime(path)


#Starting Script
#Plate Finder
def plateFinder(data, finder, image):

    cutNumberImg = finder.detectPlaitNumber(image)
    data.setPlateImg(cutNumberImg)

    if not isinstance(cutNumberImg, type(None)):

        finder.plaitNumberImage = cutNumberImg

        cutNumberImgGrey = finder.doGrayImg(cutNumberImg)
        cutNumberImgTresh = finder.doThreshold(cutNumberImgGrey, 120, 255)
        finder.treshImg = copy.copy(cutNumberImgTresh)
        contours = finder.findContours(cutNumberImgTresh)
        justNumber = finder.findPoligons(contours, finder.treshImg)

        if not isinstance(justNumber, type(0)):
            row, cols = justNumber.shape
            if row > 0 and cols > 0:
                #justNumber = finder.resizeImg(justNumber, 300, 64)
                cutNumberImgTresh = copy.copy(justNumber)
                contours = finder.findContours(cutNumberImgTresh)
                justNumber = finder.getPlaitNumberByLiterals(contours, justNumber, 140)
                data.setPlateThreash(justNumber)

                if justNumber is not "None":

                    #finder.saveImgInJPG('justNumber.jpg', justNumber)
                    #finder.openJPGsavePNG('justNumber.jpg', 'justNumber.png')
                    #numberForParsing = finder.openImgInPNG('justNumber.png')
                    numberForParsing = cv.imencode(".png", justNumber)

                    stringNumber = finder.parseImgByTess(numberForParsing)

                    n = finder.newStandart.match(stringNumber)
                    o = finder.oldStandart.match(stringNumber)
                    d = finder.allDigit.match(stringNumber)

                    path = '/var/www/plate_number_logs.txt'
                    base, ext = os.path.splitext(path)
                    log = open("{}{}".format(base, ext), mode='a')

                    path = '/var/www/plate_number_logs_err.txt'
                    base, ext = os.path.splitext(path)
                    errlog = open("{}{}".format(base, ext), mode='a')

                    if not isinstance(n, type(None)):
                        string = time.asctime() + "   " + n.group()
                        print(string)
                        log.write(string + '\r\n')
                    elif not isinstance(o, type(None)):
                        string = time.asctime() + "   " + o.group()
                        print(string)
                        log.write(string + '\r\n')
                    elif not isinstance(d, type(None)):
                        string = time.asctime() + "   " + d.group()
                        print(string)
                        log.write(string + '\r\n')
                    else:
                        string = time.asctime() + "   " + stringNumber + "   With Errors!!"
                        print(string)
                        errlog.write(string + '\r\n')
                    log.close()
                    errlog.close()
                    #time.sleep(1)


def DirectionDetector(data):

    finder = PlaitNumberFinder()
    finder.initCamera()
    finder.setHaarCascade('/home/pi/Camera/Camera/haarcascade_russian_plate_number.xml')

    finder.newStandart = re.compile('[a-z]{2}\d{4}[a-z]{2}', re.IGNORECASE)
    finder.oldStandart = re.compile('\d{5}[a-z]{2}', re.IGNORECASE)
    finder.allDigit = re.compile('\d{7}', re.IGNORECASE)

    littleImgPrv = [None for i in range(0, 16)]
    movCount = 0
    snapCount = 0
    roiForDrive = [0 for i in range(0, 16)]
    roiForLeave = [0 for i in range(0, 16)]
    lastChangeTime = 0
    confPath = '/var/www/config_drive_direction.txt'

    lastChangeTime = configurateDetector(confPath, roiForDrive, roiForLeave, lastChangeTime)

    for frame in finder.getSnapShot():
        image = frame.array

        generalview = image.copy()
        cv.putText(generalview, "fps=%u" % finder.calcFps(), (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        data.setFrame(generalview)

        #divadeImg = drawDiviadeLines(image.copy())
        #data.setDivadeImg(divadeImg)

        if getLastModifieTime(confPath) == lastChangeTime:
            pass
        else:
            lastChangeTime = configurateDetector(confPath, roiForDrive, roiForLeave, lastChangeTime)

################################################################
        #g = gDivadeImg(image.copy())
        #for i in range(0, 16):
            #littleImg = next(g)
            #gray = cv.cvtColor(littleImg.copy(), cv.COLOR_BGR2GRAY)
            #gray = cv.GaussianBlur(gray, (21, 21), 0)

            #if littleImgPrv[i] is None:
                #littleImgPrv[i] = gray.copy()
                #continue

            #frameDelta = cv.absdiff(littleImgPrv[i], gray)
            #thresh = cv.threshold(frameDelta, 25, 255, cv.THRESH_BINARY)[1]
            #thresh = cv.erode(thresh, None, iterations=2)

            #(img, cnts, _) = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL,
                #cv.CHAIN_APPROX_SIMPLE)

            #for c in cnts:
                ## if the contour is too small, ignore it
                #if cv.contourArea(c) < 500:
                    #continue
                ## compute the bounding box for the contour, draw it on the frame,
                ## and update the text
                #if movCount == 1:
                    #movCount = 0
                    ##(x, y, w, h) = cv.boundingRect(c)
                    ##cv.rectangle(littleImg, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    ##plateFinder(data, finder, image)
                #movCount += 1
                #break

            #if snapCount == 5:
                #snapCount = 0
                #littleImgPrv[i] = gray
            #snapCount += 1
###############################################################################
        plateFinder(data, finder, image)
        finder.rawCapture.truncate(0)


class MyManager(BaseManager):
    pass


def Manager():
    m = MyManager()
    m.start()
    return m


def main(data):
    DirectionDetector(data)


MyManager.register('ImgData', ImgData)


if __name__ == '__main__':

    manager = Manager()

    data = manager.ImgData()

    procServer = mp.Process(target=server, args=(data,))
    procServer.start()

    main(data)

    s.close()