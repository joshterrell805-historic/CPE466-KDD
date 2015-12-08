source('read-dataset.R')

  shaped$VALUE.PRCP <- NULL
  value_cols <- value_cols[value_cols != "VALUE.PRCP"]
write.table(shaped[,value_cols], "input_for_clustering.csv", row.names=FALSE, na="0")