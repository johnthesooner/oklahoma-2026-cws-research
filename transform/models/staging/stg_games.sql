-- One row per Oklahoma football game, typed. The source CSV is read as all-varchar so that
-- dbt sees exactly the bytes the Python validators see; casting happens here, once.
with source as (select * from {{ source('football', 'games_football') }})

select
    cast(season as integer)                          as season,
    cast(date as date)                               as game_date,
    opponent,
    try_cast(opp_rank as integer)                    as opponent_ap_rank,
    try_cast(ou_rank  as integer)                    as oklahoma_ap_rank,
    site,
    result,
    cast(ou_pts  as integer)                         as points_for,
    cast(opp_pts as integer)                         as points_against,
    cast(margin  as integer)                         as margin,
    one_score = 'Y'                                  as is_one_score,
    conf_game = 'Y'                                  as is_conference_game,
    game_type,
    overtime = 'Y'                                   as went_overtime,
    era,
    conference,
    -- derived once, here, rather than in five different analysis scripts
    opp_rank is not null and opp_rank <> ''          as opponent_was_ranked,
    try_cast(opp_rank as integer) <= 10              as opponent_was_top10,
    game_type <> 'REG'                               as is_postseason,
    game_type in ('BOWL', 'BCS_TITLE', 'CFP_SEMI', 'CFP_R1') as is_bowl_or_playoff,
    result = 'W'                                     as is_win,
    confidence,
    source
from source
