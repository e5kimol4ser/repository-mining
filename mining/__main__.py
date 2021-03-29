import click
from analysis import do_analysis
from rendering import do_rendering
from util.parse_cli_args import parse_time_unit


@click.group()
def cli():
  pass


@cli.command()
@click.option('-r', '--repository', prompt="Repository location", help="Provide a local directory or a remote url")
@click.option('-b', '--branch')
@click.option('-f', '--filetype', multiple=True)
@click.option('-a', '--author', multiple=True)
@click.option('-c', '--commit', multiple=True)
@click.option('-fd', '--fromdate', type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option('-fc', '--fromcommit')
@click.option('-ft', '--fromtag')
@click.option('-td', '--todate', type=click.DateTime(formats=["%Y-%m-%d"]))
@click.option('-tc', '--tocommit')
@click.option('-tt', '--totag')
#
@click.option('-lt', '--largethreshold', type=int, default=50)
@click.option('-nl', '--nolarge', type=bool, is_flag=True)
@click.option('-sl', '--splitlarge', type=bool, is_flag=True)
@click.option('-nm', '--nomerge', type=bool, is_flag=True)
@click.option('-nw', '--nowhitespace', type=bool, is_flag=True)
@click.option('-cc', '--combineconsecutive')
#
@click.option('-al', '--algorithm', prompt="Coupling algorithm")
@click.option('-df', '--handledeletedfiles',
              type=click.Choice(['keep', 'discard', 'reuse'], case_sensitive=True), default='discard')
@click.option('-o', '--output', type=click.Path(dir_okay=False, writable=True), prompt="Output file path")
@click.option('-ff', '--fileformat', default='inferred')
def analysis(**args):
  if (args['fromdate'] is not None and args['fromcommit'] is not None):
    raise click.BadOptionUsage(option_name='-fc', message="Cannot use multiple 'from' options.")
  if (args['fromcommit'] is not None and args['fromtag'] is not None):
    raise click.BadOptionUsage(option_name='-ft', message="Cannot use multiple 'from' options.")
  if (args['fromtag'] is not None and args['fromdate'] is not None):
    raise click.BadOptionUsage(option_name='-fd', message="Cannot use multiple 'from' options.")

  if (args['todate'] is not None and args['tocommit'] is not None):
    raise click.BadOptionUsage(option_name='-tc', message="Cannot use multiple 'to' options.")
  if (args['tocommit'] is not None and args['totag'] is not None):
    raise click.BadOptionUsage(option_name='-tt', message="Cannot use multiple 'to' options.")
  if (args['totag'] is not None and args['todate'] is not None):
    raise click.BadOptionUsage(option_name='-td', message="Cannot use multiple 'to' options.")

  if not args['algorithm']:
    raise click.BadOptionUsage(option_name='-al', message="Please specify a coupling '--algorithm'.")
  if not args['output']:
    raise click.BadOptionUsage(option_name='-o', message="Please specify an '--output' file path.")

  if args['combineconsecutive'] and not parse_time_unit(args['combineconsecutive']):
    raise click.BadOptionUsage(option_name='-cc',
                               message="Please specify a correct time unit for '--combineconsecutive'. Valid examples are: 120s, 10m, 3h, 1d")

  args['filetype'] = list(args['filetype']) or None
  args['author'] = list(args['author']) or None
  args['commit'] = list(args['commit']) or None

  do_analysis(**args)


@cli.command()
@click.option('-f', '--filetype', multiple=True)
@click.option('-if', '--inspectfile')
@click.option('-w', '--minweight', type=float)
@click.option('-v', '--minvalue', type=float)
@click.option('-wp', '--weightpercent', type=float)
#
@click.option('-i', '--input', type=click.Path(dir_okay=False, readable=True))
@click.option('-ff', '--fileformat', default='inferred')
def render(**args):
  args['filetype'] = list(args['filetype']) or None

  do_rendering(**args)


if __name__ == '__main__':
  cli()
