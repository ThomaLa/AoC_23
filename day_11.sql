WITH
  stars AS (
    SELECT x, y,
    FROM
      UNNEST(split(@real, '\n')) AS line WITH offset AS y,
      UNNEST(to_code_points(line)) AS c WITH offset AS x
    WHERE c = to_code_points('#')[offset(0)]
  ),
  sizes AS (SELECT max(x) AS max_x, max(y) AS max_y FROM stars),
  expansions AS (
    (
      SELECT x AS expansion_x, NULL AS expansion_y
      FROM
        sizes,
        UNNEST(generate_array(0, max_x)) AS x
      WHERE x NOT IN (SELECT DISTINCT x FROM stars)
    )
    UNION ALL
    SELECT NULL, y
    FROM sizes, UNNEST(generate_array(0, max_y)) AS y
    WHERE y NOT IN (SELECT DISTINCT y FROM stars)
  ),
  distances AS (
    SELECT
      start_x,
      start_y,
      end_x,
      end_y,
      abs(start_x - end_x) + abs(start_y - end_y) AS distance,
      countif(
        expansion_x BETWEEN start_x AND end_x
        OR expansion_y BETWEEN start_y AND end_y
        OR expansion_y BETWEEN end_y AND start_y) AS num_expansions
    FROM
      (SELECT x AS start_x, y AS start_y FROM stars),
      (SELECT x AS end_x, y AS end_y FROM stars),
      expansions
    WHERE
      (start_x != end_x OR start_y != end_y)
      AND (start_x < end_x OR (start_x = end_x AND start_y < end_y))
    GROUP BY 1, 2, 3, 4
  )
SELECT
  sum(distance + num_expansions) AS part1,
  sum(distance + 999999 * num_expansions) AS part2
FROM distances;
