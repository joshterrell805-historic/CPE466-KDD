if (!exists('raw_dataset')) {
  raw_dataset <- read.csv('data/weather/USW00093209.dly.csv')
  raw_dataset <- raw_dataset[raw_dataset$YEAR >= 2010,]

  shaped <- reshape(
      raw_dataset[,c("ID","YEAR", "MONTH", "DAY", "ELEMENT", "VALUE")],
      idvar=c("ID", "YEAR", "MONTH", "DAY"),
      timevar=c("ELEMENT"),
      direction="wide")
  shaped$date <- ISOdate(shaped$YEAR, shaped$MONTH, shaped$DAY)

  if (file.exists('clusters.csv')) {
    raw_clusters <- read.csv('clusters.csv')
    shaped$cluster <- factor(raw_clusters$cluster)

    cluster_names <- unique(raw_clusters)
    cluster_sizes <- sapply(cluster_names, function(cluster) {
      sum(d$cluster == cluster)
    })
  }

  value_cols <- c("VALUE.TMIN", "VALUE.TMAX", "VALUE.PRCP", "VALUE.AWND",
      "VALUE.WDF2", "VALUE.WDF5", "VALUE.WSF2", "VALUE.WSF5")
}
