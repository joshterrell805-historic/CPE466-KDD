library('ggplot2')

source('read-dataset.R')

# for printing only
# data <- shaped[shaped$YEAR == 2013 & shaped$MONTH > 10,]

data <- shaped
data$rained <- data$VALUE.PRCP > 0
graph <- ggplot(data=shaped) +
    geom_point(mapping=aes(x=date, y=VALUE.PRCP, color=cluster)) + facet_wrap( ~ rained)
        
print(graph)
