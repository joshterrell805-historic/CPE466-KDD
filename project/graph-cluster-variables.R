library('ggplot2')

source('read-dataset.R')

X <- c("VALUE.TMIN", "VALUE.TMAX", "VALUE.PRCP", "VALUE.AWND", "VALUE.WDF2",
           "VALUE.WDF5", "VALUE.WSF2", "VALUE.WSF5")
keeps <- c(X, "cluster")
d <- shaped[,(names(shaped) %in% keeps)]
print(colnames(d))
d <- reshape(d, direction="long", varying=X, timevar="ELEMENT", idvar="X")

graph <- ggplot(d, aes(cluster, VALUE)) +
  geom_boxplot(aes(fill=factor(cluster))) +
  facet_wrap(~ ELEMENT)

print(graph)
