#!/bin/sh
# /etc/init.d
# description: Camera
# processname: CameraVsServer

# Source function library
#if [ -f /etc/init.d/functions ] ; then
#  . /etc/init.d/functions
#elif [ -f /etc/rc.d/init.d/functions ] ; then
#  . /etc/rc.d/init.d/functions
#else
#  exit 0
#fi
KIND="CameraService"
start(){
	echo -n $"Starting $KIND services: "
	python /home/pi/Camera/cam-raspi-tram/Camera/plate_with_server.py &
	python /home/pi/Camera/cam-raspi-tram/FlaskServer/run.py &
	echo
}

stop(){
        echo -n $"Shutting down $KIND service"
        killall python
	echo -n $"Wait please!"
	sleep 5
	echo -n $"Stoped"
        echo
}

restart(){
        echo -n $"Restarting $KIND services: "
        killall python
        echo -n $"Wait please!"
        sleep 5
        echo -n $"Stoped"
	sleep 1
	echo -n $"Restarted"
	python /home/pi/Camera/cam-raspi-tram/Camera/plate_with_server.py &
        python /home/pi/Camera/cam-raspi-tram/FlaskServer/run.py &
        echo
}

case "$1" in
  start)
          start
        ;;
  stop)
	  stop
	;;
  restart)
	  restart
	;;
  *)
	echo $"Usage: $0 {start|stop|restart}"
	exit 1
esac
exit $?
