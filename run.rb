require "fileutils"

HERE = File.absolute_path(File.split(__FILE__).first)

def post
  case RUBY_DESCRIPTION
  when /arm64.*darwin/; "macm1"
  when /aarch64.*linux/; "rp64"
  when /arm.*linux/; "rp32"
  else
    raise "unexpected #{RUBY_DESCRIPTION.inspect}"
  end
end

def gopath
  %w(
    /opt/homebrew/bin/go
    /usr/local/go/bin/go
  ).find{ |x| File.exist?(x) }
end

def rungo
  Dir.chdir( "goma" ) do
    puts %x( #{gopath} build . )
    5.times do |ix|
      %w( c l ).each do |x|
        res = %x(./goma #{x})
        puts res
        File.open( "../res/go_#{x}_#{post}_#{ix}.csv", "w" ){ |f| f.puts res }
      end
    end
  end
end

def cpp(cc, name)
  Dir.chdir( "cpp" ) do
    exe = "./" + [post, "out"].join(".")
    puts %x( #{cc} -Wall -std=c++17 -O2 main.cpp -o #{exe} )
    5.times do |ix|
      %w( c m v r s n ).each do |x|
        res = %x(#{exe} #{x})
        puts res
        File.open( "../res/cpp_#{name}_#{x}_#{post}_#{ix}.csv", "w" ){ |f| f.puts res }
      end
    end
  end
end

Dir.chdir( HERE ) do
  FileUtils.mkdir_p("res")
  rungo
  cpp("/usr/bin/clang++", "clang")
  if /darwin/===RUBY_DESCRIPTION
    cpp("/opt/homebrew/bin/g++-13", "gcc")
  else
    cpp("/usr/bin/g++-10", "gcc")
  end
end