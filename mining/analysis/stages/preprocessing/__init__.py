from util.spinner import Spinner
from . import filter_merge, filter_large, split_large, combine_consecutive


def exec_stage(cli_args, commits):
  filter_merge.stage.process(cli_args, commits)
  filter_large.stage.process(cli_args, commits)
  split_large.stage.process(cli_args, commits)
  combine_consecutive.stage.process(cli_args, commits)
