library('ggplot2')

source('read-data.R')

# for printing only
data <- raw_dataset
#data <- data[data$timestamp > as.POSIXct("2015-02-01 12:00:00", tz = "UTC"),]
#data <- data[data$timestamp < as.POSIXct("2015-07-04 12:00:00", tz = "UTC"),]

graph <- ggplot(data=data) +
    geom_point(mapping=aes(x=timestamp, y=price, color=cluster), size=1) +
    geom_line(mapping=aes(x=timestamp, y=sma_500), color='#440000') +
    geom_line(mapping=aes(x=timestamp, y=sma_1500), color='#990000') +
    geom_line(mapping=aes(x=timestamp, y=sma_5000), color='#FF0000')
        
print(graph)
