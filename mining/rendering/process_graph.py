import math
import re


def process_graph(cli_args, graph, metadata):
  (digraph, min_weight, max_weight, min_value, max_value) = metadata

  if cli_args['weightpercent']:
    percent = min(100, max(0, cli_args['weightpercent']))
    number_of_edges = math.floor((percent / 100) * len(graph['edges']))
    all_weights = sorted([edge['weight'] for edge in graph['edges']])
    min_weight_percent = all_weights[-number_of_edges]
    if not (cli_args['minweight'] and cli_args['minweight'] > min_weight_percent):
      cli_args['minweight'] = min_weight_percent

  graph['nodes'] = [node for node in graph['nodes'] if keep_node(cli_args, graph, node)]
  graph['edges'] = [edge for edge in graph['edges'] if keep_edge(cli_args, graph, edge)]


def keep_node(cli_args, graph, node):
  if cli_args['filetype']:
    if not node_file_type(node['id']) in cli_args['filetype']:
      return False
  if cli_args['minvalue']:
    if node['value'] < cli_args['minvalue']:
      return False
  if cli_args['minweight'] and not cli_args['inspectfile']:
    try:
      next((
          edge for edge in graph['edges'] if (
              edge['start'] == node['id'] and edge['weight'] >= cli_args['minweight']) or (
              edge['end'] == node['id'] and edge['weight'] >= cli_args['minweight'])))
    except StopIteration:
      return False
  if cli_args['inspectfile']:
    if node_is_inspected(node['id'], cli_args):
      return True
    try:
      e = next((
          edge for edge in graph['edges'] if ((edge['start'] == node['id'] and node_is_inspected(edge['end'], cli_args)) or (
              edge['end'] == node['id'] and node_is_inspected(edge['start'], cli_args))) and (not cli_args['minweight'] or edge['weight'] >= cli_args['minweight'])))
    except StopIteration:
      return False

  return True


def keep_edge(cli_args, graph, edge):
  if cli_args['minweight'] and edge['weight'] < cli_args['minweight']:
    return False

  try:
    start_node = next((node for node in graph['nodes'] if edge['start'] == node['id']))
    end_node = next((node for node in graph['nodes'] if edge['end'] == node['id']))
    if cli_args['inspectfile']:
      return node_is_inspected(edge['start'], cli_args) or node_is_inspected(edge['end'], cli_args)
    return True
  except StopIteration:
    return False


def node_file_type(node_id):
  return f".{node_id.split(':')[1].split('/')[-1].split('.')[-1]}"


def node_is_inspected(node_id, cli_args):
  return True if re.search(cli_args['inspectfile'], node_file_path(node_id)) else False


def node_file_path(node_id):
  return node_id.split(':')[1]
