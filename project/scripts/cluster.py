import formatter
import numpy as np
import numpy.random
from sklearn.pipeline import Pipeline
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import RobustScaler
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
    pipeline = Pipeline([('scaler', RobustScaler()), ('clusterer', DBSCAN())])
    pipeline.set_params(**{
        'clusterer__eps': 0.5,
        'clusterer__min_samples': 5,
    })
    pipeline.fit(data)
    clusterer = pipeline.get_params()['clusterer']
    dump_graph(data, clusterer.labels_)

def dump_graph(X, labels_):
    X = pd.DataFrame(X)
    X['cluster'] = labels_
    X.to_csv('clusters.csv')

