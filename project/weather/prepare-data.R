source('read-dataset.R')
write.table(shaped[,value_cols], "input_for_clustering.csv", row.names=FALSE, na="0")