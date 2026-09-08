-- The report's second headline, expressed as data: three independent rating systems and
-- whether each says the offense or the defense was the better unit that season.
with p as (select * from {{ ref('mart_season_performance') }})

select
    season, era, coach,
    sp_plus_offense_rank, sp_plus_defense_rank,
    sp_plus_defense_rank - sp_plus_offense_rank      as sp_plus_offense_edge,
    offense_epa_rank, defense_epa_rank,
    defense_epa_rank - offense_epa_rank              as epa_offense_edge,
    case
        when sp_plus_offense_rank is null then null
        when sp_plus_defense_rank - sp_plus_offense_rank > 20 then 'offense-led'
        when sp_plus_offense_rank - sp_plus_defense_rank > 20 then 'defense-led'
        else 'balanced'
    end                                              as sp_plus_profile,
    case
        when offense_epa_rank is null then null
        when defense_epa_rank - offense_epa_rank > 20 then 'offense-led'
        when offense_epa_rank - defense_epa_rank > 20 then 'defense-led'
        else 'balanced'
    end                                              as epa_profile
from p
where sp_plus_offense_rank is not null or offense_epa_rank is not null
order by season
