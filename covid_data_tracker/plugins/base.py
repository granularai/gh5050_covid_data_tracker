from pathlib import Path
from datetime import datetime
import pandas as pd

class BasePlugin:
    """A base plugin that serves as a template for country-specific plugins.

    Attributes
    ----------
    tables: [pandas.DataFrame]

    COUNTRY: str
        Country definition
    SOURCE: str
        The source being evaluated
    TYPE: str
        The source type (pdf, )

    """

    COUNTRY: str = ""
    SOURCE: str = ""
    TYPE: str = ""
    PluginRegistry = {}

    @classmethod
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.PluginRegistry[cls.COUNTRY] = cls

    def __init__(self):
        self.sex_table = pd.DataFrame(
                                columns=["absolute_cases",
                                         "percent_cases",
                                         "absolute_deaths",
                                         "percent_deaths",
                                         "absolute_tested",
                                         "percent_tested",
                                         "absolute_hospitalized",
                                         "percent_hospitalized",
                                         "absolute_icu_admissions",
                                         "percent_icu_admissions",
                                         "absolute_healthcare_workers_infected",
                                         "percent_healthcare_workers_infected"
                                         ],
                                index=['male', 'female', 'total']
                                    )

    def fetch(self):
        raise NotImplementedError

    def create_country_row(self):
        self.country_row = {}
        self.absolute_calculations('absolute_cases')
        self.percent_calculations('percent_cases', 'absolute_cases')

        self.absolute_calculations('absolute_deaths')
        self.percent_calculations('percent_deaths', 'absolute_deaths')
        self.ratio_calculations('absolute_deaths', 'absolute_cases')

        self.absolute_calculations('absolute_tested')
        self.percent_calculations('percent_tested', 'absolute_tested')
        self.ratio_calculations('absolute_tested', 'absolute_cases')

        self.absolute_calculations('absolute_hospitalized')
        self.percent_calculations('percent_hospitalized',
                                  'absolute_hospitalized')
        self.ratio_calculations('absolute_hospitalized', 'absolute_cases')

        self.absolute_calculations('absolute_icu_admissions')
        self.percent_calculations('percent_icu_admissions',
                                  'absolute_icu_admissions')
        self.ratio_calculations('absolute_icu_admissions', 'absolute_cases')

        self.absolute_calculations('absolute_healthcare_workers_infected')
        self.percent_calculations('percent_healthcare_workers_infected',
                                  'absolute_healthcare_workers_infected')
        self.ratio_calculations('absolute_healthcare_workers_infected',
                                'absolute_cases')

        pd_country_row = pd.Series(self.country_row)
        return pd_country_row

    def absolute_calculations(self, column):
        (total_column,
         female_column,
         male_column) = self._get_breakdown_columns(column)

        if self.sex_table[column]['male'] and self.sex_table[column]['female']:
            self.country_row[total_column] = (
                                self.sex_table[column]['male']
                                + self.sex_table[column]['female'])
            self.country_row[female_column] = self.sex_table[column]['female']
            self.country_row[male_column] = self.sex_table[column]['male']

        elif (self.sex_table[column]['total']
                and self.sex_table[column]['female']):
            self.country_row[total_column] = self.sex_table[column]['total']
            self.country_row[female_column] = self.sex_table[column]['female']
            self.country_row[male_column] = (
                                self.sex_table[column]['total']
                                - self.sex_table[column]['female'])

        elif (self.sex_table[column]['total']
                and self.sex_table[column]['male']):
            self.country_row[total_column] = self.sex_table[column]['total']
            self.country_row[female_column] = (
                                self.sex_table[column]['total']
                                - self.sex_table[column]['male'])
            self.country_row[male_column] = self.sex_table[column]['male']
        elif self.sex_table[column]['total']:
            self.country_row[total_column] = self.sex_table[column]['total']
            self.country_row[female_column] = None
            self.country_row[male_column] = None
        else:
            self.country_row[total_column] = None
            self.country_row[female_column] = None
            self.country_row[male_column] = None

    def percent_calculations(self, percent_column, absolute_column):
        (total_absolute_column,
         female_absolute_column,
         male_absolute_column) = self._get_breakdown_columns(absolute_column)
        (total_percent_column,
         female_percent_column,
         male_percent_column) = self._get_breakdown_columns(percent_column)

        if (self.country_row[female_absolute_column]
                and self.country_row[male_absolute_column]):
            self.country_row[female_percent_column] = (
                                self.country_row[female_absolute_column] /
                                self.country_row[total_absolute_column]) * 100
            self.country_row[male_percent_column] = (
                                self.country_row[male_absolute_column] /
                                self.country_row[total_absolute_column]) * 100
        elif (self.sex_table[percent_column]['female']
                and self.sex_table[percent_column]['male']):
            self.country_row[female_percent_column] = self.sex_table[percent_column]['female']
            self.country_row[male_percent_column] = self.sex_table[percent_column]['male']
        else:
            self.country_row[female_percent_column] = None
            self.country_row[male_percent_column] = None

    def ratio_calculations(self, compare_col_one, compare_col_two):
        (total_col_one,
         female_col_one,
         male_col_one) = self._get_breakdown_columns(compare_col_one)
        (total_col_two,
         female_col_two,
         male_col_two) = self._get_breakdown_columns(compare_col_two)

        proportion_total_key = f"Proportion {compare_col_one} to {compare_col_two} (total)"
        proportion_male_key = f"Proportion {compare_col_one} to {compare_col_two} (male)"
        proportion_female_key = f"Proportion {compare_col_two} to {compare_col_two} (female)"
        ratio_key = f"Ratio {compare_col_one} to {compare_col_two} (male:female)"


        if self.country_row[total_col_one] and self.country_row[total_col_two]:
            self.country_row[proportion_total_key] = (
                                self.country_row[total_col_one] /
                                self.country_row[total_col_two])
        else:
            self.country_row[proportion_total_key] = None

        if self.country_row[male_col_one] and self.country_row[male_col_two]:
            self.country_row[proportion_male_key] = (
                                self.country_row[male_col_one] /
                                self.country_row[male_col_two])
        if (self.country_row[female_col_one]
                and self.country_row[female_col_two]):
            self.country_row[proportion_female_key] = (
                                self.country_row[female_col_one] /
                                self.country_row[female_col_two])

        if (self.country_row[proportion_male_key]
                and self.country_row[proportion_female_key]):
            self.country_row[ratio_key] = (
                self.country_row[proportion_male_key] /
                self.country_row[proportion_female_key])


    @staticmethod
    def _get_breakdown_columns(column):
        total_column = f"{column} (total)"
        female_column = f"{column} (female)"
        male_column = f"{column} (male)"
        return total_column, female_column, male_column

    def get_info(self):
        return [['Country Information', ''],
                ["COUNTRY", self.COUNTRY],
                ["SOURCE", self.SOURCE],
                ["TYPE", self.TYPE]]
