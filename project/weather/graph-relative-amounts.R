library('ggplot2')
source('read-dataset.R')

thing <- shaped[shaped$VALUE.PRCP > 0,]
png("kmeans-relative-over-zero.png")
barplot(tapply(thing$VALUE.PRCP, thing$cluster, sum))
dev.off()

thing <- shaped[shaped$VALUE.PRCP == 0,]
png("kmeans-relative-is-zero.png")
barplot(tapply(thing$VALUE.PRCP, thing$cluster, length))
dev.off()