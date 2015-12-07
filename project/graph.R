library('ggplot2')

source('read-dataset.R')

# for printing only
data <- shaped[shaped$YEAR == 2013 & shaped$MONTH > 10,]

graph <- ggplot(data=data) +
    geom_point(mapping=aes(x=date, y=VALUE.PRCP, color=cluster))
        
print(graph)
