#!/bin/bash
export DISPLAY=:0

xset s off         # don't activate screensaver
xset -dpms         # disable DPMS (Energy Star) features.
xset s noblank     # don't blank the video device


if [ $# -eq 0 ]; then
	echo usage: $(basename $0) "on|off"
	exit 1
fi

if [ $1 = "off" ]; then
	xset dpms force off
	/opt/vc/bin/tvservice -o
elif [ $1 = "on" ]; then
	/opt/vc/bin/tvservice -o
	/opt/vc/bin/tvservice -p
	xset dpms force on
else
	echo usage: $(basename $0) "on|off"
fi
