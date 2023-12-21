import dataclasses

real = ''  # Yes I did this in a notebook. Don't judge.

@dataclasses.dataclass(frozen=True)
class Coordinates:
  x: int
  y: int

  def __add__(self, other):
    return Coordinates(self.x + other.x, self.y + other.y)

  def __sub__(self, other):
    return Coordinates(self.x - other.x, self.y - other.y)

  def in_bounds(self):
    return self.x >= 0 and self.y >= 0 and self.x < len(drawing[0]) and self.y < len(drawing)

  def almost_in_bounds(self):
    return self.x >= -1 and self.y >= -1 and self.x <= len(drawing[0]) and self.y <= len(drawing)

  def adjacent(self, other):
    other_to_self = self - other
    self_to_other = other - self
    return other_to_self in possible[drawing[other.y][other.x]] and self_to_other in possible[drawing[self.y][self.x]]



directions = dict(N=Coordinates(0, -1),
                  S=Coordinates(0, 1),
                  E=Coordinates(1, 0),
                  W=Coordinates(-1, 0))
possible = {key: [directions[point] for point in values] for (key, values) in {
    '|': 'NS',
    '-': 'EW',
    'L': 'NE',
    'J': 'NW',
    '7': 'SW',
    'F': 'SE',
    '.': '',
    'S': 'NSEW'
}.items()}

drawing = real.splitlines()
# Find S
for y, line in enumerate(drawing):
  found = True
  for x, c in enumerate(line):
    if c == 'S':
      break
  else:
    found = False
  if found:
    break
# Move around the loop
previous = None
position = Coordinates(x, y)
boundary = set()
symbol = None
for time in range(len(drawing) * len(drawing[0])):
  boundary.add(position)
  symbol = drawing[position.y][position.x]
  for move in possible[symbol]:
    neighbor = position + move
    if neighbor != previous and neighbor.in_bounds() and neighbor.adjacent(position):
      previous = position
      position = neighbor
      break
  if time > 0 and symbol == 'S':
    break
print('Part 1:', time // 2)

part2 = 0
for y, line in enumerate(drawing):
  is_in = False
  previous_vertical = None
  for x, c in enumerate(line):
    position = Coordinates(x, y)
    if position not in boundary:
      if is_in:
        part2 += 1
    elif c == '-':
      continue
    else:
      if c in 'FL':
        previous_vertical = c
      elif (c == 'J' and previous_vertical == 'F') or (c == '7' and previous_vertical == 'L'):
        continue  # We already swapped when encountering the previous character.
      is_in = not is_in
print('Part 2:', part2)