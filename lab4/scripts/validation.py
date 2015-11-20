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

    cols, data = dataset.read(trainingsetcsv.read(), True, restrictions)
    expected, actual, expected_hunked, actual_hunked = sampling.cross_validate(data, list(cols), manifold_value)
    print("Overall confusion matrix:")
    print(sampling.confusion_matrix(expected, actual))

    print("\nOverall recall:")
    print(sampling.recall(expected, actual, 'Obama'))

    print("\nOverall precision:")
    print(sampling.precision(expected, actual, 'Obama'))

    print("\nOverall pf:")
    print(sampling.pf(expected, actual, 'Obama'))

    print("\nOverall f-measure:")
    print(sampling.f_measure(expected, actual, 'Obama'))

    print("\nOverall accuracy:")
    print(sampling.accuracy(expected, actual))

    print("\nAverage accuracy:")
    print(sum(sampling.accuracy(e, a) for e, a in zip(expected_hunked, actual_hunked))/len(expected_hunked))

    print("\nOverall error rate:")
    print(sampling.error_rate(expected, actual))

    print("\nAverage error rate:")
    print(sum(sampling.error_rate(e, a) for e, a in zip(expected_hunked, actual_hunked))/len(expected_hunked))
