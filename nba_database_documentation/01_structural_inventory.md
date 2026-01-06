# NBA Database - Structural Inventory

*Generated: 2026-01-05 16:57:59*

## Summary

- **Total Tables**: 70
- **Total Views**: 5
- **Total Rows**: 2,475,759
- **Total Constraints**: 73
- **Total Indexes**: 19
- **Custom Functions**: 0

## Tables by Layer

### RAW Layer (12 tables)

- **common_player_info_raw** (BASE TABLE): 27 columns, 0 rows
- **draft_combine_stats_raw** (BASE TABLE): 19 columns, 0 rows
- **draft_history_raw** (BASE TABLE): 13 columns, 0 rows
- **franchise_history_raw** (BASE TABLE): 16 columns, 74 rows
- **franchise_leaders_raw** (BASE TABLE): 14 columns, 150 rows
- **game_raw** (BASE TABLE): 26 columns, 0 rows
- **player_game_stats_raw** (BASE TABLE): 26 columns, 0 rows
- **player_raw** (BASE TABLE): 5 columns, 0 rows
- **player_splits_raw** (BASE TABLE): 35 columns, 6 rows
- **team_details_raw** (BASE TABLE): 14 columns, 0 rows
- **team_info_common_raw** (BASE TABLE): 27 columns, 0 rows
- **team_raw** (BASE TABLE): 7 columns, 0 rows

### SILVER Layer (26 tables)

- **br_player_box_scores_silver** (BASE TABLE): 28 columns, 0 rows
- **br_player_season_advanced_silver** (BASE TABLE): 28 columns, 8,912 rows
- **br_player_season_totals_silver** (BASE TABLE): 33 columns, 9,178 rows
- **common_player_info_silver** (BASE TABLE): 34 columns, 4,171 rows
- **draft_combine_stats_silver** (BASE TABLE): 48 columns, 1,202 rows
- **draft_history_silver** (BASE TABLE): 15 columns, 8,374 rows
- **game_gold_silver** (BASE TABLE): 56 columns, 70,228 rows
- **game_info_silver** (BASE TABLE): 5 columns, 58,053 rows
- **game_silver** (BASE TABLE): 56 columns, 65,642 rows
- **game_summary_silver** (BASE TABLE): 15 columns, 58,110 rows
- **games_silver** (BASE TABLE): 10 columns, 70,228 rows
- **inactive_players_silver** (BASE TABLE): 10 columns, 110,191 rows
- **line_score_silver** (BASE TABLE): 44 columns, 58,053 rows
- **officials_silver** (BASE TABLE): 6 columns, 70,971 rows
- **other_stats_silver** (BASE TABLE): 27 columns, 28,271 rows
- **play_by_play_silver** (BASE TABLE): 24 columns, 492 rows
- **player_game_stats_silver** (BASE TABLE): 26 columns, 769,033 rows
- **player_gold_silver** (BASE TABLE): 5 columns, 5,104 rows
- **player_season_stats_silver** (BASE TABLE): 29 columns, 19,231 rows
- **player_silver** (BASE TABLE): 5 columns, 0 rows
- **team_details_silver** (BASE TABLE): 15 columns, 25 rows
- **team_game_stats_silver** (BASE TABLE): 24 columns, 140,456 rows
- **team_gold_silver** (BASE TABLE): 7 columns, 82 rows
- **team_history_silver** (BASE TABLE): 6 columns, 52 rows
- **team_info_common_silver** (BASE TABLE): 27 columns, 0 rows
- **team_silver** (BASE TABLE): 7 columns, 0 rows

### GOLD Layer (3 tables)

- **game_gold** (BASE TABLE): 9 columns, 0 rows
- **player_gold** (BASE TABLE): 5 columns, 5,104 rows
- **team_gold** (BASE TABLE): 7 columns, 82 rows

### BASE Layer (34 tables)

- **all_star_selections** (BASE TABLE): 6 columns, 2,004 rows
- **award_voting_shares** (BASE TABLE): 10 columns, 3,397 rows
- **br_player_box_scores** (BASE TABLE): 28 columns, 0 rows
- **br_player_season_advanced** (BASE TABLE): 28 columns, 33,161 rows
- **br_player_season_totals** (BASE TABLE): 33 columns, 33,163 rows
- **br_schedule** (BASE TABLE): 15 columns, 1,321 rows
- **common_player_info** (BASE TABLE): 34 columns, 4,171 rows
- **draft_combine_stats** (BASE TABLE): 48 columns, 1,202 rows
- **draft_history** (BASE TABLE): 15 columns, 8,374 rows
- **game** (BASE TABLE): 56 columns, 65,698 rows
- **game_info** (BASE TABLE): 5 columns, 58,053 rows
- **game_summary** (BASE TABLE): 15 columns, 58,110 rows
- **games** (BASE TABLE): 10 columns, 70,228 rows
- **inactive_players** (BASE TABLE): 10 columns, 110,191 rows
- **line_score** (BASE TABLE): 44 columns, 58,053 rows
- **officials** (BASE TABLE): 6 columns, 70,971 rows
- **other_stats** (BASE TABLE): 27 columns, 28,271 rows
- **play_by_play** (BASE TABLE): 24 columns, 0 rows
- **player** (BASE TABLE): 6 columns, 5,116 rows
- **player_game_stats** (BASE TABLE): 26 columns, 0 rows
- **player_season_averages** (BASE TABLE): 14 columns, 18,745 rows
- **player_season_stats** (BASE TABLE): 29 columns, 0 rows
- **team** (BASE TABLE): 8 columns, 30 rows
- **team_details** (BASE TABLE): 15 columns, 25 rows
- **team_game_stats** (BASE TABLE): 24 columns, 140,456 rows
- **team_history** (BASE TABLE): 6 columns, 52 rows
- **team_info_common** (BASE TABLE): 27 columns, 0 rows
- **team_rolling_metrics** (BASE TABLE): 10 columns, 140,456 rows
- **team_standings** (BASE TABLE): 7 columns, 3,036 rows
- **league_season_averages** (VIEW): 16 columns
- **player_career_summary** (VIEW): 13 columns
- **player_game_advanced** (VIEW): 29 columns
- **team_four_factors** (VIEW): 12 columns
- **team_game_advanced** (VIEW): 27 columns

## Detailed Table Schemas

### all_star_selections

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| player_name | VARCHAR | YES | - |
| br_player_id | VARCHAR | NO | - |
| team | VARCHAR | YES | - |
| season_end_year | INTEGER | NO | - |
| league | VARCHAR | YES | - |
| replaced | BOOLEAN | YES | - |

**Constraints:**
- PRIMARY KEY: PRIMARY KEY(br_player_id, season_end_year)
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL

### award_voting_shares

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| season_end_year | INTEGER | NO | - |
| award | VARCHAR | NO | - |
| player_name | VARCHAR | YES | - |
| br_player_id | VARCHAR | NO | - |
| age | DOUBLE | YES | - |
| first_place_votes | DOUBLE | YES | - |
| pts_won | DOUBLE | YES | - |
| pts_max | DOUBLE | YES | - |
| share | DOUBLE | YES | - |
| winner | BOOLEAN | YES | - |

**Constraints:**
- PRIMARY KEY: PRIMARY KEY(br_player_id, season_end_year, award)
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL

### br_player_box_scores

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | VARCHAR | NO | - |
| game_date | DATE | YES | - |
| player_name | VARCHAR | NO | - |
| team_abbreviation | VARCHAR | YES | - |
| opponent | VARCHAR | YES | - |
| location | VARCHAR | YES | - |
| wl | VARCHAR | YES | - |
| min | VARCHAR | YES | - |
| fgm | INTEGER | YES | - |
| fga | INTEGER | YES | - |
| fg_pct | DOUBLE | YES | - |
| fg3m | INTEGER | YES | - |
| fg3a | INTEGER | YES | - |
| fg3_pct | DOUBLE | YES | - |
| ftm | INTEGER | YES | - |
| fta | INTEGER | YES | - |
| ft_pct | DOUBLE | YES | - |
| oreb | INTEGER | YES | - |
| dreb | INTEGER | YES | - |
| reb | INTEGER | YES | - |
| ast | INTEGER | YES | - |
| stl | INTEGER | YES | - |
| blk | INTEGER | YES | - |
| tov | INTEGER | YES | - |
| pf | INTEGER | YES | - |
| pts | INTEGER | YES | - |
| plus_minus | INTEGER | YES | - |
| game_score | DOUBLE | YES | - |

**Constraints:**
- PRIMARY KEY: PRIMARY KEY(game_id, player_name)
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL

### br_player_box_scores_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | VARCHAR | YES | - |
| game_date | DATE | YES | - |
| player_name | VARCHAR | YES | - |
| team_abbreviation | VARCHAR | YES | - |
| opponent | VARCHAR | YES | - |
| location | VARCHAR | YES | - |
| wl | VARCHAR | YES | - |
| min | VARCHAR | YES | - |
| fgm | INTEGER | YES | - |
| fga | INTEGER | YES | - |
| fg_pct | DOUBLE | YES | - |
| fg3m | INTEGER | YES | - |
| fg3a | INTEGER | YES | - |
| fg3_pct | DOUBLE | YES | - |
| ftm | INTEGER | YES | - |
| fta | INTEGER | YES | - |
| ft_pct | DOUBLE | YES | - |
| oreb | INTEGER | YES | - |
| dreb | INTEGER | YES | - |
| reb | INTEGER | YES | - |
| ast | INTEGER | YES | - |
| stl | INTEGER | YES | - |
| blk | INTEGER | YES | - |
| tov | INTEGER | YES | - |
| pf | INTEGER | YES | - |
| pts | INTEGER | YES | - |
| plus_minus | INTEGER | YES | - |
| game_score | DOUBLE | YES | - |

### br_player_season_advanced

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| season_id | VARCHAR | NO | - |
| season_end_year | INTEGER | YES | - |
| player_name | VARCHAR | NO | - |
| team_abbreviation | VARCHAR | NO | - |
| position | VARCHAR | YES | - |
| age | DOUBLE | YES | - |
| games_played | DOUBLE | YES | - |
| minutes_played | DOUBLE | YES | - |
| per | DOUBLE | YES | - |
| ts_pct | DOUBLE | YES | - |
| fg3a_rate | DOUBLE | YES | - |
| fta_rate | DOUBLE | YES | - |
| oreb_pct | DOUBLE | YES | - |
| dreb_pct | DOUBLE | YES | - |
| reb_pct | DOUBLE | YES | - |
| ast_pct | DOUBLE | YES | - |
| stl_pct | DOUBLE | YES | - |
| blk_pct | DOUBLE | YES | - |
| tov_pct | DOUBLE | YES | - |
| usg_pct | DOUBLE | YES | - |
| ows | DOUBLE | YES | - |
| dws | DOUBLE | YES | - |
| ws | DOUBLE | YES | - |
| ws_48 | DOUBLE | YES | - |
| obpm | DOUBLE | YES | - |
| dbpm | DOUBLE | YES | - |
| bpm | DOUBLE | YES | - |
| vorp | DOUBLE | YES | - |

