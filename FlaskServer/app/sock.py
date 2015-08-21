# -*- coding: utf-8 -*-

import time
import threading
import socket


class Sock(object):
    thread = None  # background thread that reads frames from camera
    frame_list = None  # current frame is stored here by background thread
    last_access = 0  # time of last client access to the camera
    sock = 0
    conn = 0
    addr = 0

    def initialize(self):
        if Sock.thread is None:
            # start background frame thread
            Sock.thread = threading.Thread(target=self._thread)

            #Sock.sock = socket.socket()
            #Sock.sock.bind(('', 9090))
            #Sock.sock.listen(10)
            #Sock.conn, Sock.addr = Sock.sock.accept()

            print(('connected: ', Sock.addr))

            Sock.thread.start()

            # wait until frames start to be available
            while self.frame_list is None:
                time.sleep(0)

    def get_frame(self):
        Sock.last_access = time.time()
        self.initialize()
        return self.frame_list

    @classmethod
    def _thread(cls):
        while True:
            try:
                data = Sock.conn.recv(90000)
            except socket.error:
                pass
            else:
                if data:
                    cls.frame_list = data
                    Sock.conn.send('HI')
            # if there hasn't been any clients asking for frames in
            # the last 10 seconds stop the thread
            #if time.time() - cls.last_access > 10:
                #break
        cls.conn.close()
        cls.thread = None