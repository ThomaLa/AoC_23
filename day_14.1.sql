WITH
  rocks AS (
    SELECT y, x, code_points_to_string([code]) AS rock
    FROM
      UNNEST(split(@real, '\n')) AS line WITH offset AS y,
      UNNEST(to_code_points(line)) AS code WITH offset AS x
    WHERE code != 46
  ),
  rounded AS (
    SELECT x, y FROM rocks WHERE rock = 'O' ORDER BY y
  ),
  sizes AS (
    SELECT max(x) AS max_x, max(y) AS max_y FROM rounded
  ),
  square AS (
    (
      SELECT x, y FROM rocks WHERE rock = '#'
    )
    UNION ALL
    SELECT x, -1 FROM sizes, UNNEST(generate_array(0, max_x)) AS x
  ),
  look_up AS (
    SELECT
      rounded.*,
      array_last(
        array_filter(array_agg(square.y order by square.y), b -> b < rounded.y)
        )
         AS above
    FROM rounded, square
    WHERE rounded.x = square.x
    GROUP BY rounded.x, rounded.y
  )
SELECT sum(cost) as part1
FROM
  (
    SELECT
      x, y, above, 1 + max_y - above - rank() OVER (PARTITION BY x, above ORDER BY y) AS cost
    FROM sizes, look_up
  );
