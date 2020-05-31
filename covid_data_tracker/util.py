import click
import importlib

COUNTRY_MAP = {
    'Germany': 'GermanyPlugin'
}


def plugin_selector(selected_country: str):
    if selected_country in COUNTRY_MAP.keys():
        class_name = COUNTRY_MAP[selected_country]
        module_name = f"covid_data_tracker.plugins.countries.{class_name}"
        print(module_name)
        module = importlib.import_module(module_name)
        class_ = getattr(module, class_name)
        instance = class_()
        return instance
    else:
        print('no country available')


def country_downloader(country: str):
    click.echo(f"selecting plugin for {country}")
    selector = plugin_selector(country)
    click.echo(f"attempting to find available data for {country}")
    selector.fetch()
    click.echo(f"downloading available data for {country}")
    selector.download()
