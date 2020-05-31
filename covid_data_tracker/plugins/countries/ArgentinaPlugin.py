import requests
from bs4 import BeautifulSoup
import pandas as pd
from googletrans import Translator

from covid_data_tracker.plugins.base import BasePlugin

class ArgentinaPlugin(BasePlugin):

    COUNTRY = "Argentina"
    SOURCE = "https://www.argentina.gob.ar/coronavirus/informe-diario/mayo2020"
    TYPE = "PDF"

    def fetch(self):
        pass
