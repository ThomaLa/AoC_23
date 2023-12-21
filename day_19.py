import collections
import functools
import re

real = ''

workflow, parts = real.split('\n\n')

Part = collections.namedtuple('Part', 'x, m, a, s')

def create_part(line):
  return Part(*[int(i) for i in re.findall('=(\d+).', line)])

class Rule:
  c: str
  above: bool
  target: int
  destination: str

  def __init__(self, token: str):
    if ':' not in token:
      self.c = 'x'
      self.above = True
      self.target = 0  # all part counts are positive
      self.destination = token
    else:
      self.c = token[0]
      self.above = token[1] == '>'
      left, self.destination = token.split(':')
      self.target = int(left[2:])

  def apply(self, part: Part):
    return self.destination if (self.target - getattr(part, self.c)) * (1 if self.above else -1) < 0 else None

class Rules:
  def __init__(self, right: str):
    self.rules = [Rule(token) for token in right.strip('}').split(',')]

  def apply(self, part: Part):
    for rule in self.rules:
      if (res := rule.apply(part)) is not None:
        return res

def prodsum(a, b):
  res = 1
  for i,j in zip(a,b):
    res *= j-i + 1
  return res

@functools.lru_cache
def combis(min_part, max_part, position, rule_idx):
  if position == 'R':
    return 0
  if position == 'A':
    return prodsum(min_part, max_part)
  rule = rules[position].rules[rule_idx]
  if rule.target == 0:
    return combis(min_part, max_part, rule.destination, 0)
  low, high = [getattr(p, rule.c) for p in (min_part, max_part)]
  mid = rule.target
  if not low <= mid <= high:
    return 0
  res = 0
  if rule.above:
    res += combis(min_part, max_part._replace(**{rule.c: mid}), position, rule_idx + 1)
    if mid < high:
      res += combis(min_part._replace(**{rule.c: mid+1}), max_part, rule.destination, 0)
  else:
    if low < mid:
      res += combis(min_part, max_part._replace(**{rule.c: mid-1}), rule.destination, 0)
    res += combis(min_part._replace(**{rule.c: mid}), max_part, position, rule_idx + 1)
  return res

rules = {}
for line in workflow.splitlines():
  key, right = line.split('{')
  rules[key] = Rules(right)
accepted = 0
for line in parts.splitlines():
  part = create_part(line)
  position = 'in'
  while position not in 'AR':
    position = rules[position].apply(part)
  if position == 'A':
    accepted += sum(part)
print('Part 1:', accepted)
print('Part 2:', combis(Part(1,1,1,1), Part(*(4000,)*4), 'in', 0))
