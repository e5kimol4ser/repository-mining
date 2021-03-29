import click
from util.formatters import get_formatter, get_valid_formatters


def exec_stage(cli_args, graph):
  formatter = get_formatter(cli_args)
  if formatter:
    formatter.export_file(cli_args, graph)
  else:
    raise click.BadOptionUsage(
        option_name='-of',
        message=f"Specified '--outputformat' not found. Possible values are: {', '.join(get_valid_formatters())}")
