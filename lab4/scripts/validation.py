# Perform cross-validation testing given a decision tree and dataset.
import click, dataset
import c45, sampling
from model import Label, Node, stringify_tree

@click.command()
@click.argument('DomainXML')
@click.argument('TrainingSetCSV', type=click.File('r'))
@click.argument('manifold_value', type=click.INT)
@click.argument('RestrictionsTXT', required=False, type=click.File('r'))
def main(domainxml, trainingsetcsv, manifold_value, restrictionstxt):
    restrictions = dataset.restrictions_from_text(restrictionstxt)

    cols, data = dataset.read(trainingsetcsv.read(), restrictions)
    expected, actual = sampling.cross_validate(data, list(cols), manifold_value)
    print(expected)
    print(actual)
