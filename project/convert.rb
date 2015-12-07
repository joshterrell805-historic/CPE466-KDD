#!/usr/bin/env ruby

# This is the data conversion script from the format in which the data
# is available from the NOAA (a fixed-width format) to CSV.  It is
# primarily my work, although my younger brother was involved in
# writing it.

data = []
$<.each do |line|
  station = line[0..10]
  year = line[11..14].to_i
  month = line[15..16].to_i
  element = line[17..20]

  values = []
  (21..(line.length - 8)).step(8) do |i|
    value = line[i..i + 4].to_f/254
    if value == -9999
      next
    end
    observation = {}
    observation[:value] = value
    observation[:mflag] = line[i + 5]
    observation[:qflag] = line[i + 6]
    observation[:sflag] = line[i + 7]

    values << observation
  end

  data << {
    station: station,
    year: year,
    month: month,
    element: element,
    values: values
  }
end

puts "ID,YEAR,MONTH,DAY,ELEMENT,VALUE,MFLAG,QFLAG,SFLAG"
data.each do |row|
  row[:values].each_with_index do |observation, index|
    puts "#{row[:station]},#{row[:year]},#{row[:month]},#{index + 1},#{row[:element]},#{observation[:value]},#{observation[:mflag]},#{observation[:qflag]},#{observation[:sflag]}"
  end
end
