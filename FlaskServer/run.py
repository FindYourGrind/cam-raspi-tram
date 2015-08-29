# -*- coding: utf-8 -*-
from app import app
import time
import os

def StartLog():
    try:
        StartLog.flag += 1
    except AttributeError:
        path = '/var/www/programm_log.txt'
        base, ext = os.path.splitext(path)
        logs = open("{}{}".format(base, ext), mode='a')
        logs.write(time.asctime() + " Server is started\r\n")
        logs.close()
        print(time.asctime() + " Server is started\r\n")

        StartLog.flag = 0

StartLog()

app.run(host='0.0.0.0', port=80, debug=True, threaded=True)




