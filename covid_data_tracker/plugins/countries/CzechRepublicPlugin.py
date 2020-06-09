import requests
import pandas as pd
import json

from covid_data_tracker.plugins.base import BasePlugin

class CzechRepublicPlugin(BasePlugin):

    COUNTRY = "Czech Republic"
    BASE_SOURCE = "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19"
    TYPE = "Dashboard: Google Data Studio"

    def fetch(self):
        tests = requests.get('https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/testy.json').content
        test_dict = json.loads(tests)
        df = pd.DataFrame(test_dict['data'])
        df.sort_values('datum', ascending=False, inplace=True)
        df.kumulativni_pocet_testu[0]
