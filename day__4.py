import re

real = ''  # Yes I did this in a notebook. Don't judge.

print('Part 1:', int(sum(
    2**(len(set(winning.split()) & set(actual.split())) - 1)
    for index, winning, actual
    in re.compile(r'Card (.*): (.*) \| (.*)\n').findall(real)
    )))

won = 0
next_cards = [0]
for index, winning, actual in re.compile(r'Card (.*): (.*) \| (.*)\n').findall(real):
  this_card = (next_cards or [0]).pop(0) + 1  # cards earned + initial card
  for i in range(len(set(winning.split()) & set(actual.split()))):
    if i < len(next_cards):
      next_cards[i] += this_card
    else:
      next_cards.append(this_card)
  won += this_card
print('Part 2:', won)
