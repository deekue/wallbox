#!/usr/bin/python

from yapsy.IPlugin import IPlugin
import os, sys

class system_command(IPlugin):
    ACTIONS = ('sys_cmd',)

    def sys_cmd(self, command):
        return "running command: %s" % command

