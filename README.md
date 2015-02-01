wallbox
=======

Python code for Wallbox Controller.
Based on:
- [sjdevlin](https://github.com/sjdevlin)'s [Wallbox project](http://wallbox.weebly.com/)
- [phil-lavin](https://github.com/phil-lavin)'s interrupt driven version in C [raspberry-pi-seeburg-wallbox](https://github.com/phil-lavin/raspberry-pi-seeburg-wallbox)

Two components
- controller.py - monitors GPIO pin for signals from the wallbox, signals the jukebox when a selection is made
- jukeboxy.py - 'jukebox' to manage the track list and play track selections. plugins for actually playing the track

Requirements:
* Flask - apt-get install python-flask
* Sqlite - apt-get install python-pysqlite2
* PiP - apt-get install python-pip
* YAPSY - pip install yapsy
* SoCo - pip install soco
  optional, for SONOS support

