from datetime import date
import pandas as pd
import click
import gspread
from gspread_dataframe import set_with_dataframe
from covid_data_tracker.registry import PluginRegistry


def plugin_selector(selected_country: str):
    """plugin selector uses COUNTRY_MAP to find the appropriate plugin
       for a given country.

    Parameters
    ----------
    selected_country : str
        specify the country of interest.

    Returns
    -------
    covid_data_tracker.plugins.BasePlugin
        More appropriately, returns an instance of a country-specific
        subclass of BasePlugin.

    """
    if selected_country in PluginRegistry.keys():
        klass = PluginRegistry[selected_country]
        instance = klass()
    else:
        raise AttributeError
        click.echo('No country plugin available')

    return instance


def country_downloader(country: str):
    """Finds country plugin, fetches data, and downloads
       to csv with click alerts.

    Parameters
    ----------
    country : str
        Name of country

    Returns
    -------
    NoneType

    """
    click.echo(f"selecting plugin for {country}")
    country_plugin = plugin_selector(country)
    click.echo(f"attempting to find available data for {country}")
    country_plugin.fetch()
    click.echo(f"downloading available data for {country}")
    country_plugin.check_instance_attributes()
    country_plugin.download()


def all_country_dataframe():
    click.echo(f"attempting to find available data for every country")
    with click.progressbar(list(PluginRegistry)) as countries:
        country_rows = {}
        for country in countries:
            try:
                country_plugin = plugin_selector(country)
                country_plugin.fetch()
                country_plugin.check_instance_attributes()
                country_plugin.create_country_row()
                meta = {"Author": country_plugin.AUTHOR,
                        "Source": country_plugin.UNIQUE_SOURCE,
                        "Date": country_plugin.DATE}
                country_rows[country] = dict(country_plugin.country_row,
                                             **meta)
            except Exception as e:
                print(f"unable to download for {country}")
                print(e)
        df = pd.DataFrame.from_dict(country_rows, orient="index")
        return df


def to_gsheets(df: pd.DataFrame,
               sa_filepath: str,
               spreadsheet_name: str = 'GH5050_Weekly_Country_Data',
               worksheet_name: str = str(date.today()),
               share_with: str = 'sid@granular.ai'):

    gc = gspread.service_account(sa_filepath)
    spreadsheets = gc.list_spreadsheet_files()

    if any([sh['name'] == spreadsheet_name for sh in spreadsheets]):
        spreadsheet = gc.open(spreadsheet_name)
    else:
        spreadsheet = gc.create(spreadsheet_name)
        spreadsheet.share(share_with, 'user', 'writer')

    num_rows = df.shape[0] + 1  # adding one row for header
    num_cols = df.shape[1]

    try:
        worksheet = spreadsheet.worksheet(worksheet_name)
    except Exception:
        worksheet = spreadsheet.add_worksheet(worksheet_name,
                                              num_rows,
                                              num_cols)
    set_with_dataframe(worksheet, df, include_index=True, resize=True)
