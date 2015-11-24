
def format(clusters):
    text = ""
    for cluster in clusters:
        name = cluster.name()
        count = cluster.size()
        
        x, y = cluster.centroid()

        max_dist = cluster.max_dist()
        min_dist = cluster.min_dist()
        average_dist = cluster.avg_dist()

        error = cluster.sse()

        """Cluster {}:
        Center: {},{}
        Max Dist. to Center: {}
        Min Dist. to Center: {}
        Avg Dist. to Center: {}
        {} Points:
""".format(name, x, y, max_dist, min_dist, avg_dist, count)
        for point in cluster.points():
            print("        {},{}\n".format(point.x, point.y))
