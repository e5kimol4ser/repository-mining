from . import stages


def do_analysis(**cli_args):
  (commits, artifacts_store) = stages.initialization.exec_stage(cli_args)
  stages.preprocessing.exec_stage(cli_args, commits)
  graph = stages.evaluation.exec_stage(cli_args, commits, artifacts_store)
  stages.export.exec_stage(cli_args, graph)
