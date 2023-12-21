import math

real = ''

class FlipFlop:
  origin: str
  destinations: list[str]
  state: bool = False  # ON/OFF

  def __init__(self, origin: str, destinations: str):
    self.origin = origin
    self.destinations = destinations.split(', ')

  def process(self, origin: str, pulse: bool, all_pulses: list):  # True == high
    del origin
    if not pulse:
      self.state = not self.state
      all_pulses.extend((d, self.origin, self.state) for d in self.destinations)

class Conjunction:
  origin: str
  destinations: list[str]
  inputs: dict[str, bool]

  def __init__(self, origin: str, destinations: str):
    self.origin = origin
    self.destinations = destinations.split(', ')
    self.inputs = {}

  def process(self, origin: str, pulse: bool, all_pulses: list):
    self.inputs[origin] = pulse
    all_pulses.extend((d, self.origin, not all(self.inputs.values()))
                      for d in self.destinations)

class Broadcaster:
  origin: str
  destinations: list[str]

  def __init__(self, origin: str, destinations: str):
    self.origin = origin
    self.destinations = destinations.split(', ')

  def process(self, origin: str, pulse: bool, all_pulses: list):
    del origin
    all_pulses.extend((d, self.origin, pulse) for d in self.destinations)

class Output:
  destinations = []
  def process(self, origin: str, pulse: bool, all_pulses: list):
    pass

gates = {'output': Output(), 'rx': Output()}
needed_for_rx = 'xl','ln','xp','gp'
for line in real.splitlines():
  key, destination = line.split(' -> ')
  if key[0] == '%':
    gates[key[1:]] = FlipFlop(key[1:], destination)
  elif key[0] == '&':
    gates[key[1:]] = Conjunction(key[1:], destination)
  else:
    gates[key] = Broadcaster(key, destination)
for key, gate in gates.items():
  for d in gate.destinations:
    if hasattr(gates[d], 'inputs'):
      gates[d].inputs[key] = False

res = {True: 0, False: 0}
earliest_reached = {}
def push():
  pulses = [('broadcaster', 'button', False)]
  reached = set()
  while pulses:
    destination, origin, pulse = pulses.pop(0)
    if not pulse and destination not in earliest_reached:
      reached.add(destination)
    gates[destination].process(origin, pulse, pulses)
    res[pulse] += 1
  return reached

for i in range(1_000_000):
  if i == 1000:
    print('Part 1:', res[True] * res[False], flush=True)
  reached = push()
  for s in reached - set(earliest_reached):
    earliest_reached[s] = i+1
  if all(s in earliest_reached for s in needed_for_rx):
    print('Part 2:', math.lcm(*[earliest_reached[s] for s in needed_for_rx]))
    break