source('sma.R')
value_cols <- c("VALUE.TMIN", "VALUE.TMAX", "VALUE.PRCP", "VALUE.AWND",
    "VALUE.WDF2", "VALUE.WDF5", "VALUE.WSF2", "VALUE.WSF5")

if (!exists('raw_dataset')) {
  raw_dataset <- read.csv('../data/weather/USW00093209.dly.csv')
#  raw_dataset <- raw_dataset[raw_dataset$YEAR >= 2001,]

  limited <- raw_dataset[raw_dataset$YEAR >= 2001 & raw_dataset$YEAR <= 2010,]
  idvars = c("ID", "YEAR", "MONTH", "DAY")
  shaped <- reshape(
      limited[,c("ID","YEAR", "MONTH", "DAY", "ELEMENT", "VALUE")],
      idvar=idvars,
      timevar=c("ELEMENT"),
      direction="wide")
  shaped$date <- ISOdate(shaped$YEAR, shaped$MONTH, shaped$DAY)
  idvars <- c(idvars, "date")

# shaped$VALUE.TMAX_SMA_3 <- sma(shaped, "VALUE.TMAX", 3)
# value_cols <- c(value_cols, "VALUE.TMAX_SMA_3")
# shaped$VALUE.TMIN_SMA_3 <- sma(shaped, "VALUE.TMIN", 3)
# value_cols <- c(value_cols, "VALUE.TMIN_SMA_3")
# shaped$VALUE.TMAX_SMA_5 <- sma(shaped, "VALUE.TMAX", 5)
# value_cols <- c(value_cols, "VALUE.TMAX_SMA_5")
# shaped$VALUE.TMIN_SMA_5 <- sma(shaped, "VALUE.TMIN", 5)
# value_cols <- c(value_cols, "VALUE.TMIN_SMA_5")
shaped$VALUE.SPREAD <- shaped$VALUE.TMAX - shaped$VALUE.TMIN
value_cols <- c(value_cols, "VALUE.SPREAD")

#  vals <- sapply(shaped$VALUE.PRCP, log)
#  vals[shaped$VALUE.PRCP == 0] <- 0
#  shaped$VALUE.PRCP <- vals
#  shaped <- tail(shaped, -2)

  if (file.exists('clusters.csv')) {
    raw_clusters <- read.csv('clusters.csv')
    shaped$cluster <- factor(raw_clusters$cluster)
    idvars <- c(idvars, "cluster")

    cluster_names <- unique(raw_clusters)
    cluster_sizes <- sapply(cluster_names, function(cluster) {
      sum(raw_clusters$cluster == cluster)
    })
  }
}
