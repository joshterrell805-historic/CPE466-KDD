import reader
import kmeans
import formatter

def main(datafile, k):
    data = reader.read_restricted(datafile)
    clusterer = kmeans.Clusterer(k)
    clusterer.data = data
    clusters = clusterer.cluster()
    print(formatter.format(clusters))
