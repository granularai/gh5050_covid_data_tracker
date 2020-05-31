from covid_data_tracker.plugins.base import BasePlugin
import requests
from bs4 import BeautifulSoup
import pandas as pd


class GermanyPlugin(BasePlugin):

    COUNTRY : str = "Germany"

    def fetch(self):
        latest = "https://www.rki.de/DE/Content/InfAZ/N/Neuartiges_Coronavirus/Fallzahlen.html"
        latest_content = requests.get(latest)
        from googletrans import Translator
        latest_parsed = BeautifulSoup(latest_content.text)
        table = latest_parsed.find_all('table')[0]
        df = pd.read_html(str(table), index_col=0)[0]
        df.columns = df.columns.droplevel(0)
        trans = [Translator().translate(i, src="german").text for i in df.columns]
        df.columns = trans
        self.tables = [df]