**Constraints:**
- PRIMARY KEY: PRIMARY KEY(season_id, player_name, team_abbreviation)
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL

### br_player_season_advanced_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| season_id | VARCHAR | YES | - |
| season_end_year | INTEGER | YES | - |
| player_name | VARCHAR | YES | - |
| team_abbreviation | VARCHAR | YES | - |
| position | VARCHAR | YES | - |
| age | DOUBLE | YES | - |
| games_played | DOUBLE | YES | - |
| minutes_played | DOUBLE | YES | - |
| per | DOUBLE | YES | - |
| ts_pct | DOUBLE | YES | - |
| fg3a_rate | DOUBLE | YES | - |
| fta_rate | DOUBLE | YES | - |
| oreb_pct | DOUBLE | YES | - |
| dreb_pct | DOUBLE | YES | - |
| reb_pct | DOUBLE | YES | - |
| ast_pct | DOUBLE | YES | - |
| stl_pct | DOUBLE | YES | - |
| blk_pct | DOUBLE | YES | - |
| tov_pct | DOUBLE | YES | - |
| usg_pct | DOUBLE | YES | - |
| ows | DOUBLE | YES | - |
| dws | DOUBLE | YES | - |
| ws | DOUBLE | YES | - |
| ws_48 | DOUBLE | YES | - |
| obpm | DOUBLE | YES | - |
| dbpm | DOUBLE | YES | - |
| bpm | DOUBLE | YES | - |
| vorp | DOUBLE | YES | - |

### br_player_season_totals

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| season_id | VARCHAR | NO | - |
| season_end_year | INTEGER | YES | - |
| player_name | VARCHAR | NO | - |
| team_abbreviation | VARCHAR | NO | - |
| position | VARCHAR | YES | - |
| age | DOUBLE | YES | - |
| games_played | DOUBLE | YES | - |
| games_started | DOUBLE | YES | - |
| minutes_played | DOUBLE | YES | - |
| fgm | DOUBLE | YES | - |
| fga | DOUBLE | YES | - |
| fg_pct | DOUBLE | YES | - |
| fg3m | DOUBLE | YES | - |
| fg3a | DOUBLE | YES | - |
| fg3_pct | DOUBLE | YES | - |
| fg2m | DOUBLE | YES | - |
| fg2a | DOUBLE | YES | - |
| fg2_pct | DOUBLE | YES | - |
| efg_pct | DOUBLE | YES | - |
| ftm | DOUBLE | YES | - |
| fta | DOUBLE | YES | - |
| ft_pct | DOUBLE | YES | - |
| oreb | DOUBLE | YES | - |
| dreb | DOUBLE | YES | - |
| reb | DOUBLE | YES | - |
| ast | DOUBLE | YES | - |
| stl | DOUBLE | YES | - |
| blk | DOUBLE | YES | - |
| tov | DOUBLE | YES | - |
| pf | DOUBLE | YES | - |
| pts | DOUBLE | YES | - |
| triple_doubles | DOUBLE | YES | - |
| awards | VARCHAR | YES | - |

**Constraints:**
- PRIMARY KEY: PRIMARY KEY(season_id, player_name, team_abbreviation)
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL

### br_player_season_totals_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| season_id | VARCHAR | YES | - |
| season_end_year | INTEGER | YES | - |
| player_name | VARCHAR | YES | - |
| team_abbreviation | VARCHAR | YES | - |
| position | VARCHAR | YES | - |
| age | DOUBLE | YES | - |
| games_played | DOUBLE | YES | - |
| games_started | DOUBLE | YES | - |
| minutes_played | DOUBLE | YES | - |
| fgm | DOUBLE | YES | - |
| fga | DOUBLE | YES | - |
| fg_pct | DOUBLE | YES | - |
| fg3m | DOUBLE | YES | - |
| fg3a | DOUBLE | YES | - |
| fg3_pct | DOUBLE | YES | - |
| fg2m | DOUBLE | YES | - |
| fg2a | DOUBLE | YES | - |
| fg2_pct | DOUBLE | YES | - |
| efg_pct | DOUBLE | YES | - |
| ftm | DOUBLE | YES | - |
| fta | DOUBLE | YES | - |
| ft_pct | DOUBLE | YES | - |
| oreb | DOUBLE | YES | - |
| dreb | DOUBLE | YES | - |
| reb | DOUBLE | YES | - |
| ast | DOUBLE | YES | - |
| stl | DOUBLE | YES | - |
| blk | DOUBLE | YES | - |
| tov | DOUBLE | YES | - |
| pf | DOUBLE | YES | - |
| pts | DOUBLE | YES | - |
| triple_doubles | DOUBLE | YES | - |
| awards | VARCHAR | YES | - |

### br_schedule

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_key | VARCHAR | NO | - |
| season_year | INTEGER | NO | - |
| season_id | VARCHAR | NO | - |
| game_date | DATE | YES | - |
| start_time | VARCHAR | YES | - |
| start_time_str | VARCHAR | YES | - |
| away_team | VARCHAR | NO | - |
| away_team_score | INTEGER | YES | - |
| home_team | VARCHAR | NO | - |
| home_team_score | INTEGER | YES | - |
| overtime_periods | INTEGER | YES | 0 |
| attendance | INTEGER | YES | - |
| arena | VARCHAR | YES | - |
| created_at | TIMESTAMP | YES | CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | YES | CURRENT_TIMESTAMP |

**Constraints:**
- PRIMARY KEY: PRIMARY KEY(game_key)
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL

**Indexes:**
- idx_br_schedule_game_date  
- idx_br_schedule_season  
- idx_br_schedule_teams  

### common_player_info

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| person_id | VARCHAR | YES | - |
| first_name | VARCHAR | YES | - |
| last_name | VARCHAR | YES | - |
| display_first_last | VARCHAR | YES | - |
| display_last_comma_first | VARCHAR | YES | - |
| display_fi_last | VARCHAR | YES | - |
| player_slug | VARCHAR | YES | - |
| birthdate | VARCHAR | YES | - |
| school | VARCHAR | YES | - |
| country | VARCHAR | YES | - |
| last_affiliation | VARCHAR | YES | - |
| height | VARCHAR | YES | - |
| weight | VARCHAR | YES | - |
| season_exp | VARCHAR | YES | - |
| jersey | VARCHAR | YES | - |
| position | VARCHAR | YES | - |
| rosterstatus | VARCHAR | YES | - |
| games_played_current_season_flag | VARCHAR | YES | - |
| team_id | VARCHAR | YES | - |
| team_name | VARCHAR | YES | - |
| team_abbreviation | VARCHAR | YES | - |
| team_code | VARCHAR | YES | - |
| team_city | VARCHAR | YES | - |
| playercode | VARCHAR | YES | - |
| from_year | VARCHAR | YES | - |
| to_year | VARCHAR | YES | - |
| dleague_flag | VARCHAR | YES | - |
| nba_flag | VARCHAR | YES | - |
| games_played_flag | VARCHAR | YES | - |
| draft_year | VARCHAR | YES | - |
| draft_round | VARCHAR | YES | - |
| draft_number | VARCHAR | YES | - |
| greatest_75_flag | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### common_player_info_raw

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| person_id | BIGINT | NO | - |
| first_name | VARCHAR | YES | - |
| last_name | VARCHAR | YES | - |
| display_first_last | VARCHAR | YES | - |
| display_last_comma_first | VARCHAR | YES | - |
| display_fi_last | VARCHAR | YES | - |
| player_slug | VARCHAR | YES | - |
| birthdate | DATE | YES | - |
| school | VARCHAR | YES | - |
| country | VARCHAR | YES | - |
| last_affiliation | VARCHAR | YES | - |
| height | VARCHAR | YES | - |
| weight | INTEGER | YES | - |
| season_exp | INTEGER | YES | - |
| jersey | VARCHAR | YES | - |
| position | VARCHAR | YES | - |
| roster_status | VARCHAR | YES | - |
| team_id | BIGINT | YES | - |
| team_name | VARCHAR | YES | - |
| team_abbreviation | VARCHAR | YES | - |
| team_city | VARCHAR | YES | - |
| from_year | INTEGER | YES | - |
| to_year | INTEGER | YES | - |
| draft_year | INTEGER | YES | - |
| draft_round | INTEGER | YES | - |
| draft_number | INTEGER | YES | - |
| greatest_75_flag | BOOLEAN | YES | - |

**Constraints:**
- PRIMARY KEY: PRIMARY KEY(person_id)
- NOT NULL: NOT NULL

**Indexes:**
- idx_common_player_info_raw_team  

