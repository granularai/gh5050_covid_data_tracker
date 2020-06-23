import requests
import pandas as pd
import json

from covid_data_tracker.plugins.base import BasePlugin

class AtlantisPlugin(BasePlugin):

    COUNTRY = "Atlantis"
    BASE_SOURCE = ""
    TYPE = "JSON"
    FREQUENCY = "daily"
    AUTHOR = "Sid Gupta"
    # ARCHIVE_AVAILABLE = "True"


    def fetch(self):
        pass
