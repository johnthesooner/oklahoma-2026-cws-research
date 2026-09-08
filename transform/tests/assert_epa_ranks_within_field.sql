-- A rank must lie inside the field it was computed over.
select season, offense_epa_rank, defense_epa_rank, teams_ranked
from {{ ref('stg_epa') }}
where offense_epa_rank not between 1 and teams_ranked
   or defense_epa_rank not between 1 and teams_ranked
   or offense_success_rate not between 0 and 1
   or defense_success_rate_allowed not between 0 and 1
