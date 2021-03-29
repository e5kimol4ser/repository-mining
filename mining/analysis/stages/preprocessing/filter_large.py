from util.CouplingCommit import CouplingCommit
from .SubStage import SubStage


def should_process(cli_args):
  return (cli_args['nolarge'] and not cli_args['splitlarge']) or False


def process_commit(cli_args, commit: CouplingCommit):
  if len(commit.all_modifications) >= cli_args['largethreshold']:
    commit.ignored = True


stage = SubStage(
    should_process,
    process_commit,
    context_sensitive=False,
    desc='Filtering large commits')
