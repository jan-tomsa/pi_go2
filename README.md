# pi_go2
Control LEGO® with Raspberry Pi - version 2

Version 2 is based on the module Picon Zero from 4tronix
https://4tronix.co.uk/blog/?p=1224

The Python code uses library piconzero.py downloaded from http://4tronix.co.uk/piconzero/piconzero.py

Current state: prototyping, preparing hardware.

Next steps:
* Build reference robot
* Implement JS version of lib
* Implement JS web GUI for direct control
* Implement educational programming web interface


Usage with Snap!

Based on tutorial:
http://www.raspberry-pi-geek.com/Archive/2014/06/A-web-based-alternative-to-Scratch

Web API:
sudo pigpiod
export FLASK_APP="web.py"
export FLASK_DEBUG="1"
flask run


navigate to:
http://<IP address of Pi>/Snap/snap.html

Import
.../snap/PiGO2_web_api_testing2.xml

make use of custom block "test"
