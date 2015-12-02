library('ggplot2')
data = read.csv('graph.csv')
data$assignment = factor(data$assignment)
graph = ggplot(data, aes(x=X0, y=X1, colour=assignment)) +
  geom_point()
print(graph)
