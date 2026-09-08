-- margin and the one-score flag are derived from the score and must never drift from it.
select season, game_date, opponent, margin, points_for, points_against, is_one_score
from {{ ref('stg_games') }}
where margin <> points_for - points_against
   or is_one_score <> (abs(margin) <= 8)
   or is_win <> (points_for > points_against)
