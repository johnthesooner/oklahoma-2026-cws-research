with source as (select * from {{ source('football', 'seasons_football') }})

select
    cast(season as integer)        as season,
    era,
    coach,
    conference,
    cast(G as integer)             as games,
    cast(W as integer)             as wins,
    cast(L as integer)             as losses,
    cast(win_pct as double)        as win_pct,
    cast(conf_W as integer)        as conference_wins,
    cast(conf_L as integer)        as conference_losses,
    conf_finish                    as conference_finish,
    conf_title = 'Y'               as won_conference_title,
    cast(PF as integer)            as points_for,
    cast(PA as integer)            as points_against,
    cast(margin_pg as double)      as margin_per_game,
    postseason                     as postseason_result,
    try_cast(ap_final as integer)  as ap_final_rank,
    try_cast(coaches_final as integer) as coaches_final_rank
from source
