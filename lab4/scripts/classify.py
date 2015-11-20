# Evaluate the dataset on the decision tree.
import click
import dataset
import model
import sampling

@click.command()
@click.argument('to_classify_CSV', type=click.File('r'))
@click.argument('decision_tree_XML', type=click.File('r'))
@click.argument('RestrictionsTXT', required=False, type=click.File('r'))
def main(to_classify_csv, decision_tree_xml, restrictionstxt):
    # how are we supposed to determine if this has a label column or not?
    # I guess we could look at the number of unique edge labels in decision tree
    #   to determine features/
    tree = model.build_tree(decision_tree_xml.read())
    restrictions = dataset.restrictions_from_text(restrictionstxt)
    cols, data = dataset.read(to_classify_csv.read(), restrictions)

    predicted_classes = [tree.classify(x[0], cols) for x in data]
    labels = [x[1] for x in data]
    print('Records:', len(data))
    print('Correctly classified:',
          sum(1 for p,l in zip(predicted_classes, labels) if p==l))
    print('Incorrectly classified:',
          sum(1 for p,l in zip(predicted_classes, labels) if p!=l))
    print('Accuracy:', sampling.accuracy(labels, predicted_classes))
    print('Error:', sampling.error_rate(labels, predicted_classes))
    print('Confusion matrix:')
    print(sampling.confusion_matrix(labels, predicted_classes))
