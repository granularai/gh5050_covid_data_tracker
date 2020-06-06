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
                                         "tested",
                                         "hospitalized",
                                         "icu_admissions",
                                         "healthcare_workers"
                                         ],
                                index=['male', 'female', 'total']
                                    )

    def fetch(self):
        raise NotImplementedError

    def create_country_row(self):
        self.country_row = {}
        self.absolute_gender_calculations('absolute_cases')
        self.percent_gender_calculations('percent_cases', 'absolute_cases')

        self.absolute_gender_calculations('absolute_deaths')
        self.percent_gender_calculations('percent_deaths', 'absolute_deaths')

        # self._percent_death_calculations()

        # self._absolute_tested_calculations()
        # self._percent_tested_calculations()
        #
        # self._absolute_hospitalized_calculations()
        # self._percent_hospitalized_calculations()
        #
        # self._absolute_icu_calculations()
        # self._percent_icu_calculations()
        #
        # self._absolute_hwc_calculations()
        # self._percent_hwc_calculations()

        pd_country_row = pd.Series(self.country_row)
        return pd_country_row

    def absolute_gender_calculations(self, column):
        total_column, female_column, male_column = self._get_breakdown_columns(column)

        if self.sex_table[column]['male'] and self.sex_table[column]['female']:
            self.country_row[total_column] = self.sex_table[column]['male'] + self.sex_table[column]['female']
            self.country_row[female_column] = self.sex_table[column]['female']
            self.country_row[male_column] = self.sex_table[column]['male']
        elif self.sex_table[column]['total'] and self.sex_table[column]['female']:
            self.country_row[total_column] = self.sex_table[column]['total']
            self.country_row[female_column] = self.sex_table[column]['female']
            self.country_row[male_column] = self.sex_table[column]['total'] - self.sex_table[column]['female']
        elif self.sex_table[column]['total'] and self.sex_table[column]['male']:
            self.country_row[total_column] = self.sex_table[column]['total']
            self.country_row[female_column] = self.sex_table[column]['total'] - self.sex_table[column]['male']
            self.country_row[male_column] = self.sex_table[column]['male']
        elif self.sex_table[column]['total']:
            self.country_row[total_column] = self.sex_table[column]['total']
            self.country_row[female_column] = None
            self.country_row[male_column] = None
        else:
            self.country_row[total_column] = None

    def percent_gender_calculations(self, percent_column, absolute_column):
        total_absolute_column, female_absolute_column, male_absolute_column = self._get_breakdown_columns(absolute_column)
        total_percent_column, female_percent_column, male_percent_column = self._get_breakdown_columns(percent_column)

        if self.country_row[female_absolute_column] and self.country_row[male_absolute_column]:
            self.country_row[female_percent_column] = self.country_row[female_absolute_column] / self.country_row[total_absolute_column] * 100
            self.country_row[male_percent_column] = self.country_row[male_absolute_column] / self.country_row[total_absolute_column] * 100
        elif self.sex_table[percent_column]['female'] and self.sex_table[percent_column]['male']:
            self.country_row[female_percent_column] = self.sex_table[percent_column]['female']
            self.country_row[male_percent_column] = self.sex_table[percent_column]['male']
        else:
            self.country_row[female_percent_column] = None
            self.country_row[male_percent_column] = None


    def _absolute_death_calculations(self):
        # Total no. of deaths:
        # if disaggregated by sex, this should be sum of male + female cases.
        # If not disaggregated by sex, total number of cases
        if self.sex_table['absolute_deaths']['male'] and self.sex_table['absolute_deaths']['female']:
            self.country_row['No. of deaths (men)'] = self.sex_table['absolute_deaths']['male']
            self.country_row['No. of deaths (women)'] = self.sex_table['absolute_deaths']['female']
            self.country_row['Total number of deaths'] = self.country_row['No. of deaths (men)'] + self.country_row['No. of deaths (women)']
        elif self.sex_table['absolute_deaths']['total']:
            self.country_row['Total number of deaths'] = self.sex_table['absolute_deaths']['total']
        else:
            self.country_row['Total number of deaths'] = None

    def _percent_death_calculations(self):
        # % cases (men) and (female)
        if self.country_row['No. of deaths (men)'] and self.country_row['No. of deaths (women)']:
            self.country_row["% deaths (male)"] = self.country_row['No. of deaths (men)'] / self.country_row['Total no. of cases']
            self.country_row["% deaths (female)"] = self.country_row['No. of deaths (women)'] / self.country_row['Total no. of cases']
        elif self.sex_table['percent_deaths']['male'] and self.sex_table['percent_deaths']['female']:
            self.country_row["% deaths (male)"] = self.sex_table['percent_deaths']['male']
            self.country_row["% deaths (female)"] = self.sex_table['percent_deaths']['female']
        else:
            self.country_row["% deaths (male)"] = None
            self.country_row["% deaths (female)"] = None

        if self.country_row['Total number of deaths'] and self.country_row['Total no. of cases']:
            self.country_row["Proportion of confirmed cases that have died - overall"] = self.country_row['Total number of deaths'] / self.country_row['Total no. of cases']
        else:
            self.country_row["Proportion of confirmed cases that have died - overall"] = None

        if self.country_row["No. of deaths (men)"] and self.country_row["no. of cases (men)"]:
            self.country_row["Proportion of confirmed cases that have died - men"] = self.country_row["No. of deaths (men)"] / self.country_row["no. of cases (men)"]
        if self.country_row["No. of deaths (women)"] and self.country_row["no. of cases (women)"]:
            self.country_row["Proportion of confirmed cases that have died - women"] = self.country_row["No. of deaths (women)"] / self.country_row["no. of cases (women)"]

        if self.country_row["Proportion of confirmed cases that have died - men"] and self.country_row["Proportion of confirmed cases that have died - women"]:
            self.country_row["Ratio - confirmed cases that have died (m:f)"] = self.country_row["Proportion of confirmed cases that have died - men"] / self.country_row["Proportion of confirmed cases that have died - women"]

    @staticmethod
    def _get_breakdown_columns(column):
        total_column = f"{column} - total"
        female_column = f"{column} - female"
        male_column = f"{column} - male"
        return total_column, female_column, male_column
    #
    # def _absolute_tested_calculations(self):
    #     # Total no. of cases:
    #     # if disaggregated by sex, this should be sum of male + female cases.
    #     # If not disaggregated by sex, total number of cases
    #     if self.sex_table['absolute_cases']['male'] and self.sex_table['absolute_cases']['female']:
    #         self.country_row['no. of cases (men)'] = self.sex_table['absolute_cases']['male']
    #         self.country_row['no. of cases (women)'] = self.sex_table['absolute_cases']['female']
    #         self.country_row['Total no. of cases'] = self.country_row['no. of cases (men)'] + self.country_row['no. of cases (women)']
    #     elif self.sex_table['absolute_cases']['total']:
    #         self.country_row['no. of cases (men)'] = None
    #         self.country_row['no. of cases (women)'] = None
    #         self.country_row['Total no. of cases'] = self.sex_table['absolute_cases']['total']
    #     else:
    #         self.country_row['Total no. of cases'] = None
    #
    # def _percent_tested_calculations(self):
    #     # % cases (men) and (female)
    #     if self.country_row['no. of cases (men)'] and self.country_row['no. of cases (women)']:
    #         self.country_row["% cases (men)"] = self.country_row['no. of cases (men)'] / self.country_row['Total no. of cases']
    #         self.country_row["% cases (female)"] = self.country_row['no. of cases (women)'] / self.country_row['Total no. of cases']
    #     elif self.sex_table['percent_cases']['male'] and self.sex_table['percent_cases']['female']:
    #         self.country_row["% cases (men)"] = self.sex_table['percent_cases']['male']
    #         self.country_row["% cases (female)"] = self.sex_table['percent_cases']['female']
    #     else:
    #         self.country_row["% cases (men)"] = None
    #         self.country_row["% cases (female)"] = None



    def get_info(self):
        return [['Country Information', ''],
                ["COUNTRY", self.COUNTRY],
                ["SOURCE", self.SOURCE],
                ["TYPE", self.TYPE]]
