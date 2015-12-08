import formatter
import numpy as np
import numpy.random
from sklearn.pipeline import Pipeline
from sklearn.cluster import DBSCAN, KMeans
from sklearn.preprocessing import RobustScaler
import numpy as np
import pandas as pd
import click

@click.command()
@click.argument('datafile', type=click.File('r'))
@click.argument('k', type=click.INT, default=2)
def main(datafile, k):
    data = pd.read_csv(datafile, sep=' ')

    matrix = data.as_matrix()
    #pipeline = Pipeline([('scaler', RobustScaler()), ('clusterer', DBSCAN())])
    pipeline = Pipeline([('scaler', RobustScaler()), ('clusterer', KMeans())])
    #pipeline.set_params(**{
    #    'clusterer__eps': eps,
    #    'clusterer__min_samples': min_samples,
    #})
    pipeline.set_params(**{
        'clusterer__n_clusters': k,
    })
    pipeline.fit(matrix)
    clusterer = pipeline.get_params()['clusterer']
    dump_graph(clusterer.labels_)

def dump_graph(labels_):
    X = pd.DataFrame()
    X['cluster'] = labels_
    X.to_csv('clusters.csv')

