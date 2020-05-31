import click
import importlib
from covid_data_tracker.registry import PluginRegistry


def plugin_selector(selected_country: str):
    """plugin selector uses COUNTRY_MAP to find the appropriate plugin for a given country.

    Parameters
    ----------
    selected_country : str
        specify the country of interest.

    Returns
    -------
    type
        Description of returned object.

    """
    print(PluginRegistry)
    if selected_country in PluginRegistry.keys():
        class_name = PluginRegistry[selected_country]
        module_name = f"covid_data_tracker.plugins.countries.{class_name}"
        print(module_name)
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        instance = class_()
        return instance
    else:
        raise AttributeError
        print('no country available')


def country_downloader(country: str):
    click.echo(f"selecting plugin for {country}")
    country_plugin = plugin_selector(country)
    click.echo(f"attempting to find available data for {country}")
    country_plugin.fetch()
    click.echo(f"downloading available data for {country}")
    country_plugin.download()
