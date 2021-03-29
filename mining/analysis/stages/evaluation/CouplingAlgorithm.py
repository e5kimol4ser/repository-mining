from tqdm import tqdm
from abc import ABC, abstractmethod


class CouplingAlgorithm(ABC):

  def compute_graph(self, cli_args, commits, artifacts_store) -> dict:
    graph_data = {}

    for commit in tqdm(commits, unit=' commits', desc="Running coupling algorithm"):
      self.process_commit(cli_args, commit, commits, artifacts_store, graph_data)

    graph = self.construct_graph(cli_args, graph_data, artifacts_store)

    return graph

  @abstractmethod
  def process_commit(self, cli_args, commit, commits, artifacts_store, graph_data) -> None:
    pass

  @abstractmethod
  def construct_graph(self, cli_args, graph_data) -> dict:
    pass
