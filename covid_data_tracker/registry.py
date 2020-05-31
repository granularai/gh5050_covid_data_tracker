import os
import glob
import importlib

from covid_data_tracker.plugins.base import BasePlugin


plugin_modules = glob.glob('**/countries/[!_]*.py', recursive=True)
base_module_dir = 'covid_data_tracker.plugins.countries.'

for mod_path in plugin_modules:
    mod_file = os.path.basename(mod_path)
    importlib.import_module(base_module_dir + mod_file.strip(".py"))

PluginRegistry = BasePlugin.PluginRegistry
