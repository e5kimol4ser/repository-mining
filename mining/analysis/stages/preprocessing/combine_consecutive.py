from typing import List
from util.CouplingCommit import CouplingCommit
from util.parse_cli_args import parse_time_unit
from .SubStage import SubStage
from datetime import timedelta


def should_process(cli_args):
  return cli_args['combineconsecutive'] or False


def process_commit(cli_args, commit: CouplingCommit, commits: List[CouplingCommit]):
  if is_unsplitted_commit(commit) and not is_ignored_commit(commit):
    commit_index = commits.index(commit)
    parent_commit_index = commit_index
    combined_modifications_count = len(commit.modifications_buckets[0].modifications)
    while parent_commit_index >= 1 and commits_are_coupled(
            cli_args, commit, commits[parent_commit_index - 1], combined_modifications_count):
      parent_commit_index -= 1
      combined_modifications_count += len(commits[parent_commit_index].modifications_buckets[0].modifications)

    if commit_index != parent_commit_index:
      parent_commit = commits[parent_commit_index]
      if not is_ignored_commit(parent_commit):
        commit.ignored = True
        parent_commit.modifications_buckets[0].associate_bucket(
            commit.hash, 0)


def is_unsplitted_commit(commit: CouplingCommit) -> bool:
  return len(commit.modifications_buckets) == 1


def is_ignored_commit(commit: CouplingCommit) -> bool:
  return commit.ignored


def commits_are_coupled(cli_args, commit: CouplingCommit, parent: CouplingCommit, combined_modifications_count: int):
  if is_unsplitted_commit(parent):
    if commit.committer.email == parent.committer.email:
      (value, unit) = parse_time_unit(cli_args['combineconsecutive'])
      time_difference = commit.committer_date - parent.committer_date
      days = (0, value)[unit == 'd']
      hours = (0, value)[unit == 'h']
      minutes = (0, value)[unit == 'm']
      seconds = (0, value)[unit == 's']
      if time_difference / timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds) <= 1:
        if is_ignored_commit(parent):  # commit already ignored, continue searching.
          return True
        if not (cli_args['nolarge'] and combined_modifications_count +
                len(parent.modifications_buckets[0].modifications) >= cli_args['largethreshold']):
          return True

  return False


stage = SubStage(
    should_process,
    process_commit,
    context_sensitive=True,
    desc='Combining consecutive commits')
