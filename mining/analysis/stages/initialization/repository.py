from pydriller import Repository


def init_repository_mining(cli_args):
  return Repository(cli_args['repository'],
                    only_in_branch=cli_args['branch'],
                    only_modifications_with_file_types=cli_args['filetype'],
                    only_authors=cli_args['author'],
                    only_commits=cli_args['commit'],
                    since=cli_args['fromdate'],
                    from_commit=cli_args['fromcommit'],
                    from_tag=cli_args['fromtag'],
                    to=cli_args['todate'],
                    to_commit=cli_args['tocommit'],
                    to_tag=cli_args['totag'],
                    skip_whitespaces=cli_args['nowhitespace'])
