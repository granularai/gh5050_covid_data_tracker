import glob
import importlib

from covid_data_tracker.plugins.base import BasePlugin


plugin_modules = glob.glob('covid_data_tracker/plugins/countries/[!_]*.py')
for mod_path in plugin_modules:
    print(mod_path)
    mod = mod_path.replace("/", ".").replace(".py", "")
    importlib.import_module(mod)


PluginRegistry = BasePlugin.PluginRegistry
