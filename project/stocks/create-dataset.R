source('lib/sma.R'); 
source('lib/growth.R'); 

quotes <- read.csv('../data/stocks/COKE.csv', sep='\t')
quotes <- na.omit(quotes)
quotes$date <- as.POSIXlt(quotes$timestamp, origin="1970-01-01")
quotes <- quotes[1:50000,]

periods <- c(500, 1500, 5000);
for (period in periods) {
  quotes[,paste('sma', period, sep='_')] = sma(quotes, 'price', period)
  print(paste('done associating sma_', period, sep=''))
}

quotes <- na.omit(quotes)

for (p in periods) {
    name = paste('sma', 'growth', p, sep='_')
    quotes[,name] = growth(quotes, paste('sma', p, sep='_'), p)
    print(paste('done associating sma_growth_', p, sep=''))
}

quotes <- na.omit(quotes)
quotes <- quotes[,!(names(quotes) %in% c('date'))]
write.csv(quotes, file='../data/stocks/COKE.labeled.csv')
