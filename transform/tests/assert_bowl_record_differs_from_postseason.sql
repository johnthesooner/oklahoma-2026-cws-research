-- The defect this test exists to prevent: "postseason" once silently included conference
-- championship games, publishing Stoops at 16-10 and Riley at 6-3 when their bowl-and-playoff
-- records are 9-9 and 2-3. The two measures must stay distinct and must keep these values.
select era, bowl_wins, bowl_losses, postseason_wins, postseason_losses
from {{ ref('mart_era_summary') }}
where (era = 'Stoops'   and (bowl_wins, bowl_losses, postseason_wins, postseason_losses) <> (9, 9, 16, 10))
   or (era = 'Riley'    and (bowl_wins, bowl_losses, postseason_wins, postseason_losses) <> (2, 3, 6, 3))
   or (era = 'Venables' and (bowl_wins, bowl_losses, postseason_wins, postseason_losses) <> (0, 4, 0, 4))
