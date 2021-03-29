from typing import List
import pydriller
from util.ArtifactStore import ArtifactStore


def init_artifacts_store(cli_args: dict, commits: List[pydriller.domain.commit.Commit]) -> ArtifactStore:
  return ArtifactStore(cli_args, commits)
