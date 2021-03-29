import click
from .RawCountingAlgorithms import UndirectedRawCountingAlgorithm, DirectedRawCountingAlgorithm

algorithms = {
    'urc': UndirectedRawCountingAlgorithm,
    'drc': DirectedRawCountingAlgorithm
}


def exec_stage(cli_args, commits, artifacts_store):
  if cli_args['algorithm'] in algorithms:
    algorithm = algorithms[cli_args['algorithm']]()
    return algorithm.compute_graph(cli_args, commits, artifacts_store)
  else:
    raise click.BadOptionUsage(
        option_name='-al',
        message=f"Specified '--algorithm' not found. Possible values are: {', '.join(list(algorithms.keys()))}")
