from typing import List, Optional
from tqdm import tqdm
from util.assertions import assert_modification_file_path
from util.CouplingCommit import CouplingCommit


class AttributedPath:
  def __init__(self, path, deleted):
    self.path = path
    self.deleted = deleted


class Artifact:
  def __init__(self, commit_hash: str, path: str) -> None:
    self.id = Artifact.artifact_id(commit_hash, path)
    self.path_history = {}
    self.add_history(commit_hash, path)

  @staticmethod
  def artifact_id(commit_hash: str, path: str) -> str:
    return f"{commit_hash}:{path}"

  def add_history(self, commit_hash: str, path: str, deleted: bool = False) -> None:
    self.path_history[commit_hash] = AttributedPath(path, deleted)
    self.final_commit = commit_hash

  def has_history(self, commit_hash: str, path: str, deleted: Optional[bool] = None) -> bool:
    attributed_path = self.attributed_path_for_commit(commit_hash)
    if attributed_path:
      if deleted is None:
        return attributed_path.path == path
      else:
        return attributed_path.path == path and attributed_path.deleted == deleted

  def exists_at_commit(self, commit_hash: str) -> bool:
    return commit_hash in self.path_history

  def attributed_path_for_commit(self, commit_hash: str) -> Optional[AttributedPath]:
    if self.exists_at_commit(commit_hash):
      return self.path_history[commit_hash]

  def __str__(self) -> str:
    history = '\n  ' + '\n  '.join(map(lambda a: f"{a[0]}:{a[1].path}:{a[1].deleted}", self.path_history.items()))
    return f"Artifact {self.id}, with history: {history}"


class ArtifactStore:

  def __init__(self, cli_args: dict, commits: List[CouplingCommit]) -> None:
    self.artifacts: List[Artifact] = []

    previous_commit = None
    for commit in tqdm(commits, unit=' commits', desc='Collecting artifacts'):
      for mod in commit.all_modifications:
        assert_modification_file_path(mod, commit.hash)
        if mod.new_path:
          if previous_commit and mod.new_path != mod.old_path:
            self.__register_artifact_rename(previous_commit.hash, mod.old_path, commit.hash, mod.new_path)
          if not self.get_artifact(commit.hash, mod.new_path, deleted=False) and not (
                  previous_commit and self.get_artifact(previous_commit.hash, mod.new_path, deleted=False)):
            if cli_args['handledeletedfiles'] == 'reuse' and previous_commit and self.get_artifact(
                    previous_commit.hash, mod.new_path, deleted=True):
              self.__register_artifact_revert_delete(previous_commit.hash, commit.hash, mod.new_path)
            else:
              self.__register_new_artifact(commit.hash, mod.new_path)
        else:
          if cli_args['handledeletedfiles'] != 'keep':
            self.__register_artifact_delete(previous_commit.hash, commit.hash, mod.old_path)
      if previous_commit:
        self.__register_all_unchanged_artifacts(previous_commit.hash, commit.hash)

      previous_commit = commit

    if cli_args['handledeletedfiles'] != 'keep':
      self.artifacts = list(filter(lambda a: not a.attributed_path_for_commit(a.final_commit).deleted, self.artifacts))

  def get_artifact(self, commit_hash: str, path: str, deleted: bool = False) -> Optional[Artifact]:
    for artifact in self.artifacts:
      if artifact.has_history(commit_hash, path, deleted):
        return artifact

  def get_artifact_file_name(self, artifact_id) -> Optional[str]:
    for artifact in self.artifacts:
      if artifact.id == artifact_id:
        final_path = artifact.attributed_path_for_commit(artifact.final_commit)
        if final_path:
          return file_name_from_artifact_path(final_path.path)

  def __register_new_artifact(self, commit_hash: str, path: str) -> Artifact:
    new_artifact = Artifact(commit_hash, path)
    self.artifacts.append(new_artifact)
    return new_artifact

  def __register_artifact_rename(self, old_commit_hash: str, old_path: str,
                                 new_commit_hash: str, new_path: str) -> None:
    artifact = self.get_artifact(old_commit_hash, old_path, deleted=False)
    if artifact:
      artifact.add_history(new_commit_hash, new_path)

  def __register_artifact_delete(self, old_commit_hash: str, new_commit_hash: str, path: str) -> None:
    artifact = self.get_artifact(old_commit_hash, path, deleted=False)
    if artifact:
      artifact.add_history(new_commit_hash, path, deleted=True)

  def __register_artifact_revert_delete(self, old_commit_hash: str, new_commit_hash: str, path: str) -> None:
    artifact = self.get_artifact(old_commit_hash, path, deleted=True)
    if artifact:
      artifact.add_history(new_commit_hash, path, deleted=False)

  def __register_all_unchanged_artifacts(
          self, previous_commit_hash: str, current_commit_hash: str) -> None:
    for artifact in self.artifacts:
      if artifact.exists_at_commit(previous_commit_hash) and not artifact.exists_at_commit(current_commit_hash):
        path_to_copy = artifact.attributed_path_for_commit(previous_commit_hash)
        artifact.add_history(current_commit_hash, path_to_copy.path, path_to_copy.deleted)

  def __str__(self) -> str:
    artifacts = '\n  ' + '\n  '.join(map(lambda a: a.__str__(), self.artifacts))
    return f"ArtifactStore with {len(self.artifacts)} artifacts: {artifacts}"


def file_name_from_artifact_path(path: str) -> str:
  return path.split('/')[-1]
