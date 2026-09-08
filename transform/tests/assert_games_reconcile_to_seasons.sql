-- The module's central integrity check, ported from validate_football.py: every season's
-- record, points and conference record computed from the game log must equal the seasons table.
with from_games as (
    select season,
           sum(case when is_win then 1 else 0 end) as wins,
           sum(case when not is_win then 1 else 0 end) as losses,
           sum(points_for) as points_for,
           sum(points_against) as points_against,
           sum(case when is_conference_game and is_win then 1 else 0 end) as conference_wins,
           sum(case when is_conference_game and not is_win then 1 else 0 end) as conference_losses
    from {{ ref('stg_games') }} group by season
)
select s.season, g.wins, s.wins as seasons_wins, g.points_for, s.points_for as seasons_points_for
from {{ ref('stg_seasons') }} s join from_games g using (season)
where g.wins <> s.wins or g.losses <> s.losses
   or g.points_for <> s.points_for or g.points_against <> s.points_against
   or g.conference_wins <> s.conference_wins or g.conference_losses <> s.conference_losses
