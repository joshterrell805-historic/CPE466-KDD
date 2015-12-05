import numpy as np
import xml.etree.ElementTree as ET
from scipy.spatial.distance import euclidean
from sklearn.base import BaseEstimator, ClassifierMixin

class Hierarchical(BaseEstimator, ClassifierMixin):
    def fit(self, X, y=None):
        clusters = [Cluster([X[x]]) for x in range(X.shape[0])]

        while len(clusters) > 1:
            clusters = self.merge_closest(clusters)

        self.hierarchy_ = clusters[0]

    def merge_closest(self, clusters):
        closest_dist = None
        closest_pair = None

        for i in range(len(clusters)-1):
            for j in range(i+1, len(clusters)):
                dist = clusters[i].dist(clusters[j])
                if closest_dist == None or dist < closest_dist:
                    closest_dist = dist
                    closest_pair = [i, j]


        closest_pair = sorted(closest_pair)
        merged = Cluster([
            clusters[closest_pair[0]],
            clusters[closest_pair[1]]
        ])
        del clusters[closest_pair[1]]
        del clusters[closest_pair[0]]
        return clusters + [merged]

class Cluster:
    header = \
"""
Center: {}
Max Dist. to Center: {}
Min Dist. to Center: {}
Avg Dist. to Center: {}
{} Points:
{}
"""

    @classmethod
    def from_xml(cls, xml):
        if xml.tag == 'node' or xml.tag == 'tree':
            children = list(xml)
            if xml.tag == 'tree' and len(list(xml)) == 1:
                return Cluster.from_xml(list(xml)[0])
            else:
                return Cluster([cls.from_xml(child) for child in children])
        if xml.tag == 'leaf':
            data = xml.get('data').replace('[', '').replace(']', '')
            array = np.fromstring(data, sep=', ')
            return Cluster([array])

    def __init__(self, clusters, k=0):
        self.clusters = clusters

    def height(self):
        return 0 if len(self.clusters) == 1 else\
                self.clusters[0].dist(self.clusters[1])

    def to_xml(self, parent=None):
        tree = -1
        if len(self.clusters) == 2:
            if parent == None:
                me = ET.Element("tree")
                tree = ET.ElementTree(element=me)
            else:
                me = ET.SubElement(parent, "node")
            me.set("height", str(self.height()))
            for child in self.clusters:
                child.to_xml(me)
        elif len(self.clusters) == 1:
            if parent == None:
                parent = ET.Element("tree")
                parent.set("height", '0.0')
            me = ET.SubElement(parent, "leaf")
            me.set("data", str(self.clusters[0].tolist()))
            tree = parent
        else:
            raise Exception("Incorrect number of child nodes")

        return tree.getroot() if parent == None else tree

    def cut(self, threshold):
        if len(self.clusters) == 1:
            return [self]
        else:
            if self.clusters[0].dist(self.clusters[1]) >= threshold:
                return self.clusters[0].cut(threshold) +\
                        self.clusters[1].cut(threshold)
            else:
                return [self]

    def dist(self, cluster):
        return euclidean(self.center(), cluster.center())

    def center(self):
        if len(self.clusters) == 1:
            return self.clusters[0]
        else:
            return np.mean([c.center() for c in self.clusters], axis=0)

    def to_str(self, k):
        return 'Cluster {}:\n{}'.format(k, str(self))

    def get_points(self):
        if len(self.clusters) == 1:
            return self.clusters
        else:
            return self.clusters[0].get_points() + self.clusters[1].get_points()

    def __str__(self):
        X = np.array(self.get_points())
        data = {
            'size': X.shape[0],
            'center': ', '.join(str(x) for x in self.center().tolist()),
            'max_dist': -1 if X.shape[0] == 0 else max(
                euclidean(x, self.center()) for x in X.tolist()
            ),
            'min_dist': -1 if X.shape[0] == 0 else min(
                euclidean(x, self.center()) for x in X.tolist()
            ),
            'mean_dist': -1 if X.shape[0] == 0 else np.mean([
                euclidean(x, self.center()) for x in X.tolist()
            ]),
            'points': X
        }
        return self.header.format(
            data['center'],
            data['max_dist'],
            data['min_dist'],
            data['mean_dist'],
            data['size'],
            '\n'.join(
                ', '.join(str(x) for x in row)
                for row in data['points'].tolist()
            )
        )

    def is_eq(self, l, r):
        if l is Cluster:
            return l == r
        else:
            return np.array_equal(l, r)

    def __eq__(self, other):
        return len(self.clusters) == len(other.clusters) and \
               self.is_eq(self.clusters[0], other.clusters[0]) and \
               (True if len(self.clusters) == 1 else \
               self.is_eq(self.clusters[1], other.clusters[1]))