### common_player_info_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| person_id | BIGINT | YES | - |
| first_name | VARCHAR | YES | - |
| last_name | VARCHAR | YES | - |
| display_first_last | VARCHAR | YES | - |
| display_last_comma_first | VARCHAR | YES | - |
| display_fi_last | VARCHAR | YES | - |
| player_slug | VARCHAR | YES | - |
| birthdate | DATE | YES | - |
| school | VARCHAR | YES | - |
| country | VARCHAR | YES | - |
| last_affiliation | VARCHAR | YES | - |
| height | VARCHAR | YES | - |
| weight | BIGINT | YES | - |
| season_exp | BIGINT | YES | - |
| jersey | VARCHAR | YES | - |
| position | VARCHAR | YES | - |
| rosterstatus | VARCHAR | YES | - |
| games_played_current_season_flag | VARCHAR | YES | - |
| team_id | BIGINT | YES | - |
| team_name | VARCHAR | YES | - |
| team_abbreviation | VARCHAR | YES | - |
| team_code | VARCHAR | YES | - |
| team_city | VARCHAR | YES | - |
| playercode | VARCHAR | YES | - |
| from_year | BIGINT | YES | - |
| to_year | BIGINT | YES | - |
| dleague_flag | VARCHAR | YES | - |
| nba_flag | VARCHAR | YES | - |
| games_played_flag | VARCHAR | YES | - |
| draft_year | VARCHAR | YES | - |
| draft_round | VARCHAR | YES | - |
| draft_number | VARCHAR | YES | - |
| greatest_75_flag | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### draft_combine_stats

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| season | VARCHAR | YES | - |
| player_id | VARCHAR | YES | - |
| first_name | VARCHAR | YES | - |
| last_name | VARCHAR | YES | - |
| player_name | VARCHAR | YES | - |
| position | VARCHAR | YES | - |
| height_wo_shoes | VARCHAR | YES | - |
| height_wo_shoes_ft_in | VARCHAR | YES | - |
| height_w_shoes | VARCHAR | YES | - |
| height_w_shoes_ft_in | VARCHAR | YES | - |
| weight | VARCHAR | YES | - |
| wingspan | VARCHAR | YES | - |
| wingspan_ft_in | VARCHAR | YES | - |
| standing_reach | VARCHAR | YES | - |
| standing_reach_ft_in | VARCHAR | YES | - |
| body_fat_pct | VARCHAR | YES | - |
| hand_length | VARCHAR | YES | - |
| hand_width | VARCHAR | YES | - |
| standing_vertical_leap | VARCHAR | YES | - |
| max_vertical_leap | VARCHAR | YES | - |
| lane_agility_time | VARCHAR | YES | - |
| modified_lane_agility_time | VARCHAR | YES | - |
| three_quarter_sprint | VARCHAR | YES | - |
| bench_press | VARCHAR | YES | - |
| spot_fifteen_corner_left | VARCHAR | YES | - |
| spot_fifteen_break_left | VARCHAR | YES | - |
| spot_fifteen_top_key | VARCHAR | YES | - |
| spot_fifteen_break_right | VARCHAR | YES | - |
| spot_fifteen_corner_right | VARCHAR | YES | - |
| spot_college_corner_left | VARCHAR | YES | - |
| spot_college_break_left | VARCHAR | YES | - |
| spot_college_top_key | VARCHAR | YES | - |
| spot_college_break_right | VARCHAR | YES | - |
| spot_college_corner_right | VARCHAR | YES | - |
| spot_nba_corner_left | VARCHAR | YES | - |
| spot_nba_break_left | VARCHAR | YES | - |
| spot_nba_top_key | VARCHAR | YES | - |
| spot_nba_break_right | VARCHAR | YES | - |
| spot_nba_corner_right | VARCHAR | YES | - |
| off_drib_fifteen_break_left | VARCHAR | YES | - |
| off_drib_fifteen_top_key | VARCHAR | YES | - |
| off_drib_fifteen_break_right | VARCHAR | YES | - |
| off_drib_college_break_left | VARCHAR | YES | - |
| off_drib_college_top_key | VARCHAR | YES | - |
| off_drib_college_break_right | VARCHAR | YES | - |
| on_move_fifteen | VARCHAR | YES | - |
| on_move_college | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### draft_combine_stats_raw

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| season | INTEGER | NO | - |
| player_id | BIGINT | NO | - |
| first_name | VARCHAR | YES | - |
| last_name | VARCHAR | YES | - |
| player_name | VARCHAR | YES | - |
| position | VARCHAR | YES | - |
| height_wo_shoes | DOUBLE | YES | - |
| height_w_shoes | DOUBLE | YES | - |
| weight | DOUBLE | YES | - |
| wingspan | DOUBLE | YES | - |
| standing_reach | DOUBLE | YES | - |
| body_fat_pct | DOUBLE | YES | - |
| hand_length | DOUBLE | YES | - |
| hand_width | DOUBLE | YES | - |
| standing_vertical_leap | DOUBLE | YES | - |
| max_vertical_leap | DOUBLE | YES | - |
| lane_agility_time | DOUBLE | YES | - |
| three_quarter_sprint | DOUBLE | YES | - |
| bench_press | INTEGER | YES | - |

**Constraints:**
- PRIMARY KEY: PRIMARY KEY(season, player_id)
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL

### draft_combine_stats_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| season | BIGINT | YES | - |
| player_id | BIGINT | YES | - |
| first_name | VARCHAR | YES | - |
| last_name | VARCHAR | YES | - |
| player_name | VARCHAR | YES | - |
| position | VARCHAR | YES | - |
| height_wo_shoes | BIGINT | YES | - |
| height_wo_shoes_ft_in | VARCHAR | YES | - |
| height_w_shoes | BIGINT | YES | - |
| height_w_shoes_ft_in | VARCHAR | YES | - |
| weight | BIGINT | YES | - |
| wingspan | BIGINT | YES | - |
| wingspan_ft_in | VARCHAR | YES | - |
| standing_reach | BIGINT | YES | - |
| standing_reach_ft_in | VARCHAR | YES | - |
| body_fat_pct | BIGINT | YES | - |
| hand_length | BIGINT | YES | - |
| hand_width | BIGINT | YES | - |
| standing_vertical_leap | BIGINT | YES | - |
| max_vertical_leap | BIGINT | YES | - |
| lane_agility_time | BIGINT | YES | - |
| modified_lane_agility_time | BIGINT | YES | - |
| three_quarter_sprint | BIGINT | YES | - |
| bench_press | BIGINT | YES | - |
| spot_fifteen_corner_left | VARCHAR | YES | - |
| spot_fifteen_break_left | VARCHAR | YES | - |
| spot_fifteen_top_key | VARCHAR | YES | - |
| spot_fifteen_break_right | VARCHAR | YES | - |
| spot_fifteen_corner_right | VARCHAR | YES | - |
| spot_college_corner_left | VARCHAR | YES | - |
| spot_college_break_left | VARCHAR | YES | - |
| spot_college_top_key | VARCHAR | YES | - |
| spot_college_break_right | VARCHAR | YES | - |
| spot_college_corner_right | VARCHAR | YES | - |
| spot_nba_corner_left | VARCHAR | YES | - |
| spot_nba_break_left | VARCHAR | YES | - |
| spot_nba_top_key | VARCHAR | YES | - |
| spot_nba_break_right | VARCHAR | YES | - |
| spot_nba_corner_right | VARCHAR | YES | - |
| off_drib_fifteen_break_left | VARCHAR | YES | - |
| off_drib_fifteen_top_key | VARCHAR | YES | - |
| off_drib_fifteen_break_right | VARCHAR | YES | - |
| off_drib_college_break_left | VARCHAR | YES | - |
| off_drib_college_top_key | VARCHAR | YES | - |
| off_drib_college_break_right | VARCHAR | YES | - |
| on_move_fifteen | VARCHAR | YES | - |
| on_move_college | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### draft_history

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| person_id | VARCHAR | YES | - |
| player_name | VARCHAR | YES | - |
| season | VARCHAR | YES | - |
| round_number | VARCHAR | YES | - |
| round_pick | VARCHAR | YES | - |
| overall_pick | VARCHAR | YES | - |
| draft_type | VARCHAR | YES | - |
| team_id | VARCHAR | YES | - |
| team_city | VARCHAR | YES | - |
| team_name | VARCHAR | YES | - |
| team_abbreviation | VARCHAR | YES | - |
| organization | VARCHAR | YES | - |
| organization_type | VARCHAR | YES | - |
| player_profile_flag | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### draft_history_raw

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| person_id | BIGINT | NO | - |
| player_name | VARCHAR | YES | - |
| season | INTEGER | NO | - |
| round_number | INTEGER | YES | - |
| round_pick | INTEGER | YES | - |
| overall_pick | INTEGER | YES | - |
| draft_type | VARCHAR | YES | - |
| team_id | BIGINT | YES | - |
| team_city | VARCHAR | YES | - |
| team_name | VARCHAR | YES | - |
| team_abbreviation | VARCHAR | YES | - |
| organization | VARCHAR | YES | - |
| organization_type | VARCHAR | YES | - |

**Constraints:**
- PRIMARY KEY: PRIMARY KEY(person_id, season)
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL

**Indexes:**
- idx_draft_history_raw_team  

### draft_history_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| person_id | BIGINT | YES | - |
| player_name | VARCHAR | YES | - |
| season | BIGINT | YES | - |
| round_number | BIGINT | YES | - |
| round_pick | BIGINT | YES | - |
| overall_pick | BIGINT | YES | - |
| draft_type | VARCHAR | YES | - |
| team_id | BIGINT | YES | - |
| team_city | VARCHAR | YES | - |
| team_name | VARCHAR | YES | - |
| team_abbreviation | VARCHAR | YES | - |
| organization | VARCHAR | YES | - |
| organization_type | VARCHAR | YES | - |
| player_profile_flag | BIGINT | YES | - |
| filename | VARCHAR | YES | - |

### franchise_history_raw

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| league_id | VARCHAR | YES | - |
| team_id | BIGINT | YES | - |
| team_city | VARCHAR | YES | - |
| team_name | VARCHAR | YES | - |
| start_year | BIGINT | YES | - |
| end_year | BIGINT | YES | - |
| years_active | BIGINT | YES | - |
| games_played | BIGINT | YES | - |
| wins | BIGINT | YES | - |
| losses | BIGINT | YES | - |
| win_pct | DOUBLE | YES | - |
| playoff_appearances | BIGINT | YES | - |
| division_titles | BIGINT | YES | - |
| conference_titles | BIGINT | YES | - |
| championships | BIGINT | YES | - |
| filename | VARCHAR | YES | - |

### franchise_leaders_raw

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| team_id | BIGINT | YES | - |
| player_id | BIGINT | YES | - |
| player_name | VARCHAR | YES | - |
| stat_category | VARCHAR | YES | - |
| stat_value | BIGINT | YES | - |
| stat_rank | BIGINT | YES | - |
| games_played | BIGINT | YES | - |
| field_goals_made | BIGINT | YES | - |
| field_goals_attempted | BIGINT | YES | - |
| three_pointers_made | BIGINT | YES | - |
| three_pointers_attempted | BIGINT | YES | - |
| free_throws_made | BIGINT | YES | - |
| free_throws_attempted | BIGINT | YES | - |
| filename | VARCHAR | YES | - |

### game

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| season_id | VARCHAR | YES | - |
| team_id_home | VARCHAR | YES | - |
| team_abbreviation_home | VARCHAR | YES | - |
| team_name_home | VARCHAR | YES | - |
| game_id | VARCHAR | YES | - |
| game_date | VARCHAR | YES | - |
| matchup_home | VARCHAR | YES | - |
| wl_home | VARCHAR | YES | - |
| min | VARCHAR | YES | - |
| fgm_home | VARCHAR | YES | - |
| fga_home | VARCHAR | YES | - |
| fg_pct_home | VARCHAR | YES | - |
| fg3m_home | VARCHAR | YES | - |
| fg3a_home | VARCHAR | YES | - |
| fg3_pct_home | VARCHAR | YES | - |
| ftm_home | VARCHAR | YES | - |
| fta_home | VARCHAR | YES | - |
| ft_pct_home | VARCHAR | YES | - |
| oreb_home | VARCHAR | YES | - |
| dreb_home | VARCHAR | YES | - |
| reb_home | VARCHAR | YES | - |
| ast_home | VARCHAR | YES | - |
| stl_home | VARCHAR | YES | - |
| blk_home | VARCHAR | YES | - |
| tov_home | VARCHAR | YES | - |
| pf_home | VARCHAR | YES | - |
| pts_home | VARCHAR | YES | - |
| plus_minus_home | VARCHAR | YES | - |
| video_available_home | VARCHAR | YES | - |
| team_id_away | VARCHAR | YES | - |
| team_abbreviation_away | VARCHAR | YES | - |
| team_name_away | VARCHAR | YES | - |
| matchup_away | VARCHAR | YES | - |
| wl_away | VARCHAR | YES | - |
| fgm_away | VARCHAR | YES | - |
| fga_away | VARCHAR | YES | - |
| fg_pct_away | VARCHAR | YES | - |
| fg3m_away | VARCHAR | YES | - |
| fg3a_away | VARCHAR | YES | - |
| fg3_pct_away | VARCHAR | YES | - |
| ftm_away | VARCHAR | YES | - |
| fta_away | VARCHAR | YES | - |
| ft_pct_away | VARCHAR | YES | - |
| oreb_away | VARCHAR | YES | - |
| dreb_away | VARCHAR | YES | - |
| reb_away | VARCHAR | YES | - |
| ast_away | VARCHAR | YES | - |
| stl_away | VARCHAR | YES | - |
| blk_away | VARCHAR | YES | - |
| tov_away | VARCHAR | YES | - |
| pf_away | VARCHAR | YES | - |
| pts_away | VARCHAR | YES | - |
| plus_minus_away | VARCHAR | YES | - |
| video_available_away | VARCHAR | YES | - |
| season_type | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### game_gold

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | NO | - |
| season_id | VARCHAR | YES | - |
| game_date | DATE | YES | - |
| home_team_id | BIGINT | YES | - |
| away_team_id | BIGINT | YES | - |
| home_pts | INTEGER | YES | - |
| away_pts | INTEGER | YES | - |
| home_win | BOOLEAN | YES | - |
| season_type | VARCHAR | YES | - |

