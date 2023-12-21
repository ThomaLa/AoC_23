CREATE TEMP FUNCTION count_diffs(a string, b string) AS (
  array_length(array_filter(generate_array(1, length(a)),
                            i -> substr(a, i, 1) != substr(b, i, 1)))
);


WITH
  puzzles AS (
    SELECT
      puzzle_idx,
      any_value(puzzle) AS puzzle,
      COUNT(line) AS puzzle_height,
      any_value(length(line)) AS puzzle_width,
    FROM
      UNNEST(split(@real, '\n\n')) AS puzzle WITH offset AS puzzle_idx,
      UNNEST(split(puzzle, '\n')) AS line
    GROUP BY 1
  ), lines AS (
    (
      SELECT puzzle_idx, line, line_idx, puzzle_height, 100 AS value
      FROM puzzles, UNNEST(split(puzzle, '\n')) AS line WITH offset AS line_idx
    )
    UNION ALL
    SELECT
      puzzle_idx,
      string_agg(substr(line, i, 1), '' ORDER BY real_line_idx),
      i - 1, any_value(puzzle_width), 1
    FROM
      puzzles,
      UNNEST(split(puzzle, '\n')) AS line WITH offset AS real_line_idx,
      UNNEST(generate_array(1, puzzle_width)) AS i
    GROUP BY puzzle_idx, i
  ), mirrors AS (
    SELECT
      puzzle_idx,
      value,
      line AS compared,
      mirror_location,
      2 * mirror_location - 1 - line_idx AS line_idx
    FROM
      lines,
      UNNEST(generate_array(1, puzzle_height - 1)) AS mirror_location
    WHERE
      2 * mirror_location - 1 - line_idx BETWEEN 0 AND puzzle_height - 1
      AND line_idx < mirror_location
  ), found AS (
    SELECT
      value,
      mirror_location,
      sum(count_diffs(line, compared)) AS total_diffs,
    FROM mirrors
    LEFT JOIN lines
      USING (puzzle_idx, value, line_idx)
    GROUP BY 1, 2, puzzle_idx
  )
SELECT
  sum(IF(total_diffs = 0, value * mirror_location, 0)) AS part1,
  sum(IF(total_diffs = 1, value * mirror_location, 0)) AS part2
FROM found;
