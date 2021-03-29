import math


def graph_metadata(graph):
  digraph = False
  min_weight = math.inf
  max_weight = 0
  min_value = math.inf
  max_value = 0

  for node in graph['nodes']:
    if node['value'] < min_value:
      min_value = node['value']
    if node['value'] > max_value:
      max_value = node['value']

  for edge in graph['edges']:
    if edge['directed']:
      digraph = True
    if edge['weight'] < min_weight:
      min_weight = edge['weight']
    if edge['weight'] > max_weight:
      max_weight = edge['weight']

  return (digraph, min_weight, max_weight, min_value, max_value)
