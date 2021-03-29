from util.spinner import Spinner
from typing import List
from tqdm import tqdm
from util.CouplingCommit import CouplingCommit


def unpack_commits(repository) -> List[CouplingCommit]:
  commits = []
  total_commits = sum(1 for _ in tqdm(repository.traverse_commits(), unit=' commits', desc='Counting commits'))
  for commit in tqdm(repository.traverse_commits(), total=total_commits, unit=' commits', desc='Unpacking commits'):
    commits.append(CouplingCommit(commit))

  return commits
