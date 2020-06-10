#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is the entry point for the command-line interface (CLI) application.

It can be used as a handy facility for running the task from a command line.

.. note::

    To learn more about Click visit the
    `project website <http://click.pocoo.org/5/>`_.  There is also a very
    helpful `tutorial video <https://www.youtube.com/watch?v=kNke39OZ2k0>`_.

    To learn more about running Luigi, visit the Luigi project's
    `Read-The-Docs <http://luigi.readthedocs.io/en/stable/>`_ page.

.. currentmodule:: covid_data_tracker.cli
.. moduleauthor:: Sid Gupta <team@granular.ai>
"""
import logging
import click
from .__init__ import __version__

from covid_data_tracker.registry import PluginRegistry
from covid_data_tracker.util import plugin_selector, country_downloader
import tabulate
import pandas as pd

LOGGING_LEVELS = {
    0: logging.NOTSET,
    1: logging.ERROR,
    2: logging.WARN,
    3: logging.INFO,
    4: logging.DEBUG,
}  #: a mapping of `verbose` option counts to logging levels


class Info(object):
    """An information object to pass data between CLI functions."""

    def __init__(self):  # Note: This object must have an empty constructor.
        """Create a new instance."""
        self.verbose: int = 0


# pass_info is a decorator for functions that pass 'Info' objects.
#: pylint: disable=invalid-name
pass_info = click.make_pass_decorator(Info, ensure=True)


# Change the options to below to suit the actual options for your task (or
# tasks).
@click.group()
@click.option("--verbose", "-v", count=True, help="Enable verbose output.")
@pass_info
def cli(info: Info, verbose: int):
    """Run covidtracker."""
    # Use the verbosity count to determine the logging level...
    if verbose > 0:
        logging.basicConfig(
            level=LOGGING_LEVELS[verbose]
            if verbose in LOGGING_LEVELS
            else logging.DEBUG
        )
        click.echo(
            click.style(
                f"Verbose logging is enabled. "
                f"(LEVEL={logging.getLogger().getEffectiveLevel()})",
                fg="yellow",
            )
        )
    info.verbose = verbose


@cli.command('list')
@pass_info
def list_countries(_: Info):
    """List all countries for which a plugin is available."""
    [click.echo(i) for i in list(PluginRegistry)]


@cli.command()
@click.option("--country", "-c", prompt="Select a country.")
@pass_info
def info(_: Info, country: str):
    """Get country level information on sources and download strategy."""
    country_plugin = plugin_selector(country)
    info = country_plugin.get_info()
    click.echo(tabulate.tabulate(info[1:], info[0]))



@cli.command()
# @click.option("--all", "-A",
#               help="Select all countries. (overrides --country)",
#               callback=download_all,
#               is_flag=True,
#               is_eager=True)
@click.option("--country", "-c", help="Select a country.", prompt="Select a country, (or pass nothing to download all)", default="")
@pass_info
def download(_: Info, country: str):
    """Download country level statistics."""
    if not country:
        click.echo(f"attempting to find available data for every country")
        with click.progressbar(list(PluginRegistry)) as countries:
            # df = pd.DataFrame()
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
                    # if not len(df.columns):
                    #     df.columns = country_plugin.country_row.index
                    country_rows[country] = dict(country_plugin.country_row,
                                                 **meta)
                except Exception as e:
                    print(f"unable to download for {country}")
                    print(e)
            df = pd.DataFrame.from_dict(country_rows, orient="index")
            df.to_csv('country_data.csv')

    else:
        country_downloader(country)


@cli.command()
def version():
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))
