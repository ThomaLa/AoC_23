WITH
  entries AS (
    SELECT
      line_idx,
      line,
      safe_cast(substr(line, -1) AS int64) AS focal,  // If NULL: deletion.
      trim(substr(line, 1, length(line) - 1), '=') AS key
    FROM
      UNNEST(split(@real, ',')) AS line WITH offset AS line_idx
  ),
  boxes AS (
    SELECT
      any_value(key) AS key,
      any_value(focal) AS focal,
      mod(sum(v), 256) AS h,
      rank() OVER (PARTITION BY any_value(key) ORDER BY line_idx) AS change_idx,
      line_idx
    FROM
      (
        SELECT
          line_idx,
          focal,
          key,
          mod(
            CAST(
              round(
                code * pow(17, length(key) - i), 0)
              AS int64),
            256) AS v
        FROM
          entries,
          UNNEST(to_code_points(key)) AS code WITH offset AS i
      )
    GROUP BY line_idx
  ),
  obfuscated AS (
    SELECT
      h,
      key,
      any_value(focal HAVING MAX(line_idx)) AS focal,  // Keep only the last value.
      array_agg(IF(focal IS NULL, -1, line_idx)) AS history,  // Store update times, to sort items within each hash bucket.
      array_last(
        split(  // Preprocessing: indices of the table above are cast into characters, except nulls which become commas so I can split by them.
          CODE_POINTS_TO_STRING(
            array_agg(
              IF(focal IS NULL, 44, 65 + change_idx))),
          ','))
        AS history_idx
    FROM boxes
    GROUP BY h, key
  ),
  renumbered AS (
    SELECT
      h,
      key,
      focal,
      rank()
        OVER (
          PARTITION BY h  // Within each hash bucket...
          ORDER BY  // ... sort by the first time at which the key was reinserted after its last deletion.
            history[ordinal(array_first(to_code_points(history_idx)) - 65)]
        ) AS slot
    FROM obfuscated
    WHERE history_idx != ''
  )
SELECT sum((h + 1) * slot * focal) AS part2 FROM renumbered;

SELECT sum(h) AS part1
FROM
  (
    SELECT line_idx, mod(sum(v), 256) AS h
    FROM
      (
        SELECT
          line_idx,
          line,
          mod(
            CAST(
              round(
                code * pow(17, COUNT(*) OVER (PARTITION BY line_idx) - i), 0)
              AS int64),
            256) AS v
        FROM
          UNNEST(split(@real, ',')) AS line WITH offset AS line_idx,
          UNNEST(to_code_points(line)) AS code WITH offset AS i
      )
    GROUP BY 1
  );
