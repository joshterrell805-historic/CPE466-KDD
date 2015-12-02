import formatter
import numpy as np
import numpy.random
from sklearn.pipeline import Pipeline
import numpy as np
import pandas as pd
import click

from hierarchical_clusterer import Hierarchical

@click.command()
@click.argument('datafile', type=click.File('r'))
@click.argument('threshold', required=False, type=click.FLOAT)
def main(datafile, threshold):
    header = datafile.readline()
    collist = [i for i, toggle in enumerate(header.split(',')) if toggle != "0"]
    data = pd.read_csv(datafile, usecols = collist).as_matrix()

    pipeline = Pipeline([('clf', Hierarchical())])
    pipeline.set_params(**{
    })
    pipeline.fit(data)

    clf = pipeline.get_params()['clf']
    #print(hierarchy.to_xml())

    if threshold != None:
        clusters = clf.hierarchy_.cut(threshold)
        print('\n'.join(c.to_str(i) for i,c in enumerate(clusters)))
        dump_graph(clusters)

def dump_graph(clusters):
    cluster_points = [c.get_points() for c in clusters]
    assignments = [i for i,c in enumerate(cluster_points) for _ in c]
    X = [pt for c in cluster_points for pt in c]
    X = pd.DataFrame(X)
    X['assignment'] = assignments
    X.to_csv('graph.csv')
