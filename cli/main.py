"""Main CLI entry point for Joe-Agent-Platform."""

import sys
from typing import Optional

import click

from cli.commands.ask import ask as ask_cmd
from cli.commands.chat import chat as chat_cmd
from cli.commands.code import code as code_cmd
from cli.commands.crawl import crawl as crawl_cmd
from cli.commands.scrape import scrape as scrape_cmd
from cli.commands.search import search as search_cmd
from cli.commands.summarize import summarize as summarize_cmd
from cli.commands.analyze import analyze as analyze_cmd
from cli.commands.config import config as config_cmd
from cli.commands.models import models as models_cmd
from cli.commands.health import health as health_cmd
from cli.commands.version import version as version_cmd
from cli.utils import setup_logging, load_config


@click.group()
@click.option('--verbose', '-v', is_flag=True, help='Enable verbose output')
@click.option('--config', '-c', type=click.Path(), help='Config file path')
@click.pass_context
def main(ctx: click.Context, verbose: bool, config: Optional[str]) -> None:
    """Joe-Agent-Platform CLI - AI Agent Command Line Interface"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose
    ctx.obj['config_path'] = config
    setup_logging(verbose)
    load_config(config)


main.add_command(ask_cmd)
main.add_command(chat_cmd)
main.add_command(code_cmd)
main.add_command(crawl_cmd)
main.add_command(scrape_cmd)
main.add_command(search_cmd)
main.add_command(summarize_cmd)
main.add_command(analyze_cmd)
main.add_command(config_cmd)
main.add_command(models_cmd)
main.add_command(health_cmd)
main.add_command(version_cmd)


if __name__ == '__main__':
    main()