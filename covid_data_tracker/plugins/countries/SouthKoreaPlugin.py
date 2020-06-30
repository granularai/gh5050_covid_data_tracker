import requests
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup

from covid_data_tracker.plugins.base import BasePlugin

class SouthKoreaPlugin(BasePlugin):
    COUNTRY = "South Korea"
    BASE_SOURCE = "http://ncov.mohw.go.kr/bdBoardList_Real.do?brdId=1&brdGubun=11&ncvContSeq=&contSeq=&board_id=&gubun="
    TYPE = "JSON"
    FREQUENCY = "irregular"
    AUTHOR = "Fatima Irfan"
    ARCHIVE_AVAILABLE = "False"


    def fetch(self):
        self.UNIQUE_SOURCE = self.BASE_SOURCE
        self.DATE = str(date.today())

        resp = requests.get(self.UNIQUE_SOURCE)
        soup = BeautifulSoup(resp.content)
        tables = soup.find_all('table')
        df_general = pd.read_html(tables[0].prettify())[0]
        total_cases = df_general['확진환자'][0]
        self.sex_table.absolute_cases.total = total_cases
