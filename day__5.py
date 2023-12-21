import re
import dataclasses
text = ''

# Even better, this one has forward declarations. I swear the next days are cleaner.

def from_spec(spec: str):
  other_min, this_min, size = spec.split()
  return Interval(int(this_min), int(this_min) + int(size), int(other_min) - int(this_min))

@dataclasses.dataclass(frozen=True)
class Interval:
  min: int
  max: int
  shift: int

  def __getitem__(self, key: tuple[int, int]):
    low, high = key
    if low < self.min:
      if high >= self.max:   # [ { } ]
        return self.min + self.shift, self.max + self.shift
      elif high <= self.min:  # [ ] { }
        return None
      else:                  # [ { ] }
        return self.min + self.shift, high + self.shift
    elif low >= self.max:    # { } [ ]
      return None
    elif high >= self.max:   # { [ } ]
      return low + self.shift, self.max + self.shift
    else:                    # { [ ] }
      return low + self.shift, high + self.shift

  def __repr__(self):
    return f"[{self.min}, {self.max}) -> {self.shift}"

class Map:
  origin: str
  destination: str
  intervals: list[Interval]

  def __init__(self, origin: str, destination: str, interval_specs: str):
    self.origin = origin
    self.destination = destination
    self.intervals = [from_spec(spec) for spec in interval_specs.split('\n')]
    lowest = min(i.min for i in self.intervals)
    highest = max(i.max for i in self.intervals)
    self.intervals += [Interval(0, lowest, 0), Interval(highest, 9876543210, 0)]

  def __repr__(self):
    intervals_string = '\n  '.join(str(i) for i in self.intervals)
    return f"{self.origin} -> {self.destination}:\n  {intervals_string}\n"

  def __getitem__(self, key: int):
    return [interval[key] for interval in self.intervals if interval[key]]

maps = {}
for origin, destination, interval_specs, _ in re.compile(
    '(.*)-to-(.*) map:\n((.+\n)+)\n').findall(text):
    maps[origin] = Map(origin, destination, interval_specs.strip())

def find_smallest(seeds):
  states = {'seed': seeds}
  state = 'seed'
  while state in maps:
    this_map = maps[state]
    next_states = []
    for i in states[state]:
      next_states.extend(this_map[i])
    state = this_map.destination
    states[state] = next_states
  return min(states['location'])[0]

seeds = [int(s) for s in text.split('\n\n', 1)[0].split()[1:]]
seeds_1 = [(low, low) for low in seeds]
seeds_2 = [(low, low + width - 1) for low, width in zip(seeds[::2], seeds[1::2])]
print(f'Part 1: {find_smallest(seeds_1)}, Part 2: {find_smallest(seeds_2)}')
