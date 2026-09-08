with source as (select * from {{ source('football', 'ratings_football') }})

select
    cast(season as integer)            as season,
    try_cast(fpi as double)            as fpi,
    try_cast(fpi_rank as integer)      as fpi_rank,
    try_cast(sos_rank as integer)      as strength_of_schedule_rank,
    try_cast(sor_rank as integer)      as strength_of_record_rank,
    try_cast(sp_rating as double)      as sp_plus_rating,
    try_cast(sp_rank as integer)       as sp_plus_rank,
    try_cast(sp_off as double)         as sp_plus_offense,
    try_cast(sp_off_rank as integer)   as sp_plus_offense_rank,
    try_cast(sp_def as double)         as sp_plus_defense,
    try_cast(sp_def_rank as integer)   as sp_plus_defense_rank,
    try_cast(eff_off_rank as integer)  as espn_offense_efficiency_rank,
    try_cast(eff_def_rank as integer)  as espn_defense_efficiency_rank,
    confidence
from source
