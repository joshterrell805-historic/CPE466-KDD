# Evaluate the dataset on the decision tree.
import click
import dataset
import model

@click.command()
@click.argument('to_classify_CSV', type=click.File('r'))
@click.argument('decision_tree_XML')
@click.argument('RestrictionsTXT', required=False, type=click.File('r'))
def main(to_classify_CSV, decision_tree_XML, restrictionstxt):
    restrictions = dataset.restrictions_from_text(restrictionstxt)
    cols, data = dataset.read(to_classify_CSV.read(), restrictions)
