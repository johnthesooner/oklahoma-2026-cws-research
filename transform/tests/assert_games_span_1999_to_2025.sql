-- 2026 is in progress and lives only in the tracker; it must never leak into the game log.
select min(season) as first_season, max(season) as last_season, count(*) as games
from {{ ref('stg_games') }}
having min(season) <> 1999 or max(season) <> 2025 or count(*) <> 356
