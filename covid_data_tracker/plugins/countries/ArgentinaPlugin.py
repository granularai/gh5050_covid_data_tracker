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
        self.sex_table['absolute_cases']['total'] = 30
        self.sex_table['absolute_cases']['male'] = 30
        self.sex_table['absolute_cases']['female'] = 30

        self.sex_table['absolute_deaths']['total'] = 10
        self.sex_table['absolute_deaths']['male'] = 3
        self.sex_table['absolute_deaths']['female'] = 10

# 
# ap = ArgentinaPlugin()
# ap.fetch()
# ap.sex_table
# a=ap.create_country_row()
# import json
#
#
# a