**Constraints:**
- PRIMARY KEY: PRIMARY KEY(game_id)
- NOT NULL: NOT NULL

### game_gold_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | YES | - |
| season_id | BIGINT | YES | - |
| game_date | DATE | YES | - |
| team_id_home | BIGINT | YES | - |
| team_abbreviation_home | VARCHAR | YES | - |
| team_name_home | VARCHAR | YES | - |
| matchup_home | VARCHAR | YES | - |
| wl_home | VARCHAR | YES | - |
| min | BIGINT | YES | - |
| fgm_home | BIGINT | YES | - |
| fga_home | BIGINT | YES | - |
| fg_pct_home | BIGINT | YES | - |
| fg3m_home | BIGINT | YES | - |
| fg3a_home | BIGINT | YES | - |
| fg3_pct_home | BIGINT | YES | - |
| ftm_home | BIGINT | YES | - |
| fta_home | BIGINT | YES | - |
| ft_pct_home | BIGINT | YES | - |
| oreb_home | BIGINT | YES | - |
| dreb_home | BIGINT | YES | - |
| reb_home | BIGINT | YES | - |
| ast_home | BIGINT | YES | - |
| stl_home | BIGINT | YES | - |
| blk_home | BIGINT | YES | - |
| tov_home | BIGINT | YES | - |
| pf_home | BIGINT | YES | - |
| pts_home | BIGINT | YES | - |
| plus_minus_home | BIGINT | YES | - |
| video_available_home | BIGINT | YES | - |
| team_id_away | BIGINT | YES | - |
| team_abbreviation_away | VARCHAR | YES | - |
| team_name_away | VARCHAR | YES | - |
| matchup_away | VARCHAR | YES | - |
| wl_away | VARCHAR | YES | - |
| fgm_away | BIGINT | YES | - |
| fga_away | BIGINT | YES | - |
| fg_pct_away | BIGINT | YES | - |
| fg3m_away | BIGINT | YES | - |
| fg3a_away | BIGINT | YES | - |
| fg3_pct_away | BIGINT | YES | - |
| ftm_away | BIGINT | YES | - |
| fta_away | BIGINT | YES | - |
| ft_pct_away | BIGINT | YES | - |
| oreb_away | BIGINT | YES | - |
| dreb_away | BIGINT | YES | - |
| reb_away | BIGINT | YES | - |
| ast_away | BIGINT | YES | - |
| stl_away | BIGINT | YES | - |
| blk_away | BIGINT | YES | - |
| tov_away | BIGINT | YES | - |
| pf_away | BIGINT | YES | - |
| pts_away | BIGINT | YES | - |
| plus_minus_away | BIGINT | YES | - |
| video_available_away | BIGINT | YES | - |
| season_type | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### game_info

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | VARCHAR | YES | - |
| game_date | VARCHAR | YES | - |
| attendance | VARCHAR | YES | - |
| game_time | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### game_info_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | YES | - |
| game_date | DATE | YES | - |
| attendance | BIGINT | YES | - |
| game_time | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### game_raw

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | NO | - |
| season_id | VARCHAR | YES | - |
| game_date | DATE | YES | - |
| team_id_home | BIGINT | YES | - |
| team_abbreviation_home | VARCHAR | YES | - |
| team_name_home | VARCHAR | YES | - |
| matchup_home | VARCHAR | YES | - |
| wl_home | VARCHAR | YES | - |
| pts_home | INTEGER | YES | - |
| fg_pct_home | DOUBLE | YES | - |
| ft_pct_home | DOUBLE | YES | - |
| fg3_pct_home | DOUBLE | YES | - |
| ast_home | INTEGER | YES | - |
| reb_home | INTEGER | YES | - |
| team_id_away | BIGINT | YES | - |
| team_abbreviation_away | VARCHAR | YES | - |
| team_name_away | VARCHAR | YES | - |
| matchup_away | VARCHAR | YES | - |
| wl_away | VARCHAR | YES | - |
| pts_away | INTEGER | YES | - |
| fg_pct_away | DOUBLE | YES | - |
| ft_pct_away | DOUBLE | YES | - |
| fg3_pct_away | DOUBLE | YES | - |
| ast_away | INTEGER | YES | - |
| reb_away | INTEGER | YES | - |
| season_type | VARCHAR | YES | - |

**Constraints:**
- PRIMARY KEY: PRIMARY KEY(game_id)
- NOT NULL: NOT NULL

**Indexes:**
- idx_game_raw_away_team  
- idx_game_raw_date  
- idx_game_raw_home_team  

### game_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| season_id | BIGINT | YES | - |
| team_id_home | BIGINT | YES | - |
| team_abbreviation_home | VARCHAR | YES | - |
| team_name_home | VARCHAR | YES | - |
| game_id | BIGINT | YES | - |
| game_date | DATE | YES | - |
| matchup_home | VARCHAR | YES | - |
| wl_home | VARCHAR | YES | - |
| min | BIGINT | YES | - |
| fgm_home | BIGINT | YES | - |
| fga_home | BIGINT | YES | - |
| fg_pct_home | BIGINT | YES | - |
| fg3m_home | BIGINT | YES | - |
| fg3a_home | BIGINT | YES | - |
| fg3_pct_home | BIGINT | YES | - |
| ftm_home | BIGINT | YES | - |
| fta_home | BIGINT | YES | - |
| ft_pct_home | BIGINT | YES | - |
| oreb_home | BIGINT | YES | - |
| dreb_home | BIGINT | YES | - |
| reb_home | BIGINT | YES | - |
| ast_home | BIGINT | YES | - |
| stl_home | BIGINT | YES | - |
| blk_home | BIGINT | YES | - |
| tov_home | BIGINT | YES | - |
| pf_home | BIGINT | YES | - |
| pts_home | BIGINT | YES | - |
| plus_minus_home | BIGINT | YES | - |
| video_available_home | BIGINT | YES | - |
| team_id_away | BIGINT | YES | - |
| team_abbreviation_away | VARCHAR | YES | - |
| team_name_away | VARCHAR | YES | - |
| matchup_away | VARCHAR | YES | - |
| wl_away | VARCHAR | YES | - |
| fgm_away | BIGINT | YES | - |
| fga_away | BIGINT | YES | - |
| fg_pct_away | BIGINT | YES | - |
| fg3m_away | BIGINT | YES | - |
| fg3a_away | BIGINT | YES | - |
| fg3_pct_away | BIGINT | YES | - |
| ftm_away | BIGINT | YES | - |
| fta_away | BIGINT | YES | - |
| ft_pct_away | BIGINT | YES | - |
| oreb_away | BIGINT | YES | - |
| dreb_away | BIGINT | YES | - |
| reb_away | BIGINT | YES | - |
| ast_away | BIGINT | YES | - |
| stl_away | BIGINT | YES | - |
| blk_away | BIGINT | YES | - |
| tov_away | BIGINT | YES | - |
| pf_away | BIGINT | YES | - |
| pts_away | BIGINT | YES | - |
| plus_minus_away | BIGINT | YES | - |
| video_available_away | BIGINT | YES | - |
| season_type | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### game_summary

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_date_est | VARCHAR | YES | - |
| game_sequence | VARCHAR | YES | - |
| game_id | VARCHAR | YES | - |
| game_status_id | VARCHAR | YES | - |
| game_status_text | VARCHAR | YES | - |
| gamecode | VARCHAR | YES | - |
| home_team_id | VARCHAR | YES | - |
| visitor_team_id | VARCHAR | YES | - |
| season | VARCHAR | YES | - |
| live_period | VARCHAR | YES | - |
| live_pc_time | VARCHAR | YES | - |
| natl_tv_broadcaster_abbreviation | VARCHAR | YES | - |
| live_period_time_bcast | VARCHAR | YES | - |
| wh_status | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### game_summary_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_date_est | DATE | YES | - |
| game_sequence | BIGINT | YES | - |
| game_id | BIGINT | YES | - |
| game_status_id | BIGINT | YES | - |
| game_status_text | VARCHAR | YES | - |
| gamecode | VARCHAR | YES | - |
| home_team_id | BIGINT | YES | - |
| visitor_team_id | BIGINT | YES | - |
| season | BIGINT | YES | - |
| live_period | BIGINT | YES | - |
| live_pc_time | VARCHAR | YES | - |
| natl_tv_broadcaster_abbreviation | VARCHAR | YES | - |
| live_period_time_bcast | VARCHAR | YES | - |
| wh_status | BIGINT | YES | - |
| filename | VARCHAR | YES | - |

### games

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | NO | - |
| season_id | BIGINT | YES | - |
| game_date | DATE | YES | - |
| home_team_id | BIGINT | YES | - |
| visitor_team_id | BIGINT | YES | - |
| home_pts | BIGINT | YES | - |
| visitor_pts | BIGINT | YES | - |
| home_wl | VARCHAR | YES | - |
| visitor_wl | VARCHAR | YES | - |
| season_type | VARCHAR | YES | - |

**Constraints:**
- NOT NULL: NOT NULL

**Indexes:**
- idx_games_game_id UNIQUE 

### games_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | YES | - |
| season_id | BIGINT | YES | - |
| game_date | DATE | YES | - |
| home_team_id | BIGINT | YES | - |
| visitor_team_id | BIGINT | YES | - |
| home_pts | BIGINT | YES | - |
| visitor_pts | BIGINT | YES | - |
| home_wl | VARCHAR | YES | - |
| visitor_wl | VARCHAR | YES | - |
| season_type | VARCHAR | YES | - |

