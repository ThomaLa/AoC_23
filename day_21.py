real = ''

def get_valid(garden, position, reached, allow_repeats=False):
  x, y = position
  for nx, ny in ((x+1, y), (x, y+1), (x-1, y), (x, y-1)):
    if garden[ny % len(garden)][nx % len(garden[0])] != '#' and (nx, ny) not in reached and (
        allow_repeats or (0 <= nx < len(garden[0]) and 0 <= ny < len(garden))):
      yield nx, ny

garden = real.splitlines()
T = len(garden)
position = None
for y, line in enumerate(garden):
  for x, c in enumerate(line):
    if c == 'S':
      position = x, y
      break

def filled(start, time=len(garden), allow_repeats=False):
  reached = [set(), set()]
  reachable = [start]
  for step in range(time):
    reached[step%2].update(reachable)
    reachable = set(valid for position in reachable for valid in get_valid(
        garden, position, reached[(step+1)%2], allow_repeats=allow_repeats))
  return set(reachable) | reached[time%2]

print('Part 1:', len(filled(position, 64)))
# No need for second order: squares are filled after 2T, so I only need to
# check what happens to the edge of the lozenge.
full_even = len(filled(position, T))  # Confirmed to be stable before T
full_odd = len(filled(position, T + 1))  # ... but parity >.<
directs = [filled(p, T) for p in ((0,T//2), (T//2, 0), (T-1, T//2), (T//2, T-1))]
diagonals = sum(len(a|b) for a,b in zip(directs, directs[1:] + [directs[0]]))

N = (26501365 - T//2)//T  # Number of iterations for which everything is filled.
# After N steps (the first one being a half step), the lozenge has N²+(N-1)² tiles.
# (N-1)² have the same parity as the border, N² are the opposite
print('Part 2 (but wrong):', 
        N*N*full_even + (N-1)*(N-1)*full_odd
      + sum(len(d) for d in directs) + (N - 1) * diagonals)

# OK I'm tired, let's just interpolate a quadratic function f(N) = aNN + bN + c.
# After all I think my formula above should work, and it's quadratic in N...
# So. if I know f(0), f(1) and f(2):
#  f(0) = c                b = f(1) - f(0) - a
#  f(1) = a + b + c        f(2) = 4a + 2(f(1)-f(0)-a) + f(0) = 2a + 2f(1) - f(0)
#  f(2) = 4a + 2b + c      a = (f(2) - 2f(1) + f(0)) / 2
#  f(N) = aNN + (f(1) - f(0) - a)N + c = N((N-1)*a + f(1) - f(0)) + c
zero, one, two = [len(filled(position, i * T + T//2, True)) for i in range(3)]
print('Part 2 for real:',
      N * ((N-1) * (two - 2*one + zero) // 2 + one - zero) + zero)