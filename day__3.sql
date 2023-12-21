WITH parsed AS (
    SELECT *, IF(char = 46, -1, IF(char BETWEEN 48 AND 57, char - 48, NULL)) AS readable_char
    FROM UNNEST(split(@input, '\n')) AS line WITH offset AS line_idx,
         UNNEST(to_code_points(line)) AS char WITH offset AS char_idx
  ), partial_numbers AS (
    SELECT units.readable_char
           + IF(tens.readable_char >= 0, 10 * tens.readable_char, 0)
           + IF(tens.readable_char >= 0 and hundreds.readable_char >= 0, 100 * hundreds.readable_char, 0)
           AS full_number,
      units.line_idx, units.char_idx,
      if(hundreds.readable_char >= 0, hundreds.char_idx,
         if(tens.readable_char >= 0, tens.char_idx,
            units.char_idx)) AS left_char_idx
    FROM parsed AS units
    LEFT JOIN parsed AS tens ON units.line_idx = tens.line_idx AND units.char_idx - 1 = tens.char_idx
    LEFT JOIN parsed AS hundreds ON hundreds.line_idx = tens.line_idx AND hundreds.char_idx + 1 = tens.char_idx
    WHERE units.readable_char >= 0
  ), full_numbers AS (
    select *
    FROM partial_numbers
    WHERE full_number > 0 and
      char_idx NOT IN (
        SELECT ci - 1
        FROM (SELECT line_idx AS li, char_idx AS ci FROM partial_numbers
        where full_number > 0)
        WHERE li = line_idx
      )
  ), seeds AS (
    SELECT
      char,
      line_idx + line_offset AS line_to_keep,
      char_idx + char_offset AS char_to_keep,
      line_idx as original_line_idx, char_idx as original_char_idx
    FROM
      parsed,
      UNNEST(generate_array(-1, 1)) AS line_offset,
      UNNEST(generate_array(-1, 1)) AS char_offset
    WHERE readable_char IS NULL AND (char_offset != 0 OR line_offset != 0)
  ), matches as (
    SELECT
      any_value(full_number) as good,
      any_value(char) as char,
      any_value(original_line_idx) as original_line_idx,
      any_value(original_char_idx) as original_char_idx
    FROM full_numbers right join seeds
    on line_to_keep = line_idx AND char_to_keep between left_char_idx and char_idx
    where full_number is not null
    group by line_idx, char_idx
  ), ops as (
    select array_agg(good) as operands, code_points_to_string([any_value(char)]) as symbol
    from matches
    group by original_line_idx, original_char_idx
  )
select 1 as part, sum(good) as result from matches
union all
select 2 as part, sum(if(symbol = '*' and array_length(operands) = 2, operands[ordinal(1)]*operands[ordinal(2)], 0)) as result from ops;


-- Part 1 if only digits not numbers
-- WITH
--   parsed AS (
--     SELECT
--       *,
--       IF(char = 46, 0, IF(char BETWEEN 48 AND 57, char - 48, NULL))
--         AS readable_char
--     FROM
--       UNNEST(split(@smol, '\n')) AS line WITH offset AS line_idx,
--       UNNEST(to_code_points(line)) AS char WITH offset AS char_idx
--   ),
--   relevant AS (
--     SELECT
--       line_idx + line_offset AS line_to_keep,
--       char_idx + char_offset AS char_to_keep
--     FROM
--       parsed,
--       UNNEST(generate_array(-1, 1)) AS line_offset,
--       UNNEST(generate_array(-1, 1)) AS char_offset
--     WHERE readable_char IS NULL AND (char_offset != 0 OR line_offset != 0)
--   )
-- SELECT sum(readable_char)
-- FROM relevant
-- LEFT JOIN parsed
--   ON line_to_keep = line_idx AND char_to_keep = char_idx;
