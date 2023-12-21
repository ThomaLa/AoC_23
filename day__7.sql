CREATE TEMPORARY FUNCTION cp(c STRING) AS (to_code_points(c)[offset(0)]);
CREATE TEMPORARY FUNCTION to_value(cards STRING, index INT32, which_part int32)
AS (
  ARRAY_TRANSFORM(to_code_points(cards),
                  e -> CASE
                    WHEN e = cp('T') THEN 10
                    WHEN e = cp('J') AND which_part = 1 THEN 11
                    WHEN e = cp('J') AND which_part = 2 THEN 0
                    WHEN e = cp('Q') THEN 12
                    WHEN e = cp('K') THEN 13
                    WHEN e = cp('A') THEN 14
                    ELSE e - 48
                    END)[ordinal(index)]
);

DEFINE MACRO values hand_value_$1 * 0x100000
         + to_value(cards, 1, $1) * 0x10000
         + to_value(cards, 2, $1) * 0x1000
         + to_value(cards, 3, $1) * 0x100
         + to_value(cards, 4, $1) * 0x10  // Values never exceed 15...
         + to_value(cards, 5, $1) AS value_$1;
DEFINE MACRO rank rank() OVER (PARTITION BY TRUE ORDER BY value_$1) AS rank_$1;
DEFINE MACRO sum_bids sum(bid * rank_$1) AS part_$1;

WITH
  hands AS (
    SELECT
      hand_idx, split(hand, ' ') AS hand
    FROM UNNEST(split(@real, '\n')) AS hand WITH offset AS hand_idx
  ), counts AS (
    SELECT
      hand_idx,
      CAST(hand[offset(1)] AS int64) AS bid,
      hand[offset(0)] AS cards,
      card,
      COUNT(card) OVER (PARTITION BY hand_idx, card) AS card_count,
    FROM hands, UNNEST(to_code_points(hand[offset(0)])) AS card
  ), hand_values AS (
    SELECT
      hand_idx,
      any_value(bid) AS bid,
      any_value(cards) AS cards,
      // Sum orders most hands correctly, and max breaks the 3-of-a-kind/double-pair tie.
      // With tuple comparison I'd simply compare the ordered counts. Oh well...
      sum(card_count) + max(card_count) AS hand_value_1,
      // As before, we want to do "sum + max" over the counts
      // For the sum: take the sum of the non-joker cards ...
      sum(IF(card = cp('J'), 0, card_count))
        // ... then add the jokers to the highest count. This means bringing H² up to (H+J)²: add J·(J + 2·H).
        + countif(card = cp('J')) * (countif(card = cp('J')) + 2 * max(IF(card = cp('J'), 0, card_count)))
        // Now the max: It's simply J + H
        + max(IF(card = cp('J'), card_count, 0))
        + max(IF(card = cp('J'), 0, card_count)) AS hand_value_2
    FROM counts
    GROUP BY hand_idx
  ), measured AS ( SELECT bid, cards, $values(1), $values(2) FROM hand_values
  ), ranked AS ( SELECT *, $rank(1), $rank(2) FROM measured
  )
SELECT $sum_bids(1), $sum_bids(2) FROM ranked;
