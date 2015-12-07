library('ggplot2')

source('read-dataset.R')

keeps <- c(value_cols, "cluster", idvars)
data <- shaped[,(names(shaped) %in% keeps)]
data <- reshape(data, direction="long", varying=value_cols, timevar="ELEMENT", idvar=idvars)

graph <- ggplot(data, aes(cluster, VALUE)) +
  geom_boxplot(aes(fill=factor(cluster))) +
  facet_wrap(~ ELEMENT)

print(graph)
