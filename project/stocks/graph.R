library('ggplot2')

source('read-data.R')

# for printing only
data <- raw_dataset

graph <- ggplot(data=data) +
    geom_point(mapping=aes(x=timestamp, y=price))
        
print(graph)
