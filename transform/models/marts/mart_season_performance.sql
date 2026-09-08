-- One row per season joining record, ratings, EPA and lagged recruiting. This is the table a
-- reader should be able to drill into from any figure in the report.
with s as (select * from {{ ref('stg_seasons') }}),
     r as (select * from {{ ref('stg_ratings') }}),
     e as (select * from {{ ref('stg_epa') }}),
     rec as (select * from {{ ref('stg_recruiting') }})

select
    s.season, s.era, s.coach, s.conference,
    s.wins, s.losses, s.win_pct, s.margin_per_game,
    s.conference_wins, s.conference_losses, s.won_conference_title, s.ap_final_rank,
    r.sp_plus_rank, r.sp_plus_offense_rank, r.sp_plus_defense_rank,
    r.fpi, r.fpi_rank, r.strength_of_schedule_rank,
    e.offense_epa_per_play, e.offense_epa_rank,
    e.defense_epa_per_play_allowed, e.defense_epa_rank,
    rec3.composite_247_rank as recruiting_rank_lag3,
    -- Pythagorean expectation, exponent 2.37, matching football_lib.PYTHAG_EXP
    round(s.games * pow(s.points_for, 2.37)
          / (pow(s.points_for, 2.37) + pow(s.points_against, 2.37)), 2) as pythagorean_wins,
    round(s.wins - s.games * pow(s.points_for, 2.37)
          / (pow(s.points_for, 2.37) + pow(s.points_against, 2.37)), 2) as luck_wins
from s
left join r   on r.season = s.season
left join e   on e.season = s.season
left join rec as rec3 on rec3.class_year = s.season - 3
order by s.season
