import random
class Clusterer:
    def __init__(self, kmeans=3):
        self.kmeans = kmeans

    def transform(self, data):
        self.last_sse = False
        centroids = self.select_centroids(data)
        while (not self.converged(data, centroids)):
            assignments = self.assign_points(data, centroids)
            centroids = self.update_centroids(data, assignments)
        return assignments

    def select_centroids(data):
        return random.sample(data, self.kmeans)

    def converged(data, centroids):
        sse = self.sse(data, centroids)
        if (self.last_sse):
            return self.last_sse - sse < 0.1
        else:
            self.last_sse = sse
            return False

    def assign_points(self, data, centroids):
        [self.assign_point(point, centroids) for point in data]

    def assign_point(self, point, centroids):
        min_dist = self.dist(point, centroids[0])
        min_centroid = centroids[0]
        for centroid in centroids[1:]:
            dist = self.dist(point, centroid)
            if (dist < min_dist):
                min_dist = dist
                min_centroid = centroid
        return min_centroid

    def sse(self, data, centroids):
        pass

    def update_centroids(self, data, assignments):
        pass

    def dist(self, point, centroid):
        point.euclidDist(centroid)
