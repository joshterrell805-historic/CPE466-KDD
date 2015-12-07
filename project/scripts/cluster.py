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
    #usecols=None
    #data = pd.read_csv(datafile, usecols=usecols)
    #.as_matrix()

    #data.as_matrix()
    data = np.random.rand(30,4)
    pipeline = Pipeline([('clst', DBSCAN())])
    pipeline.set_params(**{
        'clst__eps': 0.5,
        'clst__min_samples': 5,
    })
    pipeline.fit(data)
    clst = pipeline.get_params()['clst']
    dump_graph(data, clst.labels_)

def dump_graph(X, labels_):
    X = pd.DataFrame(X)
    X['cluster'] = labels_
    X.to_csv('clusters.csv')

