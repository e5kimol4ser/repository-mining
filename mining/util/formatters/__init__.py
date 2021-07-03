import logging
import os

from typing import List, Optional
from .Formatter import Formatter
from .JsonFormatter import JsonFormatter

formatters = {
    'json': JsonFormatter
}


def get_valid_formatters() -> List[str]:
  return list(formatters.keys())


_default_formatter: str = get_valid_formatters()[0]


def get_formatter(cli_args) -> Optional[Formatter]:
  output_format = get_file_format(cli_args)
  if output_format in formatters:
    return formatters[output_format]()


def get_file_format(cli_args) -> str:
  path = cli_args.get('output', cli_args.get('input'))
  if path and cli_args['fileformat'] == 'inferred':
      _, ext = os.path.splitext(path)
      if ext:
        return ext[1:] # remove leading dot
      logging.warn('could not detect file format from path, defaulting to %s', _default_formatter)
      return _default_formatter
  else:
    return cli_args['fileformat']
