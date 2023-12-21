-- Part 1
WITH
  tokens AS (
    SELECT line_idx, CAST(param AS int64) AS param, race_idx
    FROM
      UNNEST(split(@real, '\n')) AS line WITH offset AS line_idx,
      UNNEST(
        array_filter(split(line, ' '), e -> safe_cast(e AS int64) IS NOT NULL))
        AS param
      WITH offset AS race_idx
  ),
  outcomes AS (
    SELECT
      race_idx, time, distance, strategy, (time - strategy) * strategy AS result
    FROM
      (
        SELECT
          race_idx, param AS time, generate_array(1, param - 1) AS strategies
        FROM tokens
        WHERE line_idx = 0
      )
    INNER JOIN
      (SELECT race_idx, param AS distance FROM tokens WHERE line_idx = 1)
      USING (race_idx), UNNEST(strategies) AS strategy
  ),
  by_race AS (
    SELECT race_idx, COUNT(*) AS ways
    FROM outcomes
    WHERE result > distance
    GROUP BY 1
  )
SELECT round(exp(sum(log(ways))), 0) FROM by_race;

-- Part 2
-- (time - x) * x = distance
-- x^2 - time * x + distance = 0
-- a = 1, b = -time, c = distance
-- (-b ± SQRT(b^2 - 4c))/2

WITH
  tokens AS (
    SELECT line_idx, CAST(split(replace(line, ' ', ''), ':')[offset(1)] AS int64) AS param, 1 as race_idx
    FROM
      UNNEST(split(@real, '\n')) AS line WITH offset AS line_idx
  )
  SELECT
      time, distance, floor((time + sqrt(time*time - 4*distance)) / 2) - ceil((time - sqrt(time*time - 4*distance)) / 2) + 1 as res
    FROM
      (
        SELECT
          race_idx, param AS time
        FROM tokens
        WHERE line_idx = 0
      )
    INNER JOIN
      (SELECT race_idx, param AS distance FROM tokens WHERE line_idx = 1)
      USING (race_idx)
