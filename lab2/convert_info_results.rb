#!/usr/bin/env ruby
class ResultReader
  def initialize
    @current = Result.new
    @results = []
  end
  def main
    @state = :need
    # States:
    # need
    # query
    # score
    # meta
    # text
    $<.each_line do |line|
      case @state
      when :need
        readNeed line
      when :query
        readQuery line
      when :score
        readScore line
      when :meta
        readMeta line
      when :text
        readText line
      else
        throw "wha"
      end
    end

    @results.each {|r| r.render}
  end

  def readScore line
    @current.score = line.strip
    @state = :meta
  end

  def readMeta line
    @current.meta = line.strip
    @state = :text
  end

  def readText line
    if /^\s+$/ =~ line
      restart
    else
      @current.text << line
    end
  end

  def readNeed line
    if /^\s+$/ =~ line
      @state = :query
    end
  end

  def readQuery line
    if /^\s+$/ =~ line
      @state = :score
    end
  end

  def restart
    @results << @current
    @current = Result.new
    @state = :score
  end
end


class Result
  attr_accessor :score, :meta, :text

  def initialize
    @text = ""
  end

  def render
    puts <<END
\\begin{result}{#{score}}{#{meta}}
#{text}\\end{result}

END
  end
end

r = ResultReader.new
r.main
