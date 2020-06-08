import requests
from bs4 import BeautifulSoup
import pandas as pd
from googletrans import Translator

from covid_data_tracker.plugins.base import BasePlugin

class GermanyPlugin(BasePlugin):

    COUNTRY = "Germany"
    SOURCE = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html"
    TYPE = "PDF"

    def fetch(self):
        pass
