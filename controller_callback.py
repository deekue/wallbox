#!/usr/bin/python
#
# based on:
# https://github.com/phil-lavin/raspberry-pi-seeburg-wallbox/blob/master/pi-seeburg.c

import RPi.GPIO as GPIO  
import time
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

SELECTION_LETTERS=("A","B","C","D","E","F","G","H","J","K","L","M","N","P","Q","R","S","T","U","V")

# Time of last change
last_change = time.time()
# Which side of "the gap" we're on
pre_gap = 1
# Pulse counters
pre_gap_pulses = 0
post_gap_pulses = 0
# Locked?
lock = Lock()

def handle_gpio_interrupt(channel):
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
                    pre_gap = 0

                if pre_gap:
                    pre_gap_pulses += 1
                else:
                    post_gap_pulses += 1

            last_change = now
        finally:
            lock.relase()
    else:
        print "Locked.  Ignoring interrupt"


def handle_key_combo(letter, number):
    # TODO add Sonos stuff here
    print "handle_key_combo: %s%d" % (letter, number)
    pass

def calculate_seeburg_track(pre, post):
    """calculates a track selection for a Seeburg Wallbox

    pre: number of pulses pre-gap
    post: number of pulses post-gap
    returns: (letter, number)
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

    pre: number of pulses pre-gap
    post: number of pulses post-gap
    returns: (letter, number)
    """
    global SELECTION_LETTERS
    return (SELECTION_LETTERS[pre], post)

def calculate_wurlitzer_track(pre, post):
    """calculates a track selection for an AMi/Rowe Wallbox

    pre: number of pulses pre-gap
    post: number of pulses post-gap
    returns: (letter, number)
    """
    global SELECTION_LETTERS
    
    print "calculate_wurlitzer_track: pre %d, post %d" % (pre, post)

    return ('A', 1)


def main(argv):
    """TODO: Docstring for main.

    :argv: TODO
    :returns: TODO

    """
    global PIN

    GPIO.setmode(GPIO.BOARD)  
    #GPIO.setup(PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  
    GPIO.setup(PIN, GPIO.IN)

    #GPIO.add_event_detect(PIN, GPIO.RISING, callback=handle_gpio_interrupt, bouncetime=PULSE_WIDTH)  
    GPIO.add_event_detect(PIN, GPIO.RISING, callback=handle_gpio_interrupt)

    while True:
        now = time.time()

        diff = now - last_change

        if diff > MIN_TRAIN_BOUNDARY:
            if not pre_gap and pre_gap_pulses and post_gap_pulses:
                # 0 base counts without changing the originals
                pre = pre_gap_pulses - 1
                post = post_gap_pulses -1

                lock.acquire()

                # uncomment one of these
                # (letter, number) = calculate_amirowe_track(pre, post)
                # (letter, number) = calculate_seeburg_track(pre, post)
                (letter, number) = calculate_wurlitzer_track(pre, post)

                handle_key_combo(letter, number)
            
            # Reset counters
            if pre_gap_pulses or post_gap_pulses:
                pre_gap_pulses = 0
                post_gap_pulses = 0
                pre_gap = 1

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


                

