source('read-data.R')
feature_columns <- c('sma_delta_288_2016')
print(feature_columns)
write.table(raw_dataset[,c(feature_columns)], "limited.csv")
