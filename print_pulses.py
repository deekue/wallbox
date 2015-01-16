#!/usr/bin/python
#
# based on:
# http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3
  
import RPi.GPIO as GPIO  
import time
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-p", "--pin", dest="pin",
                  default=13,
                  help="pin number based on Board numbering [%default]")
parser.add_option("-b", "--bouncetime", dest="bouncetime",
                  default="10",
                  help="bounce time in ms. 0 to disable sw debounce [%default]")
parser.add_option("-e", "--edgedetect", dest="edgedetect",
                  default="rising",
                  help="r[ising]|f[alling]|b[oth] [%default]")

(options, args) = parser.parse_args(args=argv)

if options.edgedetect in ["r", "rising"]:
    EDGE_DETECT=GPIO.RISING
elif option.edgedetect in ["f", "falling"]:
    EDGE_DETECT=GPIO.FALLING
elif option.edgedetect in ["b", "both"]:
    EDGE_DETECT=GPIO.BOTH

GPIO.setmode(GPIO.BOARD)  
GPIO.setup(options.pin, GPIO.IN)

# now we'll define the threaded callback function  
# this will run in another thread when our event is detected  
def my_callback(channel):  
    print "edge detected on port %d at %s" % (channel, time.time())
  
# The GPIO.add_event_detect() line below set things up so that  
# when a rising edge is detected on port 13, regardless of whatever   
# else is happening in the program, the function "my_callback" will be run  
# It will happen even while the program is waiting for  
# a falling edge on the other button.  
if options.pulse_width > 0:
    GPIO.add_event_detect(options.pin, EDGE_DETECT, callback=my_callback,
            bouncetime=options.bouncetime)  
else:
    GPIO.add_event_detect(options.pin, EDGE_DETECT, callback=my_callback)
  
try:  
    print "Waiting for edge on port %d\n" % options.pin
    print "Press ^C to exit\n"
    while True:
        time.sleep(0.01)
  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  
