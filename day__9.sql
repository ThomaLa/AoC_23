WITH RECURSIVE
  parsed AS (
    SELECT
      line_idx,
      0 AS depth,
      array_transform(split(line, ' '), e -> CAST(e AS int64)) AS history
    FROM UNNEST(split(@day21, '\n')) AS line WITH offset AS line_idx
  ),
  triangles AS (
    (SELECT * FROM parsed)
    UNION ALL
    SELECT
      line_idx,
      depth + 1,
      array_transform(
        generate_array(1, array_length(history) - 1),
        i -> history[offset(i)] - history[ordinal(i)])
    FROM triangles
    WHERE array_length(history) > 1
  ),
  sides AS (
    SELECT
      line_idx,
      array_agg(array_first(history) ORDER BY depth DESC) AS first_elements,
      array_agg(array_last(history) ORDER BY depth DESC) AS last_elements
    FROM triangles
    GROUP BY line_idx
  ),
  placeholders AS (
    (
      SELECT
        0 AS index, first_elements, last_elements, 0 AS result1, 0 AS result2
      FROM sides
    )
    UNION ALL
    SELECT
      index + 1,
      first_elements,
      last_elements,
      result1 + last_elements[offset(index)],
      first_elements[offset(index)] - result2
    FROM placeholders
    WHERE array_length(last_elements) > index
  )
SELECT sum(result1) AS part1, sum(result2) AS part2
FROM placeholders
WHERE array_length(last_elements) = index;
