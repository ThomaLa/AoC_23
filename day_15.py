real = ''

hash = lambda word: sum(ord(c) * 17 ** (len(word) - i)
                        for (i, c) in enumerate(word)) % 256
print('Part 1:', sum(hash(word) for word in real.split(',')))

boxes = [[] for _ in range(256)]
for word in real.split(','):
  if word[-1] == '-':
    h = hash(word[:-1])
    for i, (lens, _) in enumerate(boxes[h]):
      if lens == word[:-1]:
        del boxes[h][i]
        break
  else:
    h = hash(word[:-2])
    for i, (lens, _) in enumerate(boxes[h]):
      if lens == word[:-2]:
        boxes[h][i] = lens, int(word[-1])
        break
    else:
      boxes[h].append((word[:-2], int(word[-1])))
print('Part 2:', sum(sum((box_idx + 1) * (slot_idx + 1) * f
                         for slot_idx, (_, f) in enumerate(box))
                     for box_idx, box in enumerate(boxes)))