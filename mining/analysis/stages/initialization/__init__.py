from util.spinner import Spinner
from .repository import init_repository_mining
from .artifacts import init_artifacts_store
from .commits import unpack_commits


def exec_stage(cli_args):
  repository = init_repository_mining(cli_args)
  commits = unpack_commits(repository)
  artifacts_store = init_artifacts_store(cli_args, commits)
  return (commits, artifacts_store)
