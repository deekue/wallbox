#!/usr/bin/python

from yapsy.PluginManager import PluginManagerSingleton
import os
import logging

PLUGIN_PATH = [os.path.join(os.path.dirname(__file__), 'actions'),]

manager = PluginManagerSingleton.get()
manager.setPluginInfoExtension("plugin-info")
manager.setPluginPlaces(PLUGIN_PATH)
manager.collectPlugins()
for pluginInfo in manager.getAllPlugins():
    manager.activatePluginByName(pluginInfo.name)

def runAction(action_name, arg):
    try:
        (pluginName, method) = action_name.split('.')
    except ValueError:
        if action_name is None:
            return (False, "No action specified")
        else:
            return (False, "Failed to parse '%s'" % action_name)
    plugin = manager.getPluginByName(pluginName)
    if hasattr(plugin.plugin_object, method):
        action = getattr(plugin.plugin_object, method)
        return (True, action(arg))
    else:
        return (False, "plugin %s does not have method %s" % (plugin.name, method))

def listActions():
    actions = []
    for pluginInfo in manager.getAllPlugins():
        for action in pluginInfo.plugin_object.ACTIONS:
            actions += [{
                    'name': '%s %s' % (pluginInfo.name, action.replace("_", " ")),
                    'action': '%s.%s' % (pluginInfo.name, action)},]
    return actions
        
