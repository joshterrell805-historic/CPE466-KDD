library('ggplot2')
source('read-data.R')
data = raw_dataset
graph = ggplot(data, aes(x=sma_growth_288, y=sma_delta_288_2016, colour=cluster)) +
  geom_point()
print(graph)
