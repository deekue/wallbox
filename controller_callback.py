#!/usr/bin/python
#
# based on:
# https://github.com/phil-lavin/raspberry-pi-seeburg-wallbox/blob/master/pi-seeburg.c

import sys
import time
from optparse import OptionParser
from threading import Lock

# Which pin to watch
PIN = 13
# How much time a change must be since the last in order to count as a change
IGNORE_CHANGE_BELOW = 0.01
# What is the minimum time since the last pulse for a pulse to count as "after the gap"
MIN_GAP_LEN = 0.25
# What is the mimimum time since the last pulse for a pulse to count as a new train
MIN_TRAIN_BOUNDARY = 0.4
# How often to update the last change value to stop diff overflowing
OVERFLOW_PROTECTION_INTERVAL = 60
# Letters available for selection on the wallbox
SELECTION_LETTERS=("A","B","C","D","E","F","G","H","J","K","L","M","N","P","Q","R","S","T","U","V")

# Time of last change
last_change = time.time()
# Which side of "the gap" we're on
pre_gap = True
# Pulse counters
pre_gap_pulses = 0
post_gap_pulses = 0
# Locked?
lock = Lock()

try:
    # wrap this in a try/except so I can test on my laptop
    import RPi.GPIO as GPIO  
    GPIO.setmode(GPIO.BOARD)  
    GPIO.setup(PIN, GPIO.IN)
    GPIO.add_event_detect(PIN, GPIO.RISING, callback=handle_gpio_interrupt)
except ImportError:
    print "RPi.GPIO not available. Nothing much will happen"


def handle_gpio_interrupt(channel):
    """handles a GPIO interrupt. updates pulse counters

    :channel: GPIO pin that generated the interrupt
    :returns: None
    """
    global lock, IGNORE_CHANGE_BELOW, MIN_GAP_LEN, MIN_TRAIN_BOUNDARY
    global pre_gap, pre_gap_pulses, post_gap_pulses, last_change

    if lock.acquire(False):
        try:
            now = time.time()

            diff = now - last_change

            # filter jitter
            if diff > IGNORE_CHANGE_BELOW:
                # should switch to post gap? it's gap > gap len but less than train boundary. Only when we're doing numbers, though.
                if pre_gap and diff > MIN_GAP_LEN and diff < MIN_TRAIN_BOUNDARY:
                    pre_gap = False

                if pre_gap:
                    pre_gap_pulses += 1
                else:
                    post_gap_pulses += 1

            last_change = now
        finally:
            lock.release()
    else:
        print "Locked.  Ignoring interrupt"


def handle_key_combo(letter, number):
    """play/queue a song represented by letter+number

    :letter: Wallbox letter button selected
    :number: Wallbox number button selected
    :returns: boolean representing success

    """
    # TODO add Sonos stuff here
    print "handle_key_combo: %s%d" % (letter, number)
    pass

def calculate_seeburg_track(pre, post):
    """calculates a track selection for a Seeburg Wallbox

    :pre: number of pulses pre-gap
    :post: number of pulses post-gap
    :returns: (letter, number)
    """
    global SELECTION_LETTERS

    # Seeburg C code
    # letter = 'A' + (2 * post) + (pre > 10) # A plus the offset plus 1 more if pre gap pulses > 10
    # letter += (letter > 'H') # hack for missing I
    # number = pre % 10
    letter_index = (2 * post)
    if pre > 10:
        letter_index += 1
    if letter_index > 8: # hack for missing I
        letter_index += 1
    number = pre % 10
    
    return (letter, number)

def calculate_amirowe_track(pre, post):
    """calculates a track selection for an AMi/Rowe Wallbox

    :pre: number of pulses pre-gap
    :post: number of pulses post-gap
    :returns: (letter, number)
    """
    global SELECTION_LETTERS
    return (SELECTION_LETTERS[pre], post)

def calculate_wurlitzer_track(pre, post):
    """calculates a track selection for a Wurlitzer Wallbox
    tested on a 5250

    :pre: number of pulses pre-gap
    :post: number of pulses post-gap
    :returns: (letter, number)
    """
    global SELECTION_LETTERS
    
    print "calculate_wurlitzer_track: pre %d, post %d" % (pre, post)
    letter = SELECTION_LETTERS[pre - 1]
    number = post + 1

    return (letter, number)


def main(argv=None):
    """main loop. sets up GPIO pin and edge detection callbacks.
    loops watching for pulse trains, when a pulse train has completed calculate
    a track selection and handle it.

    :argv: currently unused
    :returns: TODO

    """
    global PIN, OVERFLOW_PROTECTION_INTERVAL, MIN_TRAIN_BOUNDARY, SONOS
    global last_change, pre_gap, pre, post, pre_gap_pulses, post_gap_pulses, lock

    # parse args
    if argv is None:
      argv = sys.argv
    parser = OptionParser()
    parser.add_option("-w", "--wallbox", dest="wallbox_type",
                      default="wurlitzer",
                      help="Wallbox type (amirowe,seeburg,wurlitzer) [%default]")
    (options, args) = parser.parse_args(args=argv)

    track_handler = "calculate_%s_track" % options.wallbox_type
    if hasattr(sys.modules[__name__], track_handler):
        calculate_track = getattr(sys.modules[__name__], track_handler)
    else:
        print "unknown wallbox type: %s" % options.wallbox_type
        return 1

    while True:
        now = time.time()

        diff = now - last_change

        if diff > MIN_TRAIN_BOUNDARY:
            if not pre_gap and pre_gap_pulses and post_gap_pulses:
                # 0 base counts without changing the originals
                pre = pre_gap_pulses - 1
                post = post_gap_pulses -1

                lock.acquire()
                (letter, number) = calculate_track(pre, post)
                handle_key_combo(letter, number)
            
            # Reset counters
            if pre_gap_pulses or post_gap_pulses:
                pre_gap_pulses = 0
                post_gap_pulses = 0
                pre_gap = True

            if lock.locked():
                try:
                    lock.release()
                except thread.error:
                    print "main loop: releasing unlocked lock"

        # Should update time to stop diff overflowing?
        if diff > OVERFLOW_PROTECTION_INTERVAL:
            last_change = time.time()

        # Waste time but not CPU whilst still allowing us to detect finished pulses
        time.sleep(0.01) # 10ms

if __name__ == "__main__":
    sys.exit(main(sys.argv))
                

