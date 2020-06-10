import click
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
