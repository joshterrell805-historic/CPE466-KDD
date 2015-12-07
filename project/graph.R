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

shaped <- shaped[shaped$YEAR == 2013 & shaped$MONTH > 10,]

graph <- ggplot(data=shaped) +
    geom_point(mapping=aes(x=date, y=VALUE.PRCP, color=cluster))
        
print(graph)
