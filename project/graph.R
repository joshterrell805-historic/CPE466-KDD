library('ggplot2')

source('read-dataset.R')

shaped <- shaped[shaped$YEAR == 2013 & shaped$MONTH > 10,]

graph <- ggplot(data=shaped) +
    geom_point(mapping=aes(x=date, y=VALUE.PRCP, color=cluster))
        
print(graph)
