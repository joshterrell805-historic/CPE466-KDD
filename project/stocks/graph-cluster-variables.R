library('ggplot2')

source('read-data.R')

keeps <- c('sma_delta_288_2016', "cluster", 'timestamp')
data <- raw_dataset[,(names(raw_dataset) %in% keeps)]
#data <- reshape(data, direction="long", varying=c('sma_delta_288_2016'), timevar=c('timestamp'), idvar=c('timestamp'))

graph <- ggplot(data, aes(cluster, sma_delta_288_2016)) +
  geom_boxplot(aes(fill=factor(cluster)))

print(graph)
