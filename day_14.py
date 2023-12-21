import dataclasses
import collections

real = ''

@dataclasses.dataclass
class Bound:
  north: int
  south: int
  east: int
  west: int


dish = real.split()
squares, rounds = set(), set()
limits = []
north_bounds = [-1] * len(dish[0])
for y, line in enumerate(dish):
  west_bound = -1
  limits.append([])
  for x, c in enumerate(line):
    limits[y].append(Bound(north_bounds[x], len(dish), len(line), west_bound))
    if c == '#':
      squares.add((x,y))
      for limit in limits[north_bounds[x]+1:]:
        limit[x].south = y
      for limit in limits[y][west_bound+1:]:
        limit.east = x
      north_bounds[x] = y
      west_bound = x
    elif c == 'O':
      rounds.add((x,y))

shifts = collections.Counter((x, limits[y][x].north) for x,y in rounds)
part_1 = []
for (x, y), count in shifts.items():
  part_1.extend((x, y + i + 1) for i in range(count))
print('Part 1:', sum(len(dish) - y for _, y in part_1))

def cycle(limits, rounds):
  shifts = collections.Counter((x, limits[y][x].north) for x,y in rounds)
  rounds = []
  for (x, y), count in shifts.items():
    rounds.extend((x, y + i + 1) for i in range(count))
  shifts = collections.Counter((limits[y][x].west, y) for x,y in rounds)
  rounds = []
  for (x, y), count in shifts.items():
    rounds.extend((x + i + 1, y) for i in range(count))
  shifts = collections.Counter((x, limits[y][x].south) for x,y in rounds)
  rounds = []
  for (x, y), count in shifts.items():
    rounds.extend((x, y - i - 1) for i in range(count))
  shifts = collections.Counter((limits[y][x].east, y) for x,y in rounds)
  rounds = []
  for (x, y), count in shifts.items():
    rounds.extend((x - i - 1, y) for i in range(count))
  return tuple(sorted(rounds)), rounds

seen = {}
results = []
for time in range(173):
  step, rounds = cycle(limits, rounds)
  results.append(sum(len(dish) - y for _, y in rounds))
  if step in seen:
    print('Part 2:', results[seen[step] + (1_000_000_000 - time) % (time - seen[step]) - 1])
    break
  seen[step] = time