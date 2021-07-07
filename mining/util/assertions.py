import pydriller


def assert_modification_file_path(
        mod: pydriller.domain.commit.ModifiedFile,
        commit_hash) -> str:
  path = mod.new_path or mod.old_path
  assert path, f"A file in commit {commit_hash} has no path!"
  return path
