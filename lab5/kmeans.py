import formatter
import numpy as np
import numpy.random
from sklearn.pipeline import Pipeline
import numpy as np
import pandas as pd
import click

from kmeans_clusterer import KMeans

@click.command()
@click.argument('datafile', type=click.File('r'))
@click.argument('k', type=click.INT)
def main(datafile, k):
    header = datafile.readline()
    collist = [i for (i, toggle) in zip(count(), header.split()) if toggle == "0"]
    data = pd.read_csv(datafile, usecols = collist)

    pipeline = Pipeline([('clf', KMeans())])
    pipeline.set_params(**{
        'clf__k': k,
        'clf__delta_sse': 4,
    })
    pipeline.fit(data)
    clf = pipeline.get_params()['clf']
    print('\n'.join(str(c) for c in clf.clusters_))
