import click
from jsonreader import JsonReader

@click.command()
@click.argument('input', type=click.File('r'))
def cli(input):
    """Example basic script"""
    click.echo('Hello World!')
    click.secho(input.read()[0:100], fg='green')
    click.
