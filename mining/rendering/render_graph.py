import networkx as nx
import matplotlib.pyplot as plt
from util.spinner import Spinner
import re


def render_graph(cli_args, graph, metadata):
  (digraph, min_weight, max_weight, min_value, max_value) = metadata
  G = (nx.Graph, nx.DiGraph)[digraph]()
  labels = {}

  with Spinner(desc=f"Adding {len(graph['nodes'])} nodes"):
    for node in graph['nodes']:
      G.add_node(node['id'], **node)
      labels[node['id']] = f"{node['label']} ({node['value']})"

  with Spinner(desc=f"Adding {len(graph['edges'])} edges"):
    for edge in graph['edges']:
      G.add_edge(edge['start'], edge['end'], **edge)

  with Spinner(desc="Calculating layout"):
    pos = nx.spring_layout(G)

  with Spinner(desc="Drawing nodes"):
    for id, node in G.nodes(data=True):
      is_inspected = cli_args['inspectfile'] and node_is_inspected(id, cli_args) or False
      nx.draw_networkx_nodes(G, pos, node_color=("#64b5f6", "#7986cb")[is_inspected], nodelist=[id])

  with Spinner(desc="Drawing edges"):
    for start, end, edge in G.edges(data=True):
      nx.draw_networkx_edges(
          G,
          pos,
          edgelist=[(start, end)],
          edge_color="#263238",
          alpha=interpolate(
              edge['weight'],
              min_weight,
              max_weight,
              0.4),
          arrows=edge['directed'])

  with Spinner(desc="Drawing node labels"):
    nx.draw_networkx_labels(G, pos, labels=labels, font_color="#000000")

  with Spinner(desc="Drawing edge labels"):
    for start, end, edge in G.edges(data=True):
      nx.draw_networkx_edge_labels(
          G,
          pos,
          edge_labels={(start, end): round(edge['weight'], 2)},
          font_color="#4caf50",
          label_pos=0.2 if edge['directed'] else 0.5)

  plt.subplots_adjust(left=0, right=1, top=1, bottom=0)
  plt.show()


def interpolate(value, min, max, out_min=0, out_max=1):
  rel = 1
  if min != max:
    rel = (value - min) / (max - min)

  return out_min + rel * (out_max - out_min)


def node_is_inspected(node_id, cli_args):
  return True if re.search(cli_args['inspectfile'], node_file_path(node_id)) else False


def node_file_path(node_id):
  return node_id.split(':')[1]
