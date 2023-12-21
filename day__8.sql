-- I really tried, but limited to a stack depth of 100 couldn't pass the real input.
-- Attempt for part 1:
WITH RECURSIVE
  raw_input AS (SELECT split(@real, '\n\n') AS parts),
  map AS (
    SELECT
      parts[offset(0)] AS instructions,
      split(nodes, ' =')[offset(0)] AS origin,
      regexp_extract(nodes, r'\((.*),') AS L,
      regexp_extract(nodes, r', (.*)\)') AS R
    FROM raw_input, UNNEST(split(parts[offset(1)], '\n')) AS nodes
  ),
  just_instructions AS (
    SELECT TO_CODE_POINTS(instructions) AS instructions_array FROM map LIMIT 1
  ),
  move_around AS (
    (SELECT 0 AS step, 'AAA' AS position)
    UNION ALL
    SELECT
      step + 1,
      IF(instructions_array[offset(MOD(step, array_length(just_instructions.instructions_array)))] = 82,
         R, L)
    FROM just_instructions, move_around
    INNER JOIN map
      ON position = origin
    WHERE origin != R OR origin != L
  )
SELECT * FROM move_around;
