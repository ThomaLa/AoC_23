real = ''

tiles = real.split()

def transform(x, y, dx, dy):
  if not (0 <= x < len(tiles[0]) and 0 <= y < len(tiles)):
    return []
  what = tiles[y][x]
  if what == '/':
    return [(x - dy, y - dx, -dy, -dx)]
  if what == '\\':
    return [(x + dy, y + dx, dy, dx)]
  if what == '|' and dx:
    return [(x, y + 1, 0, 1), (x, y - 1, 0, -1)]
  if what == '-' and dy:
    return [(x + 1, y, 1, 0), (x - 1, y, -1, 0)]
  return [(x + dx, y + dy, dx, dy)]

def energize(state):
  seen = set()
  to_see = [state]
  while to_see:
    current = to_see.pop()
    if current in seen:
      continue
    future = transform(*current)
    if future:
      seen.add(current)
      to_see.extend(future)
  return len(set(current[:2] for current in seen))

print('Part 1:', energize((0, 0, 1, 0)))
results = []
for x in range(len(tiles[0])):
  results.extend([energize((x, 0, 0, 1)), energize((x, len(tiles) - 1, 0, -1))])
for y in range(len(tiles)):
  results.extend([energize((0, y, 1, 0)), energize((len(tiles[0]) - 1, y, -1, 0))])
print('Part 2:', max(results))