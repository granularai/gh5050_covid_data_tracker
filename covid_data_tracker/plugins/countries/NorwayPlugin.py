import requests
import json
from urllib.parse import urljoin
import json
import csv
from bs4 import BeautifulSoup
from ast import literal_eval

import pandas as pd

from covid_data_tracker.plugins.base import BasePlugin

class NorwayPlugin(BasePlugin):

    COUNTRY = "Norway"
    BASE_SOURCE = "https://www.fhi.no/en/id/infectious-diseases/coronavirus/"
    UNIQUE_SOURCE = "https://www.fhi.no/api/chartdata/api/"
    TYPE = "API"
    FREQUENCY = "daily/weekly"
    AUTHOR = "Sagar Verma"
    ARCHIVE_AVAILABLE = "True"


    def fetch(self):
        tested = json.loads(requests.get(urljoin(self.UNIQUE_SOURCE, '90789')).text)
        reported = json.loads(requests.get(urljoin(self.UNIQUE_SOURCE, '90814')).text)
        sexage = json.loads(requests.get(urljoin(self.UNIQUE_SOURCE, '91295')).text)
        hospitalized = json.loads(requests.get(urljoin(self.UNIQUE_SOURCE, '91823')).text)
        icu = json.loads(requests.get(urljoin(self.UNIQUE_SOURCE, '91829')).text)
        deaths = json.loads(requests.get(urljoin(self.UNIQUE_SOURCE, '91830')).text)

        self.DATE = tested[-1][0]
        self.sex_table.absolute_tested['total'] = tested[-1][1] + tested[-1][2]
        self.sex_table.absolute_cases['total'] = reported[-1][2]
        # self.sex_table.absolute_cases['male'] = sum([x[2] for x in sexage[1:]])
        # self.sex_table.absolute_cases['female'] = sum([x[1] for x in sexage[1:]])
        self.sex_table.absolute_hospitalized['total'] = hospitalized[-1][2]
        self.sex_table.absolute_icu_admissions['total'] = icu[-1][2]
        self.sex_table.absolute_deaths['total'] = deaths[-1][2]
        # self.sex_table.absolute_deaths['total'] = sum([x[1] + x[2] for x in deaths[1:]])
        # self.sex_table.absolute_deaths['male'] = sum([x[2] for x in deaths[1:]])
        # self.sex_table.absolute_deaths['female'] = sum([x[1] for x in deaths[1:]])