### inactive_players

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | VARCHAR | YES | - |
| player_id | VARCHAR | YES | - |
| first_name | VARCHAR | YES | - |
| last_name | VARCHAR | YES | - |
| jersey_num | VARCHAR | YES | - |
| team_id | VARCHAR | YES | - |
| team_city | VARCHAR | YES | - |
| team_name | VARCHAR | YES | - |
| team_abbreviation | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### inactive_players_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | YES | - |
| player_id | BIGINT | YES | - |
| first_name | VARCHAR | YES | - |
| last_name | VARCHAR | YES | - |
| jersey_num | BIGINT | YES | - |
| team_id | BIGINT | YES | - |
| team_city | VARCHAR | YES | - |
| team_name | VARCHAR | YES | - |
| team_abbreviation | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### line_score

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_date_est | VARCHAR | YES | - |
| game_sequence | VARCHAR | YES | - |
| game_id | VARCHAR | YES | - |
| team_id_home | VARCHAR | YES | - |
| team_abbreviation_home | VARCHAR | YES | - |
| team_city_name_home | VARCHAR | YES | - |
| team_nickname_home | VARCHAR | YES | - |
| team_wins_losses_home | VARCHAR | YES | - |
| pts_qtr1_home | VARCHAR | YES | - |
| pts_qtr2_home | VARCHAR | YES | - |
| pts_qtr3_home | VARCHAR | YES | - |
| pts_qtr4_home | VARCHAR | YES | - |
| pts_ot1_home | VARCHAR | YES | - |
| pts_ot2_home | VARCHAR | YES | - |
| pts_ot3_home | VARCHAR | YES | - |
| pts_ot4_home | VARCHAR | YES | - |
| pts_ot5_home | VARCHAR | YES | - |
| pts_ot6_home | VARCHAR | YES | - |
| pts_ot7_home | VARCHAR | YES | - |
| pts_ot8_home | VARCHAR | YES | - |
| pts_ot9_home | VARCHAR | YES | - |
| pts_ot10_home | VARCHAR | YES | - |
| pts_home | VARCHAR | YES | - |
| team_id_away | VARCHAR | YES | - |
| team_abbreviation_away | VARCHAR | YES | - |
| team_city_name_away | VARCHAR | YES | - |
| team_nickname_away | VARCHAR | YES | - |
| team_wins_losses_away | VARCHAR | YES | - |
| pts_qtr1_away | VARCHAR | YES | - |
| pts_qtr2_away | VARCHAR | YES | - |
| pts_qtr3_away | VARCHAR | YES | - |
| pts_qtr4_away | VARCHAR | YES | - |
| pts_ot1_away | VARCHAR | YES | - |
| pts_ot2_away | VARCHAR | YES | - |
| pts_ot3_away | VARCHAR | YES | - |
| pts_ot4_away | VARCHAR | YES | - |
| pts_ot5_away | VARCHAR | YES | - |
| pts_ot6_away | VARCHAR | YES | - |
| pts_ot7_away | VARCHAR | YES | - |
| pts_ot8_away | VARCHAR | YES | - |
| pts_ot9_away | VARCHAR | YES | - |
| pts_ot10_away | VARCHAR | YES | - |
| pts_away | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### line_score_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_date_est | DATE | YES | - |
| game_sequence | BIGINT | YES | - |
| game_id | BIGINT | YES | - |
| team_id_home | BIGINT | YES | - |
| team_abbreviation_home | VARCHAR | YES | - |
| team_city_name_home | VARCHAR | YES | - |
| team_nickname_home | VARCHAR | YES | - |
| team_wins_losses_home | VARCHAR | YES | - |
| pts_qtr1_home | BIGINT | YES | - |
| pts_qtr2_home | BIGINT | YES | - |
| pts_qtr3_home | BIGINT | YES | - |
| pts_qtr4_home | BIGINT | YES | - |
| pts_ot1_home | BIGINT | YES | - |
| pts_ot2_home | BIGINT | YES | - |
| pts_ot3_home | BIGINT | YES | - |
| pts_ot4_home | BIGINT | YES | - |
| pts_ot5_home | BIGINT | YES | - |
| pts_ot6_home | BIGINT | YES | - |
| pts_ot7_home | BIGINT | YES | - |
| pts_ot8_home | BIGINT | YES | - |
| pts_ot9_home | BIGINT | YES | - |
| pts_ot10_home | BIGINT | YES | - |
| pts_home | BIGINT | YES | - |
| team_id_away | BIGINT | YES | - |
| team_abbreviation_away | VARCHAR | YES | - |
| team_city_name_away | VARCHAR | YES | - |
| team_nickname_away | VARCHAR | YES | - |
| team_wins_losses_away | VARCHAR | YES | - |
| pts_qtr1_away | BIGINT | YES | - |
| pts_qtr2_away | BIGINT | YES | - |
| pts_qtr3_away | BIGINT | YES | - |
| pts_qtr4_away | BIGINT | YES | - |
| pts_ot1_away | BIGINT | YES | - |
| pts_ot2_away | BIGINT | YES | - |
| pts_ot3_away | BIGINT | YES | - |
| pts_ot4_away | BIGINT | YES | - |
| pts_ot5_away | BIGINT | YES | - |
| pts_ot6_away | BIGINT | YES | - |
| pts_ot7_away | BIGINT | YES | - |
| pts_ot8_away | BIGINT | YES | - |
| pts_ot9_away | BIGINT | YES | - |
| pts_ot10_away | BIGINT | YES | - |
| pts_away | BIGINT | YES | - |
| filename | VARCHAR | YES | - |

### officials

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | VARCHAR | YES | - |
| official_id | VARCHAR | YES | - |
| first_name | VARCHAR | YES | - |
| last_name | VARCHAR | YES | - |
| jersey_num | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### officials_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | YES | - |
| official_id | BIGINT | YES | - |
| first_name | VARCHAR | YES | - |
| last_name | VARCHAR | YES | - |
| jersey_num | BIGINT | YES | - |
| filename | VARCHAR | YES | - |

### other_stats

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | VARCHAR | YES | - |
| league_id | VARCHAR | YES | - |
| team_id_home | VARCHAR | YES | - |
| team_abbreviation_home | VARCHAR | YES | - |
| team_city_home | VARCHAR | YES | - |
| pts_paint_home | VARCHAR | YES | - |
| pts_2nd_chance_home | VARCHAR | YES | - |
| pts_fb_home | VARCHAR | YES | - |
| largest_lead_home | VARCHAR | YES | - |
| lead_changes | VARCHAR | YES | - |
| times_tied | VARCHAR | YES | - |
| team_turnovers_home | VARCHAR | YES | - |
| total_turnovers_home | VARCHAR | YES | - |
| team_rebounds_home | VARCHAR | YES | - |
| pts_off_to_home | VARCHAR | YES | - |
| team_id_away | VARCHAR | YES | - |
| team_abbreviation_away | VARCHAR | YES | - |
| team_city_away | VARCHAR | YES | - |
| pts_paint_away | VARCHAR | YES | - |
| pts_2nd_chance_away | VARCHAR | YES | - |
| pts_fb_away | VARCHAR | YES | - |
| largest_lead_away | VARCHAR | YES | - |
| team_turnovers_away | VARCHAR | YES | - |
| total_turnovers_away | VARCHAR | YES | - |
| team_rebounds_away | VARCHAR | YES | - |
| pts_off_to_away | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### other_stats_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | YES | - |
| league_id | BIGINT | YES | - |
| team_id_home | BIGINT | YES | - |
| team_abbreviation_home | VARCHAR | YES | - |
| team_city_home | VARCHAR | YES | - |
| pts_paint_home | BIGINT | YES | - |
| pts_2nd_chance_home | BIGINT | YES | - |
| pts_fb_home | BIGINT | YES | - |
| largest_lead_home | BIGINT | YES | - |
| lead_changes | BIGINT | YES | - |
| times_tied | BIGINT | YES | - |
| team_turnovers_home | BIGINT | YES | - |
| total_turnovers_home | BIGINT | YES | - |
| team_rebounds_home | BIGINT | YES | - |
| pts_off_to_home | BIGINT | YES | - |
| team_id_away | BIGINT | YES | - |
| team_abbreviation_away | VARCHAR | YES | - |
| team_city_away | VARCHAR | YES | - |
| pts_paint_away | BIGINT | YES | - |
| pts_2nd_chance_away | BIGINT | YES | - |
| pts_fb_away | BIGINT | YES | - |
| largest_lead_away | BIGINT | YES | - |
| team_turnovers_away | BIGINT | YES | - |
| total_turnovers_away | BIGINT | YES | - |
| team_rebounds_away | BIGINT | YES | - |
| pts_off_to_away | BIGINT | YES | - |
| filename | VARCHAR | YES | - |

### play_by_play

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | NO | - |
| action_number | BIGINT | NO | - |
| clock | VARCHAR | YES | - |
| period | INTEGER | YES | - |
| team_id | BIGINT | YES | - |
| team_tricode | VARCHAR | YES | - |
| person_id | BIGINT | YES | - |
| player_name | VARCHAR | YES | - |
| player_name_i | VARCHAR | YES | - |
| x_legacy | DOUBLE | YES | - |
| y_legacy | DOUBLE | YES | - |
| shot_distance | DOUBLE | YES | - |
| shot_result | VARCHAR | YES | - |
| is_field_goal | INTEGER | YES | - |
| score_home | VARCHAR | YES | - |
| score_away | VARCHAR | YES | - |
| points_total | INTEGER | YES | - |
| location | VARCHAR | YES | - |
| description | VARCHAR | YES | - |
| action_type | VARCHAR | YES | - |
| sub_type | VARCHAR | YES | - |
| video_available | INTEGER | YES | - |
| shot_value | INTEGER | YES | - |
| action_id | INTEGER | YES | - |

**Constraints:**
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL
- PRIMARY KEY: PRIMARY KEY(game_id, action_number)

**Indexes:**
- idx_play_by_play_game  
- idx_play_by_play_person  

### play_by_play_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | YES | - |
| action_number | BIGINT | YES | - |
| clock | VARCHAR | YES | - |
| period | INTEGER | YES | - |
| team_id | BIGINT | YES | - |
| team_tricode | VARCHAR | YES | - |
| person_id | BIGINT | YES | - |
| player_name | VARCHAR | YES | - |
| player_name_i | VARCHAR | YES | - |
| x_legacy | DOUBLE | YES | - |
| y_legacy | DOUBLE | YES | - |
| shot_distance | DOUBLE | YES | - |
| shot_result | VARCHAR | YES | - |
| is_field_goal | INTEGER | YES | - |
| score_home | VARCHAR | YES | - |
| score_away | VARCHAR | YES | - |
| points_total | INTEGER | YES | - |
| location | VARCHAR | YES | - |
| description | VARCHAR | YES | - |
| action_type | VARCHAR | YES | - |
| sub_type | VARCHAR | YES | - |
| video_available | INTEGER | YES | - |
| shot_value | INTEGER | YES | - |
| action_id | INTEGER | YES | - |

