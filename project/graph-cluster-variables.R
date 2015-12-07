library('ggplot2')

source('read-dataset.R')

keeps <- c(value_cols, "cluster")
data <- shaped[,(names(shaped) %in% keeps)]
data <- reshape(data, direction="long", varying=X, timevar="ELEMENT", idvar="X")

graph <- ggplot(data, aes(cluster, VALUE)) +
  geom_boxplot(aes(fill=factor(cluster))) +
  facet_wrap(~ ELEMENT)

print(graph)
