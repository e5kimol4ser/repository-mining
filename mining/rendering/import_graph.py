import click
from util.formatters import get_formatter, get_valid_formatters


def import_graph(cli_args) -> dict:
  formatter = get_formatter(cli_args)
  if formatter:
    return formatter.import_file(cli_args)
  else:
    raise click.BadOptionUsage(
        option_name='-of',
        message=f"Specified '--outputformat' not found. Possible values are: {', '.join(get_valid_formatters())}")
