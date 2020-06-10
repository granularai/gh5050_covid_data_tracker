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
    BASE_SOURCE: str
        The source being evaluated
    TYPE: str
        The source type (pdf, html, etc)
    FREQUENCY: str
        Data update frequency (daily, weekly, monthly, live)
    ARCHIVE_AVAILABLE: bool
        Is archive data accessible or is data ephemeral?
    AUTHOR: str
        Name of plugin author
    """

    PluginRegistry = {}

    sex_table = pd.DataFrame(
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

    required_cls_attr = ['COUNTRY',
                         'BASE_SOURCE',
                         'TYPE',
                         'FREQUENCY',
                         'ARCHIVE_AVAILABLE',
                         'AUTHOR']

    required_obj_attr = ['UNIQUE_SOURCE',
                         'DATE']

    @classmethod
    def __init_subclass__(cls, **kwargs):

        for required in cls.required_cls_attr:
            if not getattr(cls, required):
                raise TypeError(f"Can't instantiate class {cls.__name__}"
                                f"without {required} attribute defined")
        super().__init_subclass__(**kwargs)
        cls.PluginRegistry[cls.COUNTRY] = cls


    def check_instance_attributes(self):
        # self.UNIQUE_SOURCE: str  # the source for the specific pull
        # self.DATE: datetime.date()  # the last date for which this data is accurate
        for required in self.required_obj_attr:
            if not getattr(self, required):
                raise TypeError(f"Can't instantiate class {self.__name__}"
                                f"without {required} attribute defined")

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

        return self.country_row

    def absolute_calculations(self, column):
        (total_column,
         female_column,
         male_column) = self._get_breakdown_columns(column)

        total_cell = self.sex_table[column]['total']
        male_cell = self.sex_table[column]['male']
        female_cell = self.sex_table[column]['female']

        if pd.notna(male_cell) and pd.notna(female_cell):
            self.country_row[total_column] = male_cell + female_cell
            self.country_row[female_column] = female_cell
            self.country_row[male_column] = male_cell

        elif pd.notna(total_cell) and pd.notna(female_cell):
            self.country_row[total_column] = total_cell
            self.country_row[female_column] = female_cell
            self.country_row[male_column] = total_cell - female_cell

        elif pd.notna(total_cell) and pd.notna(male_cell):
            self.country_row[total_column] = total_cell
            self.country_row[female_column] = total_cell - male_cell
            self.country_row[male_column] = male_cell
        elif pd.notna(total_cell):
            self.country_row[total_column] = total_cell
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

        total_abs_cell = self.country_row[total_absolute_column]
        female_abs_cell = self.country_row[female_absolute_column]
        male_abs_cell = self.country_row[male_absolute_column]
        female_percent_cell = self.sex_table[percent_column]['female']
        male_percent_cell = self.sex_table[percent_column]['male']

        if pd.notna(female_abs_cell) and pd.notna(male_abs_cell):
            self.country_row[female_percent_column] = (
                                female_abs_cell /
                                total_abs_cell
                                ) * 100
            self.country_row[male_percent_column] = (
                                male_abs_cell /
                                total_abs_cell
                                ) * 100
        elif pd.notna(female_percent_cell) and pd.notna(male_percent_cell):
            self.country_row[female_percent_column] = female_percent_cell
            self.country_row[male_percent_column] = male_percent_cell
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
        proportion_female_key = f"Proportion {compare_col_one} to {compare_col_two} (female)"
        ratio_key = f"Ratio {compare_col_one} to {compare_col_two} (male:female)"

        total_cell_one = self.country_row[total_col_one]
        total_cell_two = self.country_row[total_col_two]

        female_cell_one = self.country_row[female_col_one]
        female_cell_two = self.country_row[female_col_two]

        male_cell_one = self.country_row[male_col_one]
        male_cell_two = self.country_row[male_col_two]

        if pd.notna(total_cell_one) and pd.notna(total_cell_two):
            self.country_row[proportion_total_key] = (
                                    total_cell_one / total_cell_two
                                    )
        else:
            self.country_row[proportion_total_key] = None

        if pd.notna(male_cell_one) and pd.notna(male_cell_two):
            self.country_row[proportion_male_key] = (
                                male_cell_one /
                                male_cell_two
                                )

        if pd.notna(female_cell_one) and pd.notna(female_cell_two):
            self.country_row[proportion_female_key] = (
                                female_cell_one /
                                female_cell_two
                                )

        if (proportion_male_key in self.country_row
                    and proportion_female_key in self.country_row):
            if (pd.notna(self.country_row[proportion_male_key])
                    and pd.notna(self.country_row[proportion_female_key])):
                self.country_row[ratio_key] = (
                                    self.country_row[proportion_male_key] /
                                    self.country_row[proportion_female_key]
                                    )

    def download(self):
        base_path = f"{self.COUNTRY}/{datetime.date(datetime.now())}"
        Path(base_path).mkdir(parents=True, exist_ok=True)

        if not self.COUNTRY:
            raise NotImplementedError
        else:
            self.sex_table.to_csv(f"{base_path}/data_table.csv")

    @staticmethod
    def _get_breakdown_columns(column):
        total_column = f"{column} (total)"
        female_column = f"{column} (female)"
        male_column = f"{column} (male)"
        return total_column, female_column, male_column

    def get_info(self):
        return [['Country Information', ''],
                ["COUNTRY", self.COUNTRY],
                ["BASE_SOURCE", self.BASE_SOURCE],
                ["TYPE", self.TYPE],
                ["FREQUENCY", self.FREQUENCY],
                ["ARCHIVE_AVAILABLE", self.ARCHIVE_AVAILABLE]]
