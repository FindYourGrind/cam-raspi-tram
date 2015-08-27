# -*- coding: utf-8 -*-

from flask import render_template, flash, redirect, Response
from app import app
import forms
import threading
import time
import socket
import os


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    plate = None
    threash = None
    divade = None
    gray = None
    withroi = None
    byt = None
    last_access = 0  # time of last client access to the camera
    main_img = None
    count = 0

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)

    def get_frame(self, picname):
        Camera.last_access = time.time()
        self.initialize()

        if picname == 'generalview':
            return Camera.frame
        elif picname == 'platenumber':
            return Camera.plate
        elif picname == 'platenumberthreash':
            return Camera.threash
        #elif picname == 'generalviewwithroi':
        #    return Camera.divade

    @classmethod
    def _thread(cls):

        HOST = '127.0.0.1'    # The remote host
        PORT = 50007          # The same port as used by the server
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                if cls.count == 0:
                    name = 'generalview'
                elif cls.count == 1:
                    name = 'platenumber'
                elif cls.count == 2:
                    name = 'platenumberthreash'

                s.sendall(name)

                if name == 'generalview':
                    cls.frame = s.recv(76800)
                elif name == 'platenumber':
                    cls.plate = s.recv(76800)
                elif name == 'platenumberthreash':
                    cls.threash = s.recv(76800)

                cls.count += 1
                if cls.count == 3:
                    cls.count = 0

                if time.time() - cls.last_access > 5:
                    print("Timeout")
                    s.shutdown(2)
                    s.close()
                    cls.thread = None
                    break
            except:
                print('Connection error')
                #s.close()
                while True:
                    try:
                        print("Trying to connect")
                        s.connect((HOST, PORT))
                        break
                    except:
                        pass

                    if time.time() - cls.last_access > 5:
                        print("Timeout")
                        s.close()
                        cls.thread = None
                        return

                print("Connected")


@app.route('/')
@app.route('/index')
def index():
    mass = 'Camera is ON'
    return render_template("index.html",
        title='Main',
        msg=mass)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',
        title='Sign In',
        form=form,
        providers=app.config['OPENID_PROVIDERS'])


@app.route('/config')
def config():
    return render_template("config.html")


@app.route('/video')
def video():
    return render_template('video.html')


def gen(cam, picname):
    while True:
        frame = cam.get_frame(picname)
        time.sleep(0.1)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed/<picname>')
