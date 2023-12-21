import functools

real = ''

@functools.lru_cache
def num_possible(drawing, specs):
  if not drawing:
    return not specs
  result = 0
  if drawing[0] != '#':
    result += num_possible(drawing[1:], specs)
  if (specs
      and len(drawing) > specs[0]
      and all(c in '?#' for c in drawing[:specs[0]])
      and drawing[specs[0]] in '.?'):
    result += num_possible(drawing[specs[0]+1:], specs[1:])
  return result

def try_again(line, repeats=1):
  drawing, specs = line.split()
  specs = tuple(int(i) for i in specs.split(",")) * repeats
  return num_possible('?'.join([drawing]*repeats) + '.', specs)

print('Part 1:', sum(try_again(line) for line in real.strip().splitlines()))
print('Part 2:', sum(try_again(line, 5) for line in real.strip().splitlines()))
