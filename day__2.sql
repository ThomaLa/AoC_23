DEFINE MACRO count_color
  max(CAST(regexp_extract(visible, r'(\d+) $1') AS int32)) AS $1;

WITH
  games AS (
    SELECT split(line, ': ') AS game
    FROM UNNEST(split(@input, '\n')) AS line
  ),
  parsed AS (
    SELECT
      CAST(regexp_extract(game[offset(0)], r'(\d+)') AS int32) AS id,
      $count_color(blue),
      $count_color(red),
      $count_color(green)
    FROM games, UNNEST(split(game[offset(1)], '; ')) AS visible
    GROUP BY 1
  )
SELECT
  sum(IF(blue <= 14 AND red <= 12 AND green <= 13, id, 0)) AS part1,
  sum(blue * red * green) AS part2
FROM parsed
