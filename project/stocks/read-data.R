if (!exists('raw_dataset')) {
  raw_dataset <- read.csv('../data/stocks/COKE.csv', sep='\t')
  raw_dataset <- raw_dataset[, c('timestamp', 'price')]
  print(colnames(raw_dataset))

  #if (file.exists('../clusters.csv')) {
  #  raw_clusters <- read.csv('../clusters.csv')
  #  shaped$cluster <- factor(raw_clusters$cluster)

  #  cluster_names <- unique(raw_clusters)
  #  cluster_sizes <- sapply(cluster_names, function(cluster) {
  #    sum(d$cluster == cluster)
  #  })
  #}
}
