from __future__ import annotations
from typing import List, Tuple
from .Modification import Modification


class ModificationsBucket:

  def __init__(self, modifications: List[Modification]):
    self.modifications = modifications
    self.associated_buckets: List[Tuple[str, int]] = []

  def associate_bucket(self, commit_hash, bucket_index):
    self.associated_buckets.append((commit_hash, bucket_index))

  def get_all_modifications(self, commits, commit) -> List[Tuple[Modification, str]]:
    modifications = [(mod, commit.hash) for mod in self.modifications]
    for (commit_hash, bucket_index) in self.associated_buckets:
      other_commit = next(filter(lambda c: c.hash == commit_hash, commits))
      if other_commit and bucket_index < len(other_commit.modifications_buckets):
        modifications.extend([(mod, commit_hash)
                              for mod in other_commit.modifications_buckets[bucket_index].modifications])
    return modifications

  def __str__(self) -> str:
    out = ''
    for modification in self.modifications:
      out += f"\n{modification._new_path or modification._old_path}"

    return out
