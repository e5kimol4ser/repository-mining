from abc import ABC, abstractmethod


class Formatter(ABC):

  @abstractmethod
  def import_file(self, cli_args) -> dict:
    pass

  @abstractmethod
  def export_file(self, cli_args, graph) -> None:
    pass
