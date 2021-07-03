from typing import List
import pydriller
from .Modification import Modification
from util.ModificationsBucket import ModificationsBucket


def _parse_diff_simple(diff_index) -> List[Modification]:
  modifications_list = []
  for diff in diff_index:
    old_path = diff.a_path
    new_path = diff.b_path

    modifications_list.append(Modification(old_path, new_path))

  return modifications_list


class CouplingCommit:

  def __init__(self, git_commit: pydriller.domain.commit.Commit):
    git_commit._parse_diff = _parse_diff_simple
    self.hash = git_commit.hash
    self.committer = git_commit.committer
    self.committer_date = git_commit.committer_date
    self.merge = git_commit.merge
    self.all_modifications = git_commit.modified_files
    self.ignored = False
    self.modifications_buckets: List[ModificationsBucket] = [ModificationsBucket(self.all_modifications)]
