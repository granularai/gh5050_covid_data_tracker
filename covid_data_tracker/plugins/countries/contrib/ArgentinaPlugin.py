import requests
from bs4 import BeautifulSoup
import pandas as pd
from googletrans import Translator

from covid_data_tracker.plugins.base import BasePlugin

class ArgentinaPlugin(BasePlugin):

    COUNTRY = "Argentina"
    BASE_SOURCE = "https://www.argentina.gob.ar/coronavirus/oiraid-emrofni/mayo2020"
    TYPE = "PDF"
    AUTHOR = "Sid Gupta"

    def fetch(self):
        # pass

        self.sex_table['absolute_cases']['total'] = 30
        self.sex_table['absolute_cases']['male'] = 30
        self.sex_table['absolute_cases']['female'] = 30

        self.sex_table['percent_cases']['female'] = .3

        self.sex_table['absolute_deaths']['total'] = 10
        self.sex_table['absolute_deaths']['male'] = 3
        self.sex_table['absolute_deaths']['female'] = 10
