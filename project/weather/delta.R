
delta = function(data, column, count) {
 return(sapply(1:nrow(data), function(i) {
   if (i < count) {
     return(NA);
   } else {
     start = i - count + 1
     return(data[start, column] - data[start + count-1, column]);
}}))
}
