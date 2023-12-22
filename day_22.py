import collections
import re

real = ''

air_bricks = sorted((tuple(map(int, re.findall('\d+', line)))
                     for line in real.splitlines()),
                     key = lambda brick: brick[2])

def gravity(highest_filled, bricks, removed=(0,0,0,0,0,0)):
  fallen_bricks = collections.defaultdict(list)
  fell = 0
  for x, y, z, X, Y, Z in bricks:
    if (x,y,z, X, Y, Z) == removed:
      continue
    below = max(highest_filled[a][b] for a in range(y, Y+1) for b in range(x, X+1))
    low = below + 1
    high = Z - z + low
    fell += low < z
    fallen_bricks[high].append((x, y, low, X, Y, high))
    for a in range(y, Y+1):
      for b in range(x, X+1):
        highest_filled[a][b] = high
  return fallen_bricks, fell

fallen_bricks, _ = gravity([[0] * 10 for _ in range(10)], air_bricks)
# Yes I really tried to be more intelligent than this ugly brute force.
ground_bricks = sorted((brick for stuff in fallen_bricks.values() for brick in stuff),
                key = lambda brick: brick[2])
loads = [gravity([[0] * 10 for _ in range(10)], ground_bricks, brick)[1]
         for brick in ground_bricks]
print('Part 1:', sum(not load for load in loads), '\tPart 2:', sum(loads))
