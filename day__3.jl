include("base.jl")

struct Gear
  symbol::Char
  y::Int
  x::Int
end

struct Operand
  value::Int
  y::Int
  x::Int
end
value(op) = op.value

open(Personal.to_path(ARGS[1]), "r") do input
  text = readlines(input)
  operations = Dict{Gear, Set{Operand}}()
  for (y, line) in enumerate(text), (x, char) in enumerate(line)
    if char == '.' || isdigit(char)
      continue
    end
    for dy = -1:1, dx = -1:1
      if !checkbounds(Bool, text, y + dy) ||
         !checkbounds(Bool, text[y + dy], x + dx) ||
         !isdigit(text[y + dy][x + dx])
        continue
      end
      number_line = text[y + dy]
      min_x = x + dx
      while checkbounds(Bool, number_line, min_x) && isdigit(number_line[min_x])
        min_x -= 1
      end
      max_x = x + dx
      while checkbounds(Bool, number_line, max_x) && isdigit(number_line[max_x])
        max_x += 1
      end
      push!(get!(operations, Gear(char, y, x), Set{Operand}()),
            Operand(parse(Int, number_line[min_x+1:max_x-1]), y + dy, max_x))
    end
  end

  part1 = union(values(operations)...) .|> value |> sum
  stars = filter(((gear, operands),) -> gear.symbol == '*' && length(operands) == 2, operations)
  part2 = sum(operation -> prod(value, operation), values(stars))
  println("1: $part1 2: $part2")
end

