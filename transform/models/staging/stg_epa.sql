-- Play-level EPA, 2021-2025. NOT opponent-adjusted: a team playing a hard schedule ranks
-- lower here than in SP+, which is itself the measurement of interest in mart_unit_swap.
with source as (select * from {{ source('football', 'epa_football') }})

select
    cast(season as integer)                as season,
    cast(off_plays as integer)             as offense_plays,
    cast(off_epa_play as double)           as offense_epa_per_play,
    cast(off_epa_rank as integer)          as offense_epa_rank,
    cast(off_success as double)            as offense_success_rate,
    cast(def_plays as integer)             as defense_plays,
    cast(def_epa_play as double)           as defense_epa_per_play_allowed,
    cast(def_epa_rank as integer)          as defense_epa_rank,
    cast(def_success as double)            as defense_success_rate_allowed,
    cast(n_teams as integer)               as teams_ranked,
    cast(off_epa_rank_cg as integer)       as offense_epa_rank_no_garbage,
    cast(def_epa_rank_cg as integer)       as defense_epa_rank_no_garbage
from source