### player

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| id | VARCHAR | YES | - |
| full_name | VARCHAR | YES | - |
| first_name | VARCHAR | YES | - |
| last_name | VARCHAR | YES | - |
| is_active | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### player_game_stats

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | NO | - |
| team_id | BIGINT | YES | - |
| player_id | BIGINT | NO | - |
| player_name | VARCHAR | YES | - |
| start_position | VARCHAR | YES | - |
| comment | VARCHAR | YES | - |
| min | VARCHAR | YES | - |
| fgm | INTEGER | YES | - |
| fga | INTEGER | YES | - |
| fg_pct | DOUBLE | YES | - |
| fg3m | INTEGER | YES | - |
| fg3a | INTEGER | YES | - |
| fg3_pct | DOUBLE | YES | - |
| ftm | INTEGER | YES | - |
| fta | INTEGER | YES | - |
| ft_pct | DOUBLE | YES | - |
| oreb | INTEGER | YES | - |
| dreb | INTEGER | YES | - |
| reb | INTEGER | YES | - |
| ast | INTEGER | YES | - |
| stl | INTEGER | YES | - |
| blk | INTEGER | YES | - |
| tov | INTEGER | YES | - |
| pf | INTEGER | YES | - |
| pts | INTEGER | YES | - |
| plus_minus | DOUBLE | YES | - |

**Constraints:**
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL
- PRIMARY KEY: PRIMARY KEY(game_id, player_id)

**Indexes:**
- idx_player_game_stats_game  
- idx_player_game_stats_player  
- idx_player_game_stats_team  

### player_game_stats_raw

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | NO | - |
| team_id | BIGINT | YES | - |
| player_id | BIGINT | NO | - |
| player_name | VARCHAR | YES | - |
| start_position | VARCHAR | YES | - |
| comment | VARCHAR | YES | - |
| min | VARCHAR | YES | - |
| fgm | INTEGER | YES | - |
| fga | INTEGER | YES | - |
| fg_pct | DOUBLE | YES | - |
| fg3m | INTEGER | YES | - |
| fg3a | INTEGER | YES | - |
| fg3_pct | DOUBLE | YES | - |
| ftm | INTEGER | YES | - |
| fta | INTEGER | YES | - |
| ft_pct | DOUBLE | YES | - |
| oreb | INTEGER | YES | - |
| dreb | INTEGER | YES | - |
| reb | INTEGER | YES | - |
| ast | INTEGER | YES | - |
| stl | INTEGER | YES | - |
| blk | INTEGER | YES | - |
| tov | INTEGER | YES | - |
| pf | INTEGER | YES | - |
| pts | INTEGER | YES | - |
| plus_minus | DOUBLE | YES | - |

**Constraints:**
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL
- PRIMARY KEY: PRIMARY KEY(game_id, player_id)

### player_game_stats_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | YES | - |
| team_id | BIGINT | YES | - |
| player_id | BIGINT | YES | - |
| player_name | VARCHAR | YES | - |
| start_position | VARCHAR | YES | - |
| comment | VARCHAR | YES | - |
| min | BIGINT | YES | - |
| fgm | INTEGER | YES | - |
| fga | INTEGER | YES | - |
| fg_pct | DOUBLE | YES | - |
| fg3m | INTEGER | YES | - |
| fg3a | INTEGER | YES | - |
| fg3_pct | DOUBLE | YES | - |
| ftm | INTEGER | YES | - |
| fta | INTEGER | YES | - |
| ft_pct | DOUBLE | YES | - |
| oreb | INTEGER | YES | - |
| dreb | INTEGER | YES | - |
| reb | INTEGER | YES | - |
| ast | INTEGER | YES | - |
| stl | INTEGER | YES | - |
| blk | INTEGER | YES | - |
| tov | INTEGER | YES | - |
| pf | INTEGER | YES | - |
| pts | INTEGER | YES | - |
| plus_minus | DOUBLE | YES | - |

### player_gold

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| id | BIGINT | NO | - |
| full_name | VARCHAR | YES | - |
| first_name | VARCHAR | YES | - |
| last_name | VARCHAR | YES | - |
| is_active | BIGINT | YES | - |

**Constraints:**
- NOT NULL: NOT NULL

**Indexes:**
- idx_player_gold_id UNIQUE 

### player_gold_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| id | BIGINT | YES | - |
| full_name | VARCHAR | YES | - |
| first_name | VARCHAR | YES | - |
| last_name | VARCHAR | YES | - |
| is_active | BIGINT | YES | - |

### player_raw

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| id | BIGINT | NO | - |
| full_name | VARCHAR | NO | - |
| first_name | VARCHAR | YES | - |
| last_name | VARCHAR | NO | - |
| is_active | BOOLEAN | YES | CAST('f' AS BOOLEAN) |

**Constraints:**
- PRIMARY KEY: PRIMARY KEY(id)
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL

### player_season_averages

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| player_id | BIGINT | YES | - |
| player_name | VARCHAR | YES | - |
| season_id | BIGINT | YES | - |
| games_played | BIGINT | YES | - |
| ppg | DOUBLE | YES | - |
| rpg | DOUBLE | YES | - |
| apg | DOUBLE | YES | - |
| spg | DOUBLE | YES | - |
| bpg | DOUBLE | YES | - |
| topg | DOUBLE | YES | - |
| fg_pct | DOUBLE | YES | - |
| fg3_pct | DOUBLE | YES | - |
| ft_pct | DOUBLE | YES | - |
| avg_game_score | DOUBLE | YES | - |

### player_season_stats

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| player_id | BIGINT | NO | - |
| player_name | VARCHAR | YES | - |
| team_id | BIGINT | NO | - |
| team_abbreviation | VARCHAR | YES | - |
| season_id | VARCHAR | NO | - |
| season_type | VARCHAR | YES | - |
| games_played | INTEGER | YES | - |
| minutes_played | DOUBLE | YES | - |
| fgm | DOUBLE | YES | - |
| fga | DOUBLE | YES | - |
| fg_pct | DOUBLE | YES | - |
| fg3m | DOUBLE | YES | - |
| fg3a | DOUBLE | YES | - |
| fg3_pct | DOUBLE | YES | - |
| ftm | DOUBLE | YES | - |
| fta | DOUBLE | YES | - |
| ft_pct | DOUBLE | YES | - |
| oreb | DOUBLE | YES | - |
| dreb | DOUBLE | YES | - |
| reb | DOUBLE | YES | - |
| ast | DOUBLE | YES | - |
| stl | DOUBLE | YES | - |
| blk | DOUBLE | YES | - |
| tov | DOUBLE | YES | - |
| pf | DOUBLE | YES | - |
| pts | DOUBLE | YES | - |
| plus_minus | DOUBLE | YES | - |
| ts_pct | DOUBLE | YES | - |
| efg_pct | DOUBLE | YES | - |

**Constraints:**
- NOT NULL: NOT NULL
- PRIMARY KEY: PRIMARY KEY(player_id, season_id, team_id)
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL

**Indexes:**
- idx_player_season_stats_player  
- idx_player_season_stats_season  
- idx_player_season_stats_team  

### player_season_stats_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| player_id | BIGINT | YES | - |
| player_name | VARCHAR | YES | - |
| team_id | BIGINT | YES | - |
| team_abbreviation | VARCHAR | YES | - |
| season_id | BIGINT | YES | - |
| season_type | VARCHAR | YES | - |
| games_played | BIGINT | YES | - |
| minutes_played | DOUBLE | YES | - |
| fgm | HUGEINT | YES | - |
| fga | HUGEINT | YES | - |
| fg_pct | DOUBLE | YES | - |
| fg3m | HUGEINT | YES | - |
| fg3a | HUGEINT | YES | - |
| fg3_pct | DOUBLE | YES | - |
| ftm | HUGEINT | YES | - |
| fta | HUGEINT | YES | - |
| ft_pct | DOUBLE | YES | - |
| oreb | HUGEINT | YES | - |
| dreb | HUGEINT | YES | - |
| reb | HUGEINT | YES | - |
| ast | HUGEINT | YES | - |
| stl | HUGEINT | YES | - |
| blk | HUGEINT | YES | - |
| tov | HUGEINT | YES | - |
| pf | HUGEINT | YES | - |
| pts | HUGEINT | YES | - |
| plus_minus | DOUBLE | YES | - |
| ts_pct | DOUBLE | YES | - |
| efg_pct | DOUBLE | YES | - |

### player_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| id | BIGINT | NO | - |
| full_name | VARCHAR | NO | - |
| first_name | VARCHAR | YES | - |
| last_name | VARCHAR | NO | - |
| is_active | BOOLEAN | YES | CAST('f' AS BOOLEAN) |

**Constraints:**
- PRIMARY KEY: PRIMARY KEY(id)
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL

### player_splits_raw

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| season_id | VARCHAR | YES | - |
| season_type | VARCHAR | YES | - |
| player_id | BIGINT | YES | - |
| player_name | VARCHAR | YES | - |
| team_id | BIGINT | YES | - |
| team_abbreviation | VARCHAR | YES | - |
| split_type | VARCHAR | YES | - |
| split_category | VARCHAR | YES | - |
| split_value | VARCHAR | YES | - |
| games_played | BIGINT | YES | - |
| wins | BIGINT | YES | - |
| losses | BIGINT | YES | - |
| win_pct | DOUBLE | YES | - |
| minutes | DOUBLE | YES | - |
| fgm | BIGINT | YES | - |
| fga | BIGINT | YES | - |
| fg_pct | DOUBLE | YES | - |
| fg3m | BIGINT | YES | - |
| fg3a | BIGINT | YES | - |
| fg3_pct | DOUBLE | YES | - |
| ftm | BIGINT | YES | - |
| fta | BIGINT | YES | - |
| ft_pct | DOUBLE | YES | - |
| oreb | BIGINT | YES | - |
| dreb | BIGINT | YES | - |
| reb | BIGINT | YES | - |
| ast | BIGINT | YES | - |
| stl | BIGINT | YES | - |
| blk | BIGINT | YES | - |
| tov | BIGINT | YES | - |
| pf | BIGINT | YES | - |
| pts | BIGINT | YES | - |
| plus_minus | BIGINT | YES | - |
| efg_pct | DOUBLE | YES | - |
| filename | VARCHAR | YES | - |

### team

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| id | VARCHAR | YES | - |
| full_name | VARCHAR | YES | - |
| abbreviation | VARCHAR | YES | - |
| nickname | VARCHAR | YES | - |
| city | VARCHAR | YES | - |
| state | VARCHAR | YES | - |
| year_founded | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### team_details

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| team_id | VARCHAR | YES | - |
| abbreviation | VARCHAR | YES | - |
| nickname | VARCHAR | YES | - |
| yearfounded | VARCHAR | YES | - |
| city | VARCHAR | YES | - |
| arena | VARCHAR | YES | - |
| arenacapacity | VARCHAR | YES | - |
| owner | VARCHAR | YES | - |
| generalmanager | VARCHAR | YES | - |
| headcoach | VARCHAR | YES | - |
| dleagueaffiliation | VARCHAR | YES | - |
| facebook | VARCHAR | YES | - |
| instagram | VARCHAR | YES | - |
| twitter | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### team_details_raw

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| team_id | BIGINT | NO | - |
| abbreviation | VARCHAR | YES | - |
| nickname | VARCHAR | YES | - |
| year_founded | INTEGER | YES | - |
| city | VARCHAR | YES | - |
| arena | VARCHAR | YES | - |
| arena_capacity | INTEGER | YES | - |
| owner | VARCHAR | YES | - |
| general_manager | VARCHAR | YES | - |
| head_coach | VARCHAR | YES | - |
| dleague_affiliation | VARCHAR | YES | - |
| facebook | VARCHAR | YES | - |
| instagram | VARCHAR | YES | - |
| twitter | VARCHAR | YES | - |

