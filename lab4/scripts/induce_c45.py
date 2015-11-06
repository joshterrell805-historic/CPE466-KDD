# Train a decision tree on the input data and print it to stdout.
import click, dataset
from model import Label, Node, stringify_tree

@click.command()
@click.argument('DomainXML')
@click.argument('TrainingSetCSV', type=click.File('r'))
@click.argument('RestrictionsTXT', required=False, type=click.File('r'))
def main(domainxml, trainingsetcsv, restrictionstxt):
    col_sets, data = dataset.read(trainingsetcsv.read())
    # call train function with:
    #   `col_sets` - list of sets per column, including class label
    #   `data` (list of ([train data], class))
    tree = Node("swole", ("true", Label("protein and starches")),
            ("false", Label("sugar"))) # dummy temp tree
    tree_xml = stringify_tree(tree)
    print(tree_xml)
