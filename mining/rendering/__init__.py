from rendering.process_graph import process_graph
from .import_graph import import_graph
from .render_graph import render_graph
from .graph_metadata import graph_metadata


def do_rendering(**cli_args):
  graph = import_graph(cli_args)
  metadata = graph_metadata(graph)
  process_graph(cli_args, graph, metadata)
  render_graph(cli_args, graph, metadata)
