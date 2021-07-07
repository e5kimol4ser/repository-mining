from typing import List
from util.CouplingCommit import CouplingCommit
from .SubStage import SubStage
import pydriller
from util.ModificationsBucket import ModificationsBucket


def should_process(cli_args):
  return cli_args['splitlarge'] or False


def process_commit(cli_args, commit: CouplingCommit):
  # print(commit.hash)
  # print("before: -----------------------------")
  # [print(f"\n{x}\n") for x in commit.modifications_buckets]
  commit.modifications_buckets = [
      ModificationsBucket(mods) for mods in split_path_hierarchy(
          commit.all_modifications, cli_args['largethreshold'], cli_args['nolarge'])]
  # print("after: ------------------------------")
  # [print(f"\n{x}\n") for x in commit.modifications_buckets]


def split_path_hierarchy(modifications: List[pydriller.domain.commit.ModifiedFile], threshold, filterLarge, depth=0):
  if len(modifications) < threshold:
    return [modifications]

  buckets = {}
  modifications_buckets = []
  top_level_modifications = []
  return_buckets = []
  for modification in modifications:
    name = folder_name(modification.new_path or modification.old_path, depth)
    if name:
      if not name in buckets:
        modifications_buckets.append([])
        buckets[name] = len(modifications_buckets) - 1
      modifications_buckets[buckets[name]].append(modification)
    else:
      top_level_modifications.append(modification)

  for modifications_bucket in modifications_buckets:
    return_buckets.extend(split_path_hierarchy(modifications_bucket, threshold, filterLarge, depth + 1))

  if not (filterLarge and len(top_level_modifications) >= threshold):
    return_buckets.append(top_level_modifications)

  return return_buckets


def folder_name(path: str, depth):
  hierarchy = path.split('/')
  if depth < len(hierarchy) - 1:
    return hierarchy[depth]


stage = SubStage(
    should_process,
    process_commit,
    context_sensitive=False,
    desc='Splitting large commits')
