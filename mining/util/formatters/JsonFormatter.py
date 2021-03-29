import json
from .Formatter import Formatter


class JsonFormatter(Formatter):

  def import_file(self, cli_args):
    with open(cli_args['input'], 'r') as file:
      data = file.read()
    return json.loads(data)

  def export_file(self, cli_args, graph):
    if cli_args['fromdate']:
      cli_args['fromdate']
    graph['cli_args'] = cli_args
    with open(cli_args['output'], 'w') as file:
      json.dump(graph, file, ensure_ascii=False, indent=4, default=str)
