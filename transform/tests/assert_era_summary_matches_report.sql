-- The headline figures as published in football/report/OKLAHOMA_FOOTBALL_ERAS_REPORT.md.
-- If an upstream change moves any of them, this fails and the report is stale.
select era, wins, losses, conference_titles, ap_top10_finishes, losing_seasons
from {{ ref('mart_era_summary') }}
where (era = 'Stoops'   and (wins, losses, conference_titles, ap_top10_finishes, losing_seasons) <> (190, 48, 10, 11, 0))
   or (era = 'Riley'    and (wins, losses, conference_titles, ap_top10_finishes, losing_seasons) <> (56,  10, 4,  5,  0))
   or (era = 'Venables' and (wins, losses, conference_titles, ap_top10_finishes, losing_seasons) <> (32,  20, 0,  0,  2))
