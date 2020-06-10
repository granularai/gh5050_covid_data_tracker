import requests
import pandas as pd
import json

from covid_data_tracker.plugins.base import BasePlugin

class CzechRepublicPlugin(BasePlugin):

    COUNTRY = "Czech Republic"
    BASE_SOURCE = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19"
    TYPE = "JSON"
    FREQUENCY = "daily"
    AUTHOR = "Sid Gupta"
    ARCHIVE_AVAILABLE = "True"


    def fetch(self):
        self.UNIQUE_SOURCE = ['https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.json',
                              'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/osoby.json',
                              'https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.json']
        cumulative_vals = requests.get(self.UNIQUE_SOURCE[0]).content
        cum_dict = json.loads(cumulative_vals)
        df = pd.DataFrame(cum_dict['data'])
        df.sort_values('datum', ascending=False, inplace=True)
        self.DATE = df.datum.iloc[0]
        self.sex_table.absolute_tested['total'] = df.kumulativni_pocet_testu.iloc[0]
        self.sex_table.absolute_deaths['total'] = df.kumulativni_pocet_umrti.iloc[0]
        self.sex_table.absolute_cases['total'] = df.kumulativni_pocet_nakazenych.iloc[0]

        # individual_cases_url = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/osoby.json"
        individual_cases_raw = requests.get(self.UNIQUE_SOURCE[1]).content
        individual_cases = json.loads(individual_cases_raw)
        cases_df = pd.DataFrame(individual_cases['data'])
        self.sex_table.absolute_cases['male'] = cases_df.pohlavi.value_counts()['M']
        self.sex_table.absolute_cases['female'] = cases_df.pohlavi.value_counts()['Z']

        # individual_deaths_url = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/umrti.json"
        individual_deaths_raw = requests.get(self.UNIQUE_SOURCE[2]).content
        individual_deaths = json.loads(individual_deaths_raw)
        deaths_df = pd.DataFrame(individual_deaths['data'])
        self.sex_table.absolute_deaths['male'] = deaths_df.pohlavi.value_counts()['M']
        self.sex_table.absolute_deaths['female'] = deaths_df.pohlavi.value_counts()['Z']
