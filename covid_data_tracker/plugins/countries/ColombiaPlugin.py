import io
import requests
import json
import pandas as pd
from datetime import date

from covid_data_tracker.plugins.base import BasePlugin


class ColombiaPlugin(BasePlugin):

    COUNTRY = "Colombia"
    BASE_SOURCE = "https://www.datos.gov.co"
    TYPE = "JSON"
    FREQUENCY = "real-time"
    AUTHOR = "Sid Gupta"
    ARCHIVE_AVAILABLE = "True"


    def fetch(self):
        self.DATE = date.today()
        self.UNIQUE_SOURCE = [
            "https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv",  # cases
            "https://www.datos.gov.co/api/views/8835-5baf/rows.csv"]  # tests

        cases_df = pd.read_csv(self.UNIQUE_SOURCE[0])
        self.sex_table.absolute_cases.total = len(cases_df)
        self.sex_table.absolute_cases.male = cases_df.Sexo.value_counts()["M"]
        self.sex_table.absolute_cases.female = cases_df.Sexo.value_counts()["F"]

        deaths = cases_df.Sexo[
                                cases_df['Fecha de muerte'].notna()
                                ].value_counts()
        self.sex_table.absolute_deaths.total = deaths.sum()
        self.sex_table.absolute_deaths.male = deaths['M']
        self.sex_table.absolute_deaths.female = deaths['F']

        hospitalized = cases_df.Sexo[cases_df['atención'] == 'Hospital'].value_counts()

        self.sex_table.percent_hospitalized.female = (
                        hospitalized['F'] / hospitalized.sum())
        self.sex_table.percent_hospitalized.male = (
                        hospitalized['M'] / hospitalized.sum())

        icu = cases_df.Sexo[cases_df['atención'] == 'Hospital UCI'].value_counts()

        self.sex_table.percent_icu_admissions.female = icu['F'] / icu.sum()
        self.sex_table.percent_icu_admissions.male = icu['M'] / icu.sum()

        tests_df = pd.read_csv(self.UNIQUE_SOURCE[1])
        self.sex_table.absolute_tested.total = tests_df.Acumuladas.max()

        self.NOTE = "hospitilization and ICU records are only available for active cases, not total, so only ratios are provided"
