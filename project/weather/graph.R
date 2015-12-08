library('ggplot2')

source('read-dataset.R')


# keeps <- c(value_cols, idvars)
# data <- shaped[,keeps]
# data <- reshape(data, direction="long", varying=value_cols, timevar="ELEMENT", idvar=idvars)

# graph <- ggplot(data, aes(date, VALUE)) +
#   geom_point(aes(color=factor(cluster))) +
#   facet_wrap(~ ELEMENT)

# print(graph)


# for printing only
#data <- shaped[shaped$YEAR == 2005 & shaped$MONTH > 10,]
data <- shaped

data$rained <- data$VALUE.PRCP > 0
graph <- ggplot(data) +
   geom_point(aes(date, VALUE.PRCP, color=cluster))# +
#   geom_line(aes(date, VALUE.TMAX))

ggsave("kmeans--precip.png", width=16, height=9)
print(graph)
