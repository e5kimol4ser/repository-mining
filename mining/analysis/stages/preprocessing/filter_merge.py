from util.CouplingCommit import CouplingCommit
from .SubStage import SubStage


def should_process(cli_args):
  return cli_args['nomerge'] or False


def process_commit(cli_args, commit: CouplingCommit):
  if commit.merge:
    commit.ignored = True


stage = SubStage(
    should_process,
    process_commit,
    context_sensitive=False,
    desc='Filtering merge commits')
