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
from covid_data_tracker.util import (plugin_selector,
                                     country_downloader,
                                     all_country_dataframe,
                                     to_gsheets)
import tabulate

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
@click.option("--country", "-c", help="Select a country.", prompt="Select a country, (or pass nothing to download all)", default="")
@pass_info
def download(_: Info, country: str):
    """Download country level statistics."""
    if not country:
        df = all_country_dataframe()
        df.to_csv('country_data.csv')
    else:
        country_downloader(country)


@cli.command()
@click.option("--country", "-c", help="Select a specific country.", default="")
@click.option("--all", "-A", help="Select all countries (will override country option).", default=True)
@click.option("--sa_key_path", "-sa", help="Provide path to service account for google.", required=True)
@pass_info
def to_sheet(_: Info, country: str, all: str, sa_key_path: str):
    """Push country level statistics to google spreadsheet."""
    if all or not country:
        df = all_country_dataframe()
        to_gsheets(df, sa_key_path)
    else:
        raise NotImplementedError(
            "Single country push to google sheets not yet available")


@cli.command()
def version():
    """Get the library version."""
    click.echo(click.style(f"{__version__}", bold=True))
