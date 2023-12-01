DEFINE MACRO digits array_filter(to_code_points(line), c -> c BETWEEN 48 AND 57);
DEFINE MACRO get_first [offset(0)] - 48 AS $1;
DEFINE MACRO reduce
  replace(replace(replace(replace(replace(replace(replace(replace(replace(replace($1,
  'zero', '0o'), 'one', 'o1e'), 'two', 't2o'), 'three', 't3e'), 'four', '4'), 'five', '5'), 'six', '6'), 'seven', '7n'), 'eight', 'e8t'), 'nine', 'n9e');
DEFINE MACRO calibrate (
  WITH lines AS (
    SELECT
      $digits(line)$get_first(l),
      array_reverse($digits(line))$get_first(r)
    FROM UNNEST(split($2, '\n')) AS line )
  SELECT $1 AS part, 10 * sum(l) + sum(r) AS result FROM lines );

SELECT * FROM $calibrate(1, $input()) UNION ALL $calibrate(2, $reduce($input()));
