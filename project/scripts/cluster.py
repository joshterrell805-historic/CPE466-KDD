import formatter
import numpy as np
import numpy.random
from sklearn.pipeline import Pipeline
from sklearn.cluster import DBSCAN
import numpy as np
import pandas as pd
import click

@click.command()
@click.argument('datafile', type=click.File('r'))
@click.argument('k', type=click.INT)
def main(datafile, k):
    header = datafile.readline()
    collist = [i for i, toggle in enumerate(header.split(',')) if toggle != "0"]
    datafile.seek(0)
    data = pd.read_csv(datafile, usecols=collist).as_matrix()

    def metric(

    pipeline = Pipeline([('dbscan', DBSCAN())])
    pipeline.set_params(**{
        'dbscan__k': k,
        'dbscan__delta_sse': 4,
    })
    pipeline.fit(data)
    clf = pipeline.get_params()['clf']
    print('\n'.join(str(c) for c in clf.clusters_))
    dump_graph(data, clf.assignments_)

def dump_graph(X, assignments_):
    X = pd.DataFrame(X)
    X['assignment'] = assignments_
    X.to_csv('graph.csv')

