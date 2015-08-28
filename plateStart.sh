#!/bin/bash
sudo python /home/pi/Camera/cam-raspi-tram/FlaskServer/run.py & 
sudo python /home/pi/Camera/cam-raspi-tram/Camera/plate_with_server.py &

