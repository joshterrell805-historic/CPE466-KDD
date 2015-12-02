import numpy as np
from scipy.spatial.distance import euclidean
from sklearn.base import BaseEstimator, ClassifierMixin

class Hierarchical(BaseEstimator, ClassifierMixin):
    def fit(self, X, y=None):
        #self.hierarchy_ = Cluster()
        pass

class Cluster:
    @classmethod
    def from_xml(cls):
        #return Hierarchy()
        pass

    def __init__(self):
        self.clusters = None

    def to_xml(self):
        pass

    def cut(self, threshold):
        pass

    def dist(self, cluster):
        return euclidean(self.center(), cluster.center())

    def center(self):
        pass
