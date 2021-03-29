from typing import List, Optional
from .Formatter import Formatter
from .JsonFormatter import JsonFormatter

formatters = {
    'json': JsonFormatter
}


def get_valid_formatters() -> List[str]:
  return list(formatters.keys())


def get_formatter(cli_args) -> Optional[Formatter]:
  output_format = get_file_format(cli_args)
  if output_format in formatters:
    return formatters[output_format]()


def get_file_format(cli_args):
  if cli_args['fileformat'] == 'inferred':
    if 'output' in cli_args:
      return cli_args['output'].split('.')[-1]
    if 'input' in cli_args:
      return cli_args['input'].split('.')[-1]
  else:
    return cli_args['fileformat']
