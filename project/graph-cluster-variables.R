library('ggplot2')

d <- read.csv('data/weather/USW00093209.dly.csv')
d <- d[d$YEAR >= 2010,]
shaped <- reshape(d[,c("ID","YEAR", "MONTH", "DAY", "ELEMENT", "VALUE")],
                  idvar=c("ID", "YEAR", "MONTH", "DAY"),
                  timevar=c("ELEMENT"),
                  direction="wide")
shaped$date <- ISOdate(shaped$YEAR, shaped$MONTH, shaped$DAY)
c <- read.csv('clusters.csv')
shaped$cluster <- factor(c$cluster)

X <- c("VALUE.TMIN", "VALUE.TMAX", "VALUE.PRCP", "VALUE.AWND", "VALUE.WDF2",
           "VALUE.WDF5", "VALUE.WSF2", "VALUE.WSF5")
keeps <- c(X, "cluster")
d <- shaped[,(names(shaped) %in% keeps)]
print(colnames(d))
d <- reshape(d, direction="long", varying=X, timevar="ELEMENT", idvar="X")

graph <- ggplot(d, aes(cluster, VALUE)) +
  geom_boxplot(aes(fill=factor(cluster))) +
  facet_wrap(~ ELEMENT)

print(graph)
