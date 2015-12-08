source('read-dataset.R')

  # shaped$VALUE.PRCP <- NULL
  # value_cols <- value_cols[value_cols != "VALUE.PRCP"]
  shaped$VALUE.AWND <- NULL
  value_cols <- value_cols[value_cols != "VALUE.AWND"]
  shaped$VALUE.WDF2 <- NULL
  value_cols <- value_cols[value_cols != "VALUE.WDF2"]
  shaped$VALUE.WDF5 <- NULL
  value_cols <- value_cols[value_cols != "VALUE.WDF5"]
  shaped$VALUE.WSF2 <- NULL
  value_cols <- value_cols[value_cols != "VALUE.WSF2"]
  shaped$VALUE.WSF5 <- NULL
  value_cols <- value_cols[value_cols != "VALUE.WSF5"]
  shaped$VALUE.SPREAD <- NULL
  value_cols <- value_cols[value_cols != "VALUE.SPREAD"]
  

write.table(shaped[,value_cols], "input_for_clustering.csv", row.names=FALSE, na="0")