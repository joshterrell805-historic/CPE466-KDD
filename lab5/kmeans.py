import reader
import Clusterer from kmeans_clusterer
import formatter
from sklearn.pipeline import Pipeline

def main(datafile, k):
    data = reader.read_restricted(datafile)
    pipeline = Pipeline(steps=[('cluster', Clusterer(kmeans=k))])
    pipeline.fit()
    clusters = pipeline.cluster()
    print(formatter.format(clusters))
