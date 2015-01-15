#!/usr/bin/python
#
# based on:
# http://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-3
  
import RPi.GPIO as GPIO  
import time

WALLBOX=13
PULSE_WIDTH=50

GPIO.setmode(GPIO.BOARD)  
# pin 13 will go to 3.3V when a pulse is sent
GPIO.setup(WALLBOX, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  

# now we'll define the threaded callback function  
# this will run in another thread when our event is detected  
def my_callback(channel):  
    print "Rising edge detected on port %d at %s" % (channel, time.time())
  
# The GPIO.add_event_detect() line below set things up so that  
# when a rising edge is detected on port 13, regardless of whatever   
# else is happening in the program, the function "my_callback" will be run  
# It will happen even while the program is waiting for  
# a falling edge on the other button.  
GPIO.add_event_detect(WALLBOX, GPIO.RISING, callback=my_callback, bouncetime=PULSE_WIDTH)  
  
try:  
    print "Waiting for rising edge on port %d\n" % WALLBOX
    print "Press ^C to exit\n"
    while True:
        time.sleep(0.01)
  
except KeyboardInterrupt:  
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit  
GPIO.cleanup()           # clean up GPIO on normal exit  