**Constraints:**
- PRIMARY KEY: PRIMARY KEY(team_id)
- NOT NULL: NOT NULL

### team_details_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| team_id | BIGINT | YES | - |
| abbreviation | VARCHAR | YES | - |
| nickname | VARCHAR | YES | - |
| yearfounded | BIGINT | YES | - |
| city | VARCHAR | YES | - |
| arena | VARCHAR | YES | - |
| arenacapacity | BIGINT | YES | - |
| owner | VARCHAR | YES | - |
| generalmanager | VARCHAR | YES | - |
| headcoach | VARCHAR | YES | - |
| dleagueaffiliation | VARCHAR | YES | - |
| facebook | VARCHAR | YES | - |
| instagram | VARCHAR | YES | - |
| twitter | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### team_game_stats

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | YES | - |
| team_id | BIGINT | YES | - |
| season_id | BIGINT | YES | - |
| game_date | DATE | YES | - |
| is_home | BOOLEAN | YES | - |
| pts | BIGINT | YES | - |
| fgm | BIGINT | YES | - |
| fga | BIGINT | YES | - |
| fg_pct | BIGINT | YES | - |
| fg3m | BIGINT | YES | - |
| fg3a | BIGINT | YES | - |
| fg3_pct | BIGINT | YES | - |
| ftm | BIGINT | YES | - |
| fta | BIGINT | YES | - |
| ft_pct | BIGINT | YES | - |
| oreb | BIGINT | YES | - |
| dreb | BIGINT | YES | - |
| reb | BIGINT | YES | - |
| ast | BIGINT | YES | - |
| stl | BIGINT | YES | - |
| blk | BIGINT | YES | - |
| tov | BIGINT | YES | - |
| pf | BIGINT | YES | - |
| plus_minus | BIGINT | YES | - |

### team_game_stats_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | YES | - |
| team_id | BIGINT | YES | - |
| season_id | BIGINT | YES | - |
| game_date | DATE | YES | - |
| is_home | BOOLEAN | YES | - |
| pts | BIGINT | YES | - |
| fgm | BIGINT | YES | - |
| fga | BIGINT | YES | - |
| fg_pct | BIGINT | YES | - |
| fg3m | BIGINT | YES | - |
| fg3a | BIGINT | YES | - |
| fg3_pct | BIGINT | YES | - |
| ftm | BIGINT | YES | - |
| fta | BIGINT | YES | - |
| ft_pct | BIGINT | YES | - |
| oreb | BIGINT | YES | - |
| dreb | BIGINT | YES | - |
| reb | BIGINT | YES | - |
| ast | BIGINT | YES | - |
| stl | BIGINT | YES | - |
| blk | BIGINT | YES | - |
| tov | BIGINT | YES | - |
| pf | BIGINT | YES | - |
| plus_minus | BIGINT | YES | - |

### team_gold

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| id | BIGINT | NO | - |
| full_name | VARCHAR | YES | - |
| abbreviation | VARCHAR | YES | - |
| nickname | VARCHAR | YES | - |
| city | VARCHAR | YES | - |
| state | VARCHAR | YES | - |
| year_founded | BIGINT | YES | - |

**Constraints:**
- NOT NULL: NOT NULL

**Indexes:**
- idx_team_gold_id UNIQUE 

### team_gold_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| id | BIGINT | YES | - |
| full_name | VARCHAR | YES | - |
| abbreviation | VARCHAR | YES | - |
| nickname | VARCHAR | YES | - |
| city | VARCHAR | YES | - |
| state | VARCHAR | YES | - |
| year_founded | BIGINT | YES | - |

### team_history

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| team_id | VARCHAR | YES | - |
| city | VARCHAR | YES | - |
| nickname | VARCHAR | YES | - |
| year_founded | VARCHAR | YES | - |
| year_active_till | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### team_history_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| team_id | BIGINT | YES | - |
| city | VARCHAR | YES | - |
| nickname | VARCHAR | YES | - |
| year_founded | BIGINT | YES | - |
| year_active_till | BIGINT | YES | - |
| filename | VARCHAR | YES | - |

### team_info_common

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| team_id | VARCHAR | YES | - |
| season_year | VARCHAR | YES | - |
| team_city | VARCHAR | YES | - |
| team_name | VARCHAR | YES | - |
| team_abbreviation | VARCHAR | YES | - |
| team_conference | VARCHAR | YES | - |
| team_division | VARCHAR | YES | - |
| team_code | VARCHAR | YES | - |
| team_slug | VARCHAR | YES | - |
| w | VARCHAR | YES | - |
| l | VARCHAR | YES | - |
| pct | VARCHAR | YES | - |
| conf_rank | VARCHAR | YES | - |
| div_rank | VARCHAR | YES | - |
| min_year | VARCHAR | YES | - |
| max_year | VARCHAR | YES | - |
| league_id | VARCHAR | YES | - |
| season_id | VARCHAR | YES | - |
| pts_rank | VARCHAR | YES | - |
| pts_pg | VARCHAR | YES | - |
| reb_rank | VARCHAR | YES | - |
| reb_pg | VARCHAR | YES | - |
| ast_rank | VARCHAR | YES | - |
| ast_pg | VARCHAR | YES | - |
| opp_pts_rank | VARCHAR | YES | - |
| opp_pts_pg | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### team_info_common_raw

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| team_id | BIGINT | NO | - |
| season_year | VARCHAR | NO | - |
| team_city | VARCHAR | YES | - |
| team_name | VARCHAR | YES | - |
| team_abbreviation | VARCHAR | YES | - |
| team_conference | VARCHAR | YES | - |
| team_division | VARCHAR | YES | - |
| team_code | VARCHAR | YES | - |
| team_slug | VARCHAR | YES | - |
| w | INTEGER | YES | - |
| l | INTEGER | YES | - |
| pct | DOUBLE | YES | - |
| conf_rank | INTEGER | YES | - |
| div_rank | INTEGER | YES | - |
| min_year | INTEGER | YES | - |
| max_year | INTEGER | YES | - |
| league_id | VARCHAR | YES | - |
| season_id | VARCHAR | YES | - |
| pts_rank | INTEGER | YES | - |
| pts_pg | DOUBLE | YES | - |
| reb_rank | INTEGER | YES | - |
| reb_pg | DOUBLE | YES | - |
| ast_rank | INTEGER | YES | - |
| ast_pg | DOUBLE | YES | - |
| opp_pts_rank | INTEGER | YES | - |
| opp_pts_pg | DOUBLE | YES | - |
| filename | VARCHAR | YES | - |

**Constraints:**
- PRIMARY KEY: PRIMARY KEY(team_id, season_year)
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL

### team_info_common_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| team_id | VARCHAR | YES | - |
| season_year | VARCHAR | YES | - |
| team_city | VARCHAR | YES | - |
| team_name | VARCHAR | YES | - |
| team_abbreviation | VARCHAR | YES | - |
| team_conference | VARCHAR | YES | - |
| team_division | VARCHAR | YES | - |
| team_code | VARCHAR | YES | - |
| team_slug | VARCHAR | YES | - |
| w | VARCHAR | YES | - |
| l | VARCHAR | YES | - |
| pct | VARCHAR | YES | - |
| conf_rank | VARCHAR | YES | - |
| div_rank | VARCHAR | YES | - |
| min_year | VARCHAR | YES | - |
| max_year | VARCHAR | YES | - |
| league_id | VARCHAR | YES | - |
| season_id | VARCHAR | YES | - |
| pts_rank | VARCHAR | YES | - |
| pts_pg | VARCHAR | YES | - |
| reb_rank | VARCHAR | YES | - |
| reb_pg | VARCHAR | YES | - |
| ast_rank | VARCHAR | YES | - |
| ast_pg | VARCHAR | YES | - |
| opp_pts_rank | VARCHAR | YES | - |
| opp_pts_pg | VARCHAR | YES | - |
| filename | VARCHAR | YES | - |

### team_raw

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| id | BIGINT | NO | - |
| full_name | VARCHAR | NO | - |
| abbreviation | VARCHAR | NO | - |
| nickname | VARCHAR | YES | - |
| city | VARCHAR | YES | - |
| state | VARCHAR | YES | - |
| year_founded | INTEGER | YES | - |

**Constraints:**
- PRIMARY KEY: PRIMARY KEY(id)
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL

### team_rolling_metrics

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| team_id | BIGINT | YES | - |
| game_id | BIGINT | YES | - |
| game_date | DATE | YES | - |
| season_id | BIGINT | YES | - |
| pts | BIGINT | YES | - |
| pts_allowed | BIGINT | YES | - |
| is_win | INTEGER | YES | - |
| rolling_pts_avg | DOUBLE | YES | - |
| rolling_pts_allowed_avg | DOUBLE | YES | - |
| rolling_win_pct | DOUBLE | YES | - |

### team_silver

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| id | BIGINT | NO | - |
| full_name | VARCHAR | NO | - |
| abbreviation | VARCHAR | NO | - |
| nickname | VARCHAR | YES | - |
| city | VARCHAR | YES | - |
| state | VARCHAR | YES | - |
| year_founded | INTEGER | YES | - |

**Constraints:**
- PRIMARY KEY: PRIMARY KEY(id)
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL
- NOT NULL: NOT NULL

### team_standings

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| team_id | BIGINT | YES | - |
| team_name | VARCHAR | YES | - |
| season_id | BIGINT | YES | - |
| games_played | BIGINT | YES | - |
| wins | HUGEINT | YES | - |
| losses | HUGEINT | YES | - |
| win_pct | DOUBLE | YES | - |

### league_season_averages

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| season_id | BIGINT | YES | - |
| total_games | DOUBLE | YES | - |
| total_teams | BIGINT | YES | - |
| avg_pts | DOUBLE | YES | - |
| total_pts | HUGEINT | YES | - |
| avg_fgm | DOUBLE | YES | - |
| avg_fga | DOUBLE | YES | - |
| league_fg_pct | DOUBLE | YES | - |
| league_fg3_pct | DOUBLE | YES | - |
| league_ft_pct | DOUBLE | YES | - |
| league_efg_pct | DOUBLE | YES | - |
| league_ts_pct | DOUBLE | YES | - |
| avg_ast | DOUBLE | YES | - |
| avg_reb | DOUBLE | YES | - |
| avg_tov | DOUBLE | YES | - |
| avg_poss_estimate | DOUBLE | YES | - |

