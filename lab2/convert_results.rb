#!/usr/bin/env ruby
class ResultReader
  def initialize
    @current = Result.new
    @results = []
  end
  def main
    @state = :relevant
    # States:
    # score
    # meta
    # text
    $<.each_line do |line|
      line.gsub!(/%/, '\%')
      case @state
      when :relevant
        readRelevant line
      when :score
        readScore line
      when :meta
        readMeta line
      when :text
        readText line
      else
        puts "wha"
      end
    end

    @results << @current
    @results.each {|r| r.render}
  end

  def readRelevant line
    line = line.strip

    if line == 'relevant'
      @current.relevant = true 
    elsif line == 'not relevant'
      @current.relevant = false
    else
      raise 'relevance line should be "relevant" or "not relevant"'
    end
      
    @state = :score
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

  def restart
    @results << @current
    @current = Result.new
    @state = :relevant
  end
end


class Result
  attr_accessor :relevant, :score, :meta, :text

  def initialize
    @text = ""
  end

  def render
    @text = if @relevant then "\\textbf{#{text}}" else @text end
    puts <<END
\\begin{result}{#{score}}{#{meta}}
#{text}\\end{result}

END
  end
end

r = ResultReader.new
r.main
