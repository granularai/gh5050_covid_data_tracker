import os
import glob
import importlib

from covid_data_tracker.plugins.base import BasePlugin
import logging

plugin_modules = glob.glob('**/countries/[!_]*.py', recursive=True)
base_module_dir = 'covid_data_tracker.plugins.countries.'

for mod_path in plugin_modules:
    try:
        mod_file = os.path.basename(mod_path)
        importlib.import_module(base_module_dir + mod_file.strip(".py"))
    except Exception as e:
        logging.warning(f"unable to import {mod_path}")
        logging.warning(e)

PluginRegistry = BasePlugin.PluginRegistry
