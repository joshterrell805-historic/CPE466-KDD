import numpy as np
from scipy.spatial.distance import euclidean
from sklearn.base import BaseEstimator, ClassifierMixin

class KMeans(BaseEstimator, ClassifierMixin):
    def __init__(self, k=3, delta_sse=0.1):
        self.k = k

    def fit(self, X, y=None):
        self.last_sse = False
        self.iteration = 0

        centroids = self.select_centroids(X)
        assignments = self.assign_points(X, centroids)

        while not self.converged(X, centroids, assignments):
            assignments = self.assign_points(X, centroids)
            centroids = self.update_centroids(X, assignments)

        self.centroids_ = centroids
        self.assignments_ = assignments
        self.clusters_ = self.clusters(X, centroids, assignments)

    def select_centroids(self, X):
        indexes = np.random.randint(0, X.shape[0], self.k)
        return X[indexes]

    def converged(self, X, centroids, assignments):
        sse = self.sse(X, centroids, assignments)
        converged = False

        if self.last_sse:
            diff = self.last_sse - sse
            converged = diff < self.delta_sse

        self.last_sse = sse
        return converged

    def assign_points(self, X, centroids):
        return [self.assign_point(point, centroids) for point in X]

    def assign_point(self, point, centroids):
        min_dist = euclidean(point, centroids[0])
        min_centroid = 0

        for i in range(1, len(centroids)):
            dist = euclidean(point, centroids[i])
            if (dist < min_dist):
                min_dist = dist
                min_centroid = i

        return min_centroid

    def sse(self, X, centroids, assignments):
        return sum(
            euclidean(X[i], centroids[a]) for i,a in enumerate(assignments)
        )

    def update_centroids(self, X, assignments):
        return np.array([
            np.mean(X[[i for i,a in enumerate(assignments) if a == k]], axis=0)
            for k in range(self.k)
        ])

    def clusters(self, X, centroids, assignments):
        clusters = []
        for k in range(self.k):
            size = sum(1 for i,a in enumerate(assignments) if a == k)
            clusters.append(Cluster({
                'k': k,
                'size': size,
                'center': ', '.join(str(x) for x in centroids[k].tolist()),
                'max_dist': -1 if size == 0 else max(
                    euclidean(X[i], centroids[k])
                    for i,a in enumerate(assignments) if a == k
                ),
                'min_dist': -1 if size == 0 else min(
                    euclidean(X[i], centroids[k])
                    for i,a in enumerate(assignments) if a == k
                ),
                'mean_dist': -1 if size == 0 else np.mean([
                    euclidean(X[i], centroids[k])
                    for i,a in enumerate(assignments) if a == k
                ]),
                'points': X[[i for i,a in enumerate(assignments) if a == k]],
            }))
        return clusters

class Cluster:
    header = \
"""
Cluster {}:
Center: {}
Max Dist. to Center: {}
Min Dist. to Center: {}
Avg Dist. to Center: {}
{} Points:
{}
"""

    def __init__(self, data):
        self.data = data

    def __str__(self):
        return self.header.format(
            self.data['k'],
            self.data['center'],
            self.data['max_dist'],
            self.data['min_dist'],
            self.data['mean_dist'],
            self.data['size'],
            '\n'.join(
                ', '.join(str(x) for x in row)
                for row in self.data['points'].tolist()
            )
        )
        
