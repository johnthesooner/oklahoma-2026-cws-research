-- Oklahoma won exactly 14 conference titles in this window, independently sourced from the
-- Big 12 champions list. 2003 must NOT appear: OU won the division but lost the title game 7-35.
with titles as (
    select season from {{ ref('stg_seasons') }} where won_conference_title
)
select 'wrong title set' as failure, list(season order by season) as seasons
from titles
having list(season order by season)
    <> [2000, 2002, 2004, 2006, 2007, 2008, 2010, 2012, 2015, 2016, 2017, 2018, 2019, 2020]
