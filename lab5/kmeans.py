from kmeans_clusterer import Clusterer
import formatter
from sklearn.pipeline import Pipeline
import numpy as np
import pandas as pd

@click.command()
@click.argument('datafile', type=click.File('r'))
@click.argument('k', type=click.INT)
def main(datafile, k):
    header = datafile.readline()
    collist = [i for (i, toggle) in zip(count(), header.split()) if toggle == "0"]
    data = pd.read_csv(datafile, usecols = collist)
    pipeline = Pipeline(steps=[('cluster', Clusterer(kmeans=k))])
    pipeline.fit(data)
    clusters = pipeline.cluster(data)
    print(formatter.format(clusters))