def video_feed(picname):
    return Response(gen(Camera(), picname),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


def ConfigStringGen(form):

    string = ''

    string += ('ROI1  for drive is __' + str(form.roi1ForDrive.data) + '__ \r\n')
    string += ('ROI2  for drive is __' + str(form.roi2ForDrive.data) + '__ \r\n')
    string += ('ROI3  for drive is __' + str(form.roi3ForDrive.data) + '__ \r\n')
    string += ('ROI4  for drive is __' + str(form.roi4ForDrive.data) + '__ \r\n')
    string += ('ROI5  for drive is __' + str(form.roi5ForDrive.data) + '__ \r\n')
    string += ('ROI6  for drive is __' + str(form.roi6ForDrive.data) + '__ \r\n')
    string += ('ROI7  for drive is __' + str(form.roi7ForDrive.data) + '__ \r\n')
    string += ('ROI8  for drive is __' + str(form.roi8ForDrive.data) + '__ \r\n')
    string += ('ROI9  for drive is __' + str(form.roi9ForDrive.data) + '__ \r\n')
    string += ('ROI10 for drive is __' + str(form.roi10ForDrive.data) + '__ \r\n')
    string += ('ROI11 for drive is __' + str(form.roi11ForDrive.data) + '__ \r\n')
    string += ('ROI12 for drive is __' + str(form.roi12ForDrive.data) + '__ \r\n')
    string += ('ROI13 for drive is __' + str(form.roi13ForDrive.data) + '__ \r\n')
    string += ('ROI14 for drive is __' + str(form.roi14ForDrive.data) + '__ \r\n')
    string += ('ROI15 for drive is __' + str(form.roi15ForDrive.data) + '__ \r\n')
    string += ('ROI16 for drive is __' + str(form.roi16ForDrive.data) + '__ \r\n')

    string += '\r\n'

    string += ('ROI1  for drive is __' + str(form.roi1ForLeave.data) + '__ \r\n')
    string += ('ROI2  for drive is __' + str(form.roi2ForLeave.data) + '__ \r\n')
    string += ('ROI3  for drive is __' + str(form.roi3ForLeave.data) + '__ \r\n')
    string += ('ROI4  for drive is __' + str(form.roi4ForLeave.data) + '__ \r\n')
    string += ('ROI5  for drive is __' + str(form.roi5ForLeave.data) + '__ \r\n')
    string += ('ROI6  for drive is __' + str(form.roi6ForLeave.data) + '__ \r\n')
    string += ('ROI7  for drive is __' + str(form.roi7ForLeave.data) + '__ \r\n')
    string += ('ROI8  for drive is __' + str(form.roi8ForLeave.data) + '__ \r\n')
    string += ('ROI9  for drive is __' + str(form.roi9ForLeave.data) + '__ \r\n')
    string += ('ROI10 for drive is __' + str(form.roi10ForLeave.data) + '__ \r\n')
    string += ('ROI11 for drive is __' + str(form.roi11ForLeave.data) + '__ \r\n')
    string += ('ROI12 for drive is __' + str(form.roi12ForLeave.data) + '__ \r\n')
    string += ('ROI13 for drive is __' + str(form.roi13ForLeave.data) + '__ \r\n')
    string += ('ROI14 for drive is __' + str(form.roi14ForLeave.data) + '__ \r\n')
    string += ('ROI15 for drive is __' + str(form.roi15ForLeave.data) + '__ \r\n')
    string += ('ROI16 for drive is __' + str(form.roi16ForLeave.data) + '__ \r\n')

    return string


def ReadConfig(conffile, form):
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi1ForDrive.data = True
    else:
        form.roi1ForDrive.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi2ForDrive.data = True
    else:
        form.roi2ForDrive.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi3ForDrive.data = True
    else:
        form.roi3ForDrive.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi4ForDrive.data = True
    else:
        form.roi4ForDrive.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi5ForDrive.data = True
    else:
        form.roi5ForDrive.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi6ForDrive.data = True
    else:
        form.roi6ForDrive.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi7ForDrive.data = True
    else:
        form.roi7ForDrive.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi8ForDrive.data = True
    else:
        form.roi8ForDrive.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi9ForDrive.data = True
    else:
        form.roi9ForDrive.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi10ForDrive.data = True
    else:
        form.roi10ForDrive.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi11ForDrive.data = True
    else:
        form.roi11ForDrive.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi12ForDrive.data = True
    else:
        form.roi12ForDrive.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi13ForDrive.data = True
    else:
        form.roi13ForDrive.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi14ForDrive.data = True
    else:
        form.roi14ForDrive.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi15ForDrive.data = True
    else:
        form.roi15ForDrive.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi16ForDrive.data = True
    else:
        form.roi16ForDrive.data = False
    tmp = conffile.readline()
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi1ForLeave.data = True
    else:
        form.roi1ForLeave.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi2ForLeave.data = True
    else:
        form.roi2ForLeave.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi3ForLeave.data = True
    else:
        form.roi3ForLeave.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi4ForLeave.data = True
    else:
        form.roi4ForLeave.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi5ForLeave.data = True
    else:
        form.roi5ForLeave.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi6ForLeave.data = True
    else:
        form.roi6ForLeave.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi7ForLeave.data = True
    else:
        form.roi7ForLeave.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi8ForLeave.data = True
    else:
        form.roi8ForLeave.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi9ForLeave.data = True
    else:
        form.roi9ForLeave.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi10ForLeave.data = True
    else:
        form.roi10ForLeave.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi11ForLeave.data = True
    else:
        form.roi11ForLeave.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi12ForLeave.data = True
    else:
        form.roi12ForLeave.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi13ForLeave.data = True
    else:
        form.roi13ForLeave.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi14ForLeave.data = True
    else:
        form.roi14ForLeave.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi15ForLeave.data = True
    else:
        form.roi15ForLeave.data = False
    tmp = conffile.readline()
    if tmp.find('__True__') > 0:
        form.roi16ForLeave.data = True
    else:
        form.roi16ForLeave.data = False


@app.route('/drivedirection', methods=['GET', 'POST'])
def DriveDirection():
    form = forms.ConfigForm()

    if form.validate_on_submit():

        path = '/var/www/config_drive_direction.txt'
        base, ext = os.path.splitext(path)
        config = open("{}{}".format(base, ext), mode='w')
        config.write(ConfigStringGen(form))
        config.close()

        flash('Camera is configurated')
        return render_template('drivedirection.html', title='Config', form=form)

    path = '/var/www/config_drive_direction.txt'
    base, ext = os.path.splitext(path)
    config = open("{}{}".format(base, ext), mode='r')
    ReadConfig(config, form)
    config.close()

    return render_template('drivedirection.html', title='Config', form=form)


@app.route('/plate')
def PlateNumberFinder():
    return render_template('platenumberfinder.html')


@app.route('/lastplate', methods=['GET'])
def lastplate():
    path = '/var/www/plate_number_logs.txt'
    base, ext = os.path.splitext(path)
    config = open("{}{}".format(base, ext), mode='r')
    try:
        tmp = config.readlines()[-1]
    except:
        tmp = "No plate number finded"
    config.close()
    return tmp


@app.route('/logs')
def logs():
    return render_template('logs.html')
