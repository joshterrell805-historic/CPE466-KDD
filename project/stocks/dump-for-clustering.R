source('read-data.R')
feature_columns <- c('sma_growth_500')
print(feature_columns)
write.table(raw_dataset[,c(feature_columns)], "limited.csv")
