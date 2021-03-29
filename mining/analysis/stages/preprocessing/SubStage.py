from tqdm import tqdm


class SubStage:

  def __init__(self, should_process, process_commit, context_sensitive, desc):
    self.should_process = should_process
    self.process_commit = process_commit
    self.context_sensitive = context_sensitive
    self.desc = desc

  def process(self, cli_args, commits):
    if not self.should_process(cli_args):
      return

    for commit in tqdm(commits, unit=' commits', desc=self.desc):
      if self.context_sensitive:
        self.process_commit(cli_args, commit, commits)
      else:
        self.process_commit(cli_args, commit)
