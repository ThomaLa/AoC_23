import heapq

real = ''

heatmap = {(x, y): int(c)
           for y, line in enumerate(real.splitlines())
           for x, c in enumerate(line)}

def find(heatmap, min_inertia, max_inertia):
  destination = max(heatmap)
  to_see = [(0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0)]
  seen =   {key[1:]: 0 for key in to_see}
  heapq.heapify(to_see)
  while to_see:
    heat, x, y, dx, dy, inertia = heapq.heappop(to_see)
    if (x, y) == destination and inertia + 1 >= min_inertia:
      return heat
    for new_dx, new_dy in ((dx, dy), (dy, -dx), (-dy, dx)):
      new_x, new_y = x + new_dx, y + new_dy
      new_inertia = inertia + 1 if (dx, dy) == (new_dx, new_dy) else 0
      new_heat = heat + heatmap.get((new_x, new_y), 1e10)
      if new_inertia == max_inertia or (
         heat > 0 and new_inertia == 0 and inertia + 1 < min_inertia):
        continue
      new_state = new_heat, new_x, new_y, new_dx, new_dy, new_inertia
      if new_heat < seen.get(new_state[1:], new_heat + 1):
        heapq.heappush(to_see, new_state)
        seen[new_state[1:]] = new_heat

print('Part 1:', find(heatmap, 0, 3))
print('Part 2:', find(heatmap, 4, 10))