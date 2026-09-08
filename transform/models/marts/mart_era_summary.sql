-- The report's Q1 table, computed in SQL instead of pandas. Every figure here is asserted
-- against the published report by tests/assert_era_summary_matches_report.sql.
with games as (select * from {{ ref('stg_games') }}),
     seasons as (select * from {{ ref('stg_seasons') }}),

game_side as (
    select
        era,
        count(*)                                                   as games,
        sum(case when is_win then 1 else 0 end)                    as wins,
        sum(case when not is_win then 1 else 0 end)                as losses,
        avg(margin)                                                as margin_per_game,
        sum(case when opponent_was_ranked and is_win then 1 else 0 end)      as wins_vs_ranked,
        sum(case when opponent_was_ranked and not is_win then 1 else 0 end)  as losses_vs_ranked,
        sum(case when opponent_was_top10 and is_win then 1 else 0 end)       as wins_vs_top10,
        sum(case when opponent_was_top10 and not is_win then 1 else 0 end)   as losses_vs_top10,
        -- the distinction the report got wrong once: postseason includes conference title
        -- games; the bowl/playoff record excludes them
        sum(case when is_postseason and is_win then 1 else 0 end)            as postseason_wins,
        sum(case when is_postseason and not is_win then 1 else 0 end)        as postseason_losses,
        sum(case when is_bowl_or_playoff and is_win then 1 else 0 end)       as bowl_wins,
        sum(case when is_bowl_or_playoff and not is_win then 1 else 0 end)   as bowl_losses,
        sum(case when is_one_score and is_win then 1 else 0 end)             as one_score_wins,
        sum(case when is_one_score and not is_win then 1 else 0 end)         as one_score_losses
    from games group by era
),
season_side as (
    select
        era,
        count(*)                                                as seasons,
        sum(conference_wins)                                    as conference_wins,
        sum(conference_losses)                                  as conference_losses,
        sum(case when won_conference_title then 1 else 0 end)   as conference_titles,
        sum(case when ap_final_rank <= 10 then 1 else 0 end)    as ap_top10_finishes,
        sum(case when wins < losses then 1 else 0 end)          as losing_seasons
    from seasons group by era
)

select
    g.era,
    s.seasons,
    g.wins, g.losses,
    round(g.wins::double / g.games, 3)                as win_pct,
    s.conference_wins, s.conference_losses,
    round(g.margin_per_game, 1)                       as margin_per_game,
    g.wins_vs_ranked, g.losses_vs_ranked,
    g.wins_vs_top10, g.losses_vs_top10,
    g.postseason_wins, g.postseason_losses,
    g.bowl_wins, g.bowl_losses,
    g.one_score_wins, g.one_score_losses,
    s.conference_titles, s.ap_top10_finishes, s.losing_seasons
from game_side g join season_side s using (era)
order by case g.era when 'Stoops' then 1 when 'Riley' then 2 else 3 end
