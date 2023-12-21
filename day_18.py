real = ''

# Actually doable in SQL (contrary to day 10 the path can be merged in log(N)
# steps, which is less than 100), but i lack time.

directions = [(1,0), (0, 1), (-1, 0), (0, -1)]
codes = {c: i for i, c in enumerate('RULD')}

def go(position, line, part):
  code, n, color = line.split()
  if part == 1:
    direction = directions[codes[code]]
    distance = int(n)
  else:
    direction = directions[int(color[-2])]
    distance = int(color[2:-2], 16)
  return position[0] + distance * direction[0], position[1] + distance * direction[1]

def to_index(coords, coord):
  for i, c in enumerate(coords):
    if c == coord:
      return 2*i

def solve(lines, part):
  segments, split_segments = set(), set()
  position = 0, 0
  for line in lines.splitlines():
    next_position = go(position, line, part)
    segments.add((position, next_position))
    position = next_position

  xs = sorted(set(pos[0] for segment in segments for pos in segment))
  ys = sorted(set(pos[1] for segment in segments for pos in segment))
  for segment in segments:
    x = to_index(xs, segment[0][0])
    y = to_index(ys, segment[0][1])
    for i, (low, high) in enumerate(zip(xs[:-1], xs[1:])):
      if (low >= segment[0][0] and high <= segment[1][0]) or (low >= segment[1][0] and high <= segment[0][0]):
        x = 2 * i
        split_segments.update([(x, y), (x+1, y), (x+2, y)])
    for i, (low, high) in enumerate(zip(ys[:-1], ys[1:])):
      if (low >= segment[0][1] and high <= segment[1][1]) or (low >= segment[1][1] and high <= segment[0][1]):
        y = 2 * i
        split_segments.update([(x, y), (x, y+1), (x, y+2)])

  values_x = [1]
  for low, high in zip(xs[:-1], xs[1:]):
    values_x.extend([high - low - 1, 1])
  values_y = [1]
  for low, high in zip(ys[:-1], ys[1:]):
    values_y.extend([high - low - 1, 1])
  interior = 0
  for y in range(2 * len(ys) + 1):
    inside = False
    previous = None
    for x in range(2 * len(xs) + 1):
      if (x, y) in split_segments:
        if previous is None:
          previous = (x, y+1) in split_segments
        interior += values_x[x] * values_y[y]
      else:
        if previous is not None:
          if previous == ((x-1, y-1) in split_segments):
            inside = not inside
          previous = None
        if inside:
          interior += values_x[x] * values_y[y]
  return interior

print('Part 1:', solve(real, 1), ' ', 'Part 2:', solve(real, 2))