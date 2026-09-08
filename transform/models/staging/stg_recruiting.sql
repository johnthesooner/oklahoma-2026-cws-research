with source as (select * from {{ source('football', 'recruiting_football') }})

select
    cast(class_year as integer)               as class_year,
    try_cast(rank_247_composite as integer)   as composite_247_rank,
    try_cast(rank_rivals as integer)          as rivals_rank,
    try_cast(rank_espn as integer)            as espn_rank,
    try_cast(rank_scout as integer)           as scout_rank,
    confidence
from source
