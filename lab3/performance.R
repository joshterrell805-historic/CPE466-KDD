library('ggplot2');
data = read.csv('performance.csv');
# print(data);

xlimits = c(
  floor(min(data$edge_count) * 0.9),
  ceiling(max(data$edge_count) * 1.1)
);
ylimits = c(
  floor(min(data$execution_seconds) * 0.9),
  ceiling(max(data$execution_seconds) * 1.1)
);

fn_smooth <- smooth.spline(x=data$edge_count, y=data$execution_seconds);
data$smooth = data.frame(predict(fn_smooth, data$edge_count))$y;

graph <- ggplot() +
    geom_point(data=data , aes(x=edge_count, y=execution_seconds)) +
    stat_smooth(data=data , aes(x=edge_count, y=smooth)) +
    scale_y_continuous(trans='log2') +
    scale_x_continuous(trans='log2') +
    xlab('Edge Count') +
    ylab('Execution Seconds');

# print(graph);
ggsave(plot=graph, 'performance.png');
dev.off();