### player_career_summary

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| player_id | BIGINT | YES | - |
| full_name | VARCHAR | YES | - |
| first_name | VARCHAR | YES | - |
| last_name | VARCHAR | YES | - |
| is_active | BIGINT | YES | - |
| height | VARCHAR | YES | - |
| weight | VARCHAR | YES | - |
| position | VARCHAR | YES | - |
| jersey | VARCHAR | YES | - |
| draft_year | VARCHAR | YES | - |
| draft_round | VARCHAR | YES | - |
| draft_number | VARCHAR | YES | - |
| greatest_75_flag | VARCHAR | YES | - |

### player_game_advanced

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | YES | - |
| team_id | BIGINT | YES | - |
| player_id | BIGINT | YES | - |
| player_name | VARCHAR | YES | - |
| start_position | VARCHAR | YES | - |
| comment | VARCHAR | YES | - |
| min | BIGINT | YES | - |
| fgm | INTEGER | YES | - |
| fga | INTEGER | YES | - |
| fg_pct | DOUBLE | YES | - |
| fg3m | INTEGER | YES | - |
| fg3a | INTEGER | YES | - |
| fg3_pct | DOUBLE | YES | - |
| ftm | INTEGER | YES | - |
| fta | INTEGER | YES | - |
| ft_pct | DOUBLE | YES | - |
| oreb | INTEGER | YES | - |
| dreb | INTEGER | YES | - |
| reb | INTEGER | YES | - |
| ast | INTEGER | YES | - |
| stl | INTEGER | YES | - |
| blk | INTEGER | YES | - |
| tov | INTEGER | YES | - |
| pf | INTEGER | YES | - |
| pts | INTEGER | YES | - |
| plus_minus | DOUBLE | YES | - |
| ts_pct | DOUBLE | YES | - |
| efg_pct | DOUBLE | YES | - |
| game_score | DECIMAL(18,1) | YES | - |

### team_four_factors

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | YES | - |
| team_id | BIGINT | YES | - |
| season_id | BIGINT | YES | - |
| game_date | DATE | YES | - |
| is_home | BOOLEAN | YES | - |
| efg_pct | DOUBLE | YES | - |
| tov_pct | DOUBLE | YES | - |
| orb_pct | DOUBLE | YES | - |
| ft_factor | DOUBLE | YES | - |
| is_win | INTEGER | YES | - |
| pts | BIGINT | YES | - |
| plus_minus | BIGINT | YES | - |

### team_game_advanced

| Column | Type | Nullable | Default |
|--------|------|----------|---------|
| game_id | BIGINT | YES | - |
| team_id | BIGINT | YES | - |
| season_id | BIGINT | YES | - |
| game_date | DATE | YES | - |
| is_home | BOOLEAN | YES | - |
| pts | BIGINT | YES | - |
| fgm | BIGINT | YES | - |
| fga | BIGINT | YES | - |
| fg_pct | BIGINT | YES | - |
| fg3m | BIGINT | YES | - |
| fg3a | BIGINT | YES | - |
| fg3_pct | BIGINT | YES | - |
| ftm | BIGINT | YES | - |
| fta | BIGINT | YES | - |
| ft_pct | BIGINT | YES | - |
| oreb | BIGINT | YES | - |
| dreb | BIGINT | YES | - |
| reb | BIGINT | YES | - |
| ast | BIGINT | YES | - |
| stl | BIGINT | YES | - |
| blk | BIGINT | YES | - |
| tov | BIGINT | YES | - |
| pf | BIGINT | YES | - |
| plus_minus | BIGINT | YES | - |
| pts_allowed | BIGINT | YES | - |
| efg_pct | DOUBLE | YES | - |
| ts_pct | DOUBLE | YES | - |

## View Definitions

### duckdb_columns

```sql
CREATE TEMP VIEW duckdb_columns AS SELECT * FROM duckdb_columns() WHERE (NOT internal);
```

### duckdb_constraints

```sql
CREATE TEMP VIEW duckdb_constraints AS SELECT * FROM duckdb_constraints();
```

### duckdb_databases

```sql
CREATE TEMP VIEW duckdb_databases AS SELECT * FROM duckdb_databases() WHERE (NOT internal);
```

### duckdb_indexes

```sql
CREATE TEMP VIEW duckdb_indexes AS SELECT * FROM duckdb_indexes();
```

### duckdb_logs

```sql
CREATE TEMP VIEW duckdb_logs AS SELECT * FROM duckdb_logs((denormalized_table = CAST('t' AS BOOLEAN)));
```

### duckdb_schemas

```sql
CREATE TEMP VIEW duckdb_schemas AS SELECT * FROM duckdb_schemas() WHERE (NOT internal);
```

### duckdb_tables

```sql
CREATE TEMP VIEW duckdb_tables AS SELECT * FROM duckdb_tables() WHERE (NOT internal);
```

### duckdb_types

```sql
CREATE TEMP VIEW duckdb_types AS SELECT * FROM duckdb_types();
```

### duckdb_views

```sql
CREATE TEMP VIEW duckdb_views AS SELECT * FROM duckdb_views() WHERE (NOT internal);
```

### league_season_averages

```sql
CREATE VIEW league_season_averages AS SELECT season_id, (count(DISTINCT game_id) / 2) AS total_games, count(DISTINCT team_id) AS total_teams, avg(pts) AS avg_pts, sum(pts) AS total_pts, avg(fgm) AS avg_fgm, avg(fga) AS avg_fga, (sum(fgm) / "nullif"(sum(fga), 0)) AS league_fg_pct, (sum(fg3m) / "nullif"(sum(fg3a), 0)) AS league_fg3_pct, (sum(ftm) / "nullif"(sum(fta), 0)) AS league_ft_pct, ((sum(fgm) + (0.5 * sum(fg3m))) / "nullif"(sum(fga), 0)) AS league_efg_pct, (sum(pts) / "nullif"((2.0 * (sum(fga) + (0.44 * sum(fta)))), 0)) AS league_ts_pct, avg(ast) AS avg_ast, avg(reb) AS avg_reb, avg(tov) AS avg_tov, ((avg(fga) + (0.44 * avg(fta))) + avg(tov)) AS avg_poss_estimate FROM team_game_stats GROUP BY season_id;
```

### player_career_summary

```sql
CREATE VIEW player_career_summary AS SELECT ps.id AS player_id, ps.full_name, ps.first_name, ps.last_name, ps.is_active, cpi.height, cpi.weight, cpi."position", cpi.jersey, cpi.draft_year, cpi.draft_round, cpi.draft_number, cpi.greatest_75_flag FROM player_silver AS ps LEFT JOIN common_player_info AS cpi ON ((ps.id = cpi.person_id));
```

### player_game_advanced

```sql
CREATE VIEW player_game_advanced AS SELECT pgs.*, CASE  WHEN (((pgs.fga + (0.44 * pgs.fta)) > 0)) THEN ((pgs.pts / (2.0 * (pgs.fga + (0.44 * pgs.fta))))) ELSE 0 END AS ts_pct, CASE  WHEN ((pgs.fga > 0)) THEN (((pgs.fgm + (0.5 * pgs.fg3m)) / pgs.fga)) ELSE 0 END AS efg_pct, ((((((((((pgs.pts + (0.4 * pgs.fgm)) - (0.7 * pgs.fga)) - (0.4 * (pgs.fta - pgs.ftm))) + (0.7 * pgs.oreb)) + (0.3 * pgs.dreb)) + pgs.stl) + (0.7 * pgs.ast)) + (0.7 * pgs.blk)) - (0.4 * pgs.pf)) - pgs.tov) AS game_score FROM player_game_stats AS pgs;
```

### pragma_database_list

```sql
CREATE TEMP VIEW pragma_database_list AS SELECT database_oid AS seq, database_name AS "name", path AS file FROM duckdb_databases() WHERE (NOT internal) ORDER BY 1;
```

### sqlite_master

```sql
CREATE TEMP VIEW sqlite_master AS ((SELECT 'table' AS "type", table_name AS "name", table_name AS tbl_name, 0 AS rootpage, "sql" FROM duckdb_tables) UNION ALL (SELECT 'view' AS "type", view_name AS "name", view_name AS tbl_name, 0 AS rootpage, "sql" FROM duckdb_views)) UNION ALL (SELECT 'index' AS "type", index_name AS "name", table_name AS tbl_name, 0 AS rootpage, "sql" FROM duckdb_indexes);
```

### sqlite_schema

```sql
CREATE TEMP VIEW sqlite_schema AS SELECT * FROM sqlite_master;
```

### sqlite_temp_master

```sql
CREATE TEMP VIEW sqlite_temp_master AS SELECT * FROM sqlite_master;
```

### sqlite_temp_schema

```sql
CREATE TEMP VIEW sqlite_temp_schema AS SELECT * FROM sqlite_master;
```

### team_four_factors

```sql
CREATE VIEW team_four_factors AS SELECT tgs.game_id, tgs.team_id, tgs.season_id, tgs.game_date, tgs.is_home, CASE  WHEN ((tgs.fga > 0)) THEN (((tgs.fgm + (0.5 * COALESCE(tgs.fg3m, 0))) / CAST(tgs.fga AS DOUBLE))) ELSE NULL END AS efg_pct, CASE  WHEN ((((tgs.fga + (0.44 * COALESCE(tgs.fta, 0))) + COALESCE(tgs.tov, 0)) > 0)) THEN (((100.0 * COALESCE(tgs.tov, 0)) / ((tgs.fga + (0.44 * COALESCE(tgs.fta, 0))) + COALESCE(tgs.tov, 0)))) ELSE NULL END AS tov_pct, CASE  WHEN (((COALESCE(tgs.oreb, 0) + COALESCE(tgs.dreb, 0)) > 0)) THEN (((100.0 * COALESCE(tgs.oreb, 0)) / (COALESCE(tgs.oreb, 0) + COALESCE(tgs.dreb, 0)))) ELSE NULL END AS orb_pct, CASE  WHEN ((tgs.fga > 0)) THEN ((CAST(COALESCE(tgs.ftm, 0) AS DOUBLE) / tgs.fga)) ELSE NULL END AS ft_factor, CASE  WHEN ((tgs.plus_minus > 0)) THEN (1) ELSE 0 END AS is_win, tgs.pts, tgs.plus_minus FROM team_game_stats AS tgs;
```

### team_game_advanced

```sql
CREATE VIEW team_game_advanced AS SELECT tgs.*, CASE  WHEN (tgs.is_home) THEN (g.visitor_pts) ELSE g.home_pts END AS pts_allowed, CASE  WHEN ((tgs.fga > 0)) THEN (((tgs.fgm + (0.5 * tgs.fg3m)) / tgs.fga)) ELSE 0 END AS efg_pct, CASE  WHEN (((tgs.fga + (0.44 * tgs.fta)) > 0)) THEN ((tgs.pts / (2.0 * (tgs.fga + (0.44 * tgs.fta))))) ELSE 0 END AS ts_pct FROM team_game_stats AS tgs INNER JOIN games AS g ON ((tgs.game_id = g.game_id));
```

