raw_dataset <- read.csv('../data/stocks/AAPL.labeled.csv', sep=',')
print(colnames(raw_dataset))
raw_dataset$timestamp <-
    as.POSIXlt(raw_dataset$timestamp, origin="1970-01-01")

feature_columns <- c(
  'sma_growth_288',
  'sma_growth_2016',
  'sma_delta_288_2016'
)

if (file.exists('../clusters.csv')) {
  raw_clusters <- read.csv('../clusters.csv')
  raw_dataset$cluster <- factor(raw_clusters$cluster)

  cluster_names <- unique(raw_clusters)
  cluster_sizes <- sapply(cluster_names, function(cluster) {
    sum(raw_dataset$cluster == cluster)
  })
}
