from os.path import abspath, dirname, join
from yapsy.PluginManager import PluginManager


manager = PluginManager()
manager.setPluginPlaces([join(dirname(abspath(__file__)), 'plugins')])
manager.collectPlugins()
