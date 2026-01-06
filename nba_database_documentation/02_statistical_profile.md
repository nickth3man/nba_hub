# NBA Database - Statistical Profile

*Generated: 2026-01-05 16:58:23*

## Summary

- **Total Columns Profiled**: 1052
- **Total Tables**: 51

## all_star_selections

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| player_name | VARCHAR | 526 | 0.0 | nan | nan | nan | nan |
| br_player_id | VARCHAR | 526 | 0.0 | nan | nan | nan | nan |
| team | VARCHAR | 10 | 0.0 | nan | nan | nan | nan |
| season_end_year | INTEGER | 73 | 0.0 | 1951 | 2024 | 1986.9820359281437 | 1985.0 |
| league | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| replaced | BOOLEAN | 2 | 0.0 | nan | nan | nan | nan |

## award_voting_shares

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| season_end_year | INTEGER | 77 | 0.0 | 1948 | 2024 | 1999.7859876361495 | 2004.0 |
| award | VARCHAR | 9 | 0.0 | nan | nan | nan | nan |
| player_name | VARCHAR | 1025 | 0.0 | nan | nan | nan | nan |
| br_player_id | VARCHAR | 1025 | 0.0 | nan | nan | nan | nan |
| age | DOUBLE | 22 | 0.0 | 19.0 | 40.0 | 26.125110391521932 | 26.0 |
| first_place_votes | DOUBLE | 153 | 1.12 | 0.0 | 159.0 | 8.187258112533492 | 1.0 |
| pts_won | DOUBLE | 481 | 0.65 | 0.1 | 1310.0 | 72.82782222222222 | 7.0 |
| pts_max | DOUBLE | 105 | 0.65 | 17.0 | 1310.0 | 560.4450370370371 | 600.0 |
| share | DOUBLE | 619 | 0.65 | 0.001 | 1.0 | 0.1283274074074064 | 0.02 |
| winner | BOOLEAN | 2 | 0.0 | nan | nan | nan | nan |

## br_player_season_advanced

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| season_id | VARCHAR | 80 | 0.0 | nan | nan | nan | nan |
| season_end_year | INTEGER | 80 | 0.0 | 1947 | 2026 | 1996.1593739633906 | 1999.0 |
| player_name | VARCHAR | 5354 | 0.0 | nan | nan | nan | nan |
| team_abbreviation | VARCHAR | 109 | 0.0 | nan | nan | nan | nan |
| position | VARCHAR | 5 | 3.68 | nan | nan | nan | nan |
| age | DOUBLE | 28 | 0.13 | 18.0 | 46.0 | 26.469412404130683 | 26.0 |
| games_played | DOUBLE | 89 | 0.07 | 1.0 | 90.0 | 48.09403102178768 | 53.0 |
| minutes_played | DOUBLE | 3363 | 3.34 | 0.0 | 3882.0 | 1143.6567462174387 | 958.0 |
| per | DOUBLE | 624 | 3.39 | -90.6 | 133.8 | 12.516040327111503 | 12.7 |
| ts_pct | DOUBLE | 696 | 0.43 | 0.0 | 1.5 | 0.4987279059906713 | 0.511 |
| fg3a_rate | DOUBLE | 883 | 19.62 | 0.0 | 1.0 | 0.20683407112845098 | 0.127 |
| fta_rate | DOUBLE | 963 | 0.49 | 0.0 | 6.0 | 0.3123090280934641 | 0.284 |
| oreb_pct | DOUBLE | 337 | 15.98 | 0.0 | 100.0 | 5.988937941925946 | 5.0 |
| dreb_pct | DOUBLE | 443 | 15.98 | 0.0 | 100.0 | 13.96376296615347 | 13.0 |
| reb_pct | DOUBLE | 351 | 11.18 | 0.0 | 100.0 | 9.97651432839881 | 9.1 |
| ast_pct | DOUBLE | 529 | 8.22 | 0.0 | 100.0 | 12.97781574451315 | 10.5 |
| stl_pct | DOUBLE | 128 | 16.91 | 0.0 | 48.2 | 1.631576655052263 | 1.5 |
| blk_pct | DOUBLE | 143 | 16.91 | 0.0 | 77.8 | 1.492872178268114 | 1.0 |
| tov_pct | DOUBLE | 430 | 17.34 | 0.0 | 100.0 | 14.59132496716756 | 13.7 |
| usg_pct | DOUBLE | 434 | 17.03 | 0.0 | 100.0 | 18.813149669259303 | 18.5 |
| ows | DOUBLE | 197 | 0.1 | -5.1 | 18.3 | 1.180801159175302 | 0.4 |
| dws | DOUBLE | 108 | 0.1 | -1.0 | 16.0 | 1.1529869894647344 | 0.8 |
| ws | DOUBLE | 230 | 0.1 | -2.8 | 25.4 | 2.3349503426208043 | 1.3 |
| ws_48 | DOUBLE | 919 | 3.39 | -2.519 | 2.712 | 0.06630573069479975 | 0.076 |
| obpm | DOUBLE | 418 | 17.12 | -68.9 | 199.4 | -1.6304675277424123 | -1.4 |
| dbpm | DOUBLE | 256 | 17.12 | -31.1 | 60.7 | -0.22282699654356916 | -0.2 |
| bpm | DOUBLE | 504 | 17.12 | -92.1 | 242.2 | -1.8534582499545296 | -1.5 |
| vorp | DOUBLE | 128 | 17.1 | -2.6 | 12.5 | 0.5332520916696847 | 0.1 |

## br_player_season_advanced_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| season_id | VARCHAR | 23 | 0.0 | nan | nan | nan | nan |
| season_end_year | INTEGER | 23 | 0.0 | 1973 | 1996 | 1985.9688061041293 | 1987.0 |
| player_name | VARCHAR | 1688 | 0.0 | nan | nan | nan | nan |
| team_abbreviation | VARCHAR | 41 | 0.0 | nan | nan | nan | nan |
| position | VARCHAR | 5 | 0.26 | nan | nan | nan | nan |
| age | DOUBLE | 25 | 0.26 | 18.0 | 42.0 | 26.550118123523458 | 26.0 |
| games_played | DOUBLE | 87 | 0.26 | 1.0 | 87.0 | 54.01417482281472 | 64.0 |
| minutes_played | DOUBLE | 2937 | 0.26 | 1.0 | 3681.0 | 1276.478231522106 | 1132.0 |
| per | DOUBLE | 418 | 0.26 | -49.6 | 76.3 | 12.581538980762726 | 12.9 |
| ts_pct | DOUBLE | 495 | 0.25 | 0.0 | 1.136 | 0.5016164229471313 | 0.511 |
| fg3a_rate | DOUBLE | 521 | 20.49 | 0.0 | 1.0 | 0.07548998024273124 | 0.021 |
| fta_rate | DOUBLE | 757 | 0.35 | 0.0 | 4.0 | 0.3335503884697665 | 0.304 |
| oreb_pct | DOUBLE | 253 | 3.03 | 0.0 | 100.0 | 6.66992594306873 | 6.4 |
| dreb_pct | DOUBLE | 352 | 3.03 | 0.0 | 76.5 | 13.143520018514241 | 12.1 |
| reb_pct | DOUBLE | 267 | 0.0 | 0.0 | 75.0 | 9.912623429084372 | 9.4 |
| ast_pct | DOUBLE | 450 | 0.0 | 0.0 | 100.0 | 13.330935816876154 | 11.2 |
| stl_pct | DOUBLE | 88 | 3.03 | 0.0 | 24.2 | 1.6811039111316917 | 1.6 |
| blk_pct | DOUBLE | 106 | 3.03 | 0.0 | 62.9 | 1.2341587595464034 | 0.8 |
| tov_pct | DOUBLE | 361 | 16.16 | 0.0 | 100.0 | 15.852301927194798 | 15.0 |
| usg_pct | DOUBLE | 346 | 16.0 | 0.0 | 100.0 | 19.211928934010228 | 19.0 |
| ows | DOUBLE | 158 | 0.26 | -3.1 | 15.2 | 1.318303521205983 | 0.5 |
| dws | DOUBLE | 86 | 0.26 | -0.4 | 9.9 | 1.3045224434694644 | 0.9 |
| ws | DOUBLE | 192 | 0.26 | -1.8 | 21.9 | 2.6234897063786686 | 1.6 |
| ws_48 | DOUBLE | 598 | 0.26 | -1.365 | 1.442 | 0.06510203622454737 | 0.075 |
| obpm | DOUBLE | 277 | 3.28 | -49.1 | 31.5 | -1.5863921113689137 | -1.4 |
| dbpm | DOUBLE | 167 | 3.28 | -20.3 | 15.2 | -0.21816705336426898 | -0.2 |
| bpm | DOUBLE | 334 | 3.28 | -67.6 | 39.9 | -1.8045823665893361 | -1.6 |
| vorp | DOUBLE | 116 | 3.28 | -2.1 | 12.5 | 0.6145127610208861 | 0.1 |

## br_player_season_totals

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| season_id | VARCHAR | 80 | 0.0 | nan | nan | nan | nan |
| season_end_year | INTEGER | 80 | 0.0 | 1947 | 2026 | 1996.1579169556433 | 1999.0 |
| player_name | VARCHAR | 5354 | 0.0 | nan | nan | nan | nan |
| team_abbreviation | VARCHAR | 109 | 0.0 | nan | nan | nan | nan |
| position | VARCHAR | 5 | 3.68 | nan | nan | nan | nan |
| age | DOUBLE | 28 | 0.13 | 18.0 | 46.0 | 26.46927745402941 | 26.0 |
| games_played | DOUBLE | 89 | 0.07 | 1.0 | 90.0 | 48.09324361024775 | 53.0 |
| games_started | DOUBLE | 85 | 24.67 | 0.0 | 84.0 | 22.277639900728524 | 7.0 |
| minutes_played | DOUBLE | 3363 | 3.34 | 0.0 | 3882.0 | 1143.6350449213876 | 958.0 |
| fgm | DOUBLE | 917 | 0.07 | 0.0 | 1597.0 | 185.50653308790248 | 128.0 |
| fga | DOUBLE | 1757 | 0.07 | 0.0 | 3159.0 | 409.7596789281511 | 294.0 |
| fg_pct | DOUBLE | 592 | 0.1 | 0.0 | 1.0 | 0.4290758504120015 | 0.438 |
| fg3m | DOUBLE | 283 | 19.23 | 0.0 | 402.0 | 26.225574015307075 | 4.0 |
| fg3a | DOUBLE | 643 | 19.24 | 0.0 | 1028.0 | 74.55409946236558 | 17.0 |
| fg3_pct | DOUBLE | 436 | 10.52 | 0.0 | 1.0 | 0.20029342185077778 | 0.235 |
| fg2m | DOUBLE | 836 | 19.23 | 0.0 | 1086.0 | 152.22303528094082 | 95.0 |
| fg2a | DOUBLE | 1525 | 19.23 | 0.0 | 2213.0 | 312.34840395743885 | 199.0 |
| fg2_pct | DOUBLE | 552 | 6.33 | 0.0 | 1.0 | 0.4006839208112033 | 0.46 |
| efg_pct | DOUBLE | 578 | 6.31 | 0.0 | 1.5 | 0.40622207202858196 | 0.469 |
| ftm | DOUBLE | 661 | 0.07 | 0.0 | 840.0 | 95.03286158302906 | 55.0 |
| fta | DOUBLE | 822 | 0.07 | 0.0 | 1363.0 | 126.61232988321916 | 77.0 |
| ft_pct | DOUBLE | 667 | 0.8 | 0.0 | 1.0 | 0.6983989482962931 | 0.741 |
| oreb | DOUBLE | 410 | 14.09 | 0.0 | 587.0 | 58.432171562949705 | 34.0 |
| dreb | DOUBLE | 809 | 14.09 | 0.0 | 1111.0 | 142.96623495138815 | 101.0 |
| reb | DOUBLE | 1186 | 2.77 | 0.0 | 2149.0 | 213.655357419755 | 148.0 |
| ast | DOUBLE | 802 | 0.07 | 0.0 | 1164.0 | 108.34325115422915 | 63.0 |
| stl | DOUBLE | 243 | 16.97 | 0.0 | 346.0 | 37.267550390412204 | 26.0 |
| blk | DOUBLE | 288 | 16.96 | 0.0 | 456.0 | 22.921632712350654 | 11.0 |
| tov | DOUBLE | 357 | 17.07 | 0.0 | 464.0 | 69.48460055997964 | 49.0 |
| pf | DOUBLE | 364 | 0.08 | 0.0 | 386.0 | 107.95449333091919 | 96.0 |
| pts | DOUBLE | 2175 | 0.07 | 0.0 | 4029.0 | 487.2430670810827 | 335.0 |
| triple_doubles | DOUBLE | 18 | 72.4 | 0.0 | 18.0 | 0.10017478697837011 | 0.0 |
| awards | VARCHAR | 298 | 97.08 | nan | nan | nan | nan |

## br_player_season_totals_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| season_id | VARCHAR | 24 | 0.0 | nan | nan | nan | nan |
| season_end_year | INTEGER | 24 | 0.0 | 1972 | 1996 | 1985.5639572891698 | 1986.0 |
| player_name | VARCHAR | 1734 | 0.0 | nan | nan | nan | nan |
| team_abbreviation | VARCHAR | 42 | 0.0 | nan | nan | nan | nan |
| position | VARCHAR | 5 | 0.26 | nan | nan | nan | nan |
| age | DOUBLE | 25 | 0.26 | 18.0 | 42.0 | 26.540856456194014 | 26.0 |
| games_played | DOUBLE | 87 | 0.26 | 1.0 | 87.0 | 54.06772995411842 | 64.0 |
| games_started | DOUBLE | 84 | 26.56 | 0.0 | 83.0 | 26.072848664688426 | 9.0 |
| minutes_played | DOUBLE | 2970 | 0.26 | 1.0 | 3698.0 | 1280.068276163426 | 1134.0 |
| fgm | DOUBLE | 846 | 0.26 | 0.0 | 1159.0 | 221.28140703517587 | 164.0 |
| fga | DOUBLE | 1542 | 0.26 | 0.0 | 2279.0 | 468.00196635350665 | 358.0 |
| fg_pct | DOUBLE | 404 | 0.35 | 0.0 | 1.0 | 0.448435381587581 | 0.458 |
| fg3m | DOUBLE | 177 | 22.71 | 0.0 | 267.0 | 11.138990696363123 | 1.0 |
| fg3a | DOUBLE | 369 | 22.71 | 0.0 | 678.0 | 33.947561319424864 | 5.0 |
| fg3_pct | DOUBLE | 371 | 38.01 | 0.0 | 1.0 | 0.20312673580594173 | 0.214 |
| fg2m | DOUBLE | 782 | 22.71 | 0.0 | 1086.0 | 204.13433887792502 | 148.0 |
| fg2a | DOUBLE | 1382 | 22.71 | 0.0 | 2213.0 | 416.9444601071328 | 310.0 |
| fg2_pct | DOUBLE | 381 | 22.86 | 0.0 | 1.0 | 0.46415070621469 | 0.475 |
| efg_pct | DOUBLE | 391 | 22.79 | 0.0 | 1.0 | 0.463759808072256 | 0.475 |
| ftm | DOUBLE | 548 | 0.26 | 0.0 | 833.0 | 111.60782171728206 | 75.0 |
| fta | DOUBLE | 676 | 0.26 | 0.0 | 972.0 | 148.02894909329254 | 104.0 |
| ft_pct | DOUBLE | 554 | 2.88 | 0.0 | 1.0 | 0.7248791788198342 | 0.748 |
| oreb | DOUBLE | 364 | 6.08 | 0.0 | 573.0 | 74.84872389791184 | 51.0 |
| dreb | DOUBLE | 706 | 6.08 | 0.0 | 1111.0 | 157.06380510440835 | 113.0 |
| reb | DOUBLE | 969 | 0.26 | 0.0 | 1572.0 | 235.49289927900372 | 171.0 |
| ast | DOUBLE | 688 | 0.26 | 0.0 | 1164.0 | 130.99049595805113 | 81.0 |
| stl | DOUBLE | 240 | 6.08 | 0.0 | 301.0 | 45.94060324825986 | 35.0 |
| blk | DOUBLE | 263 | 6.08 | 0.0 | 456.0 | 27.320649651972158 | 12.0 |
| tov | DOUBLE | 330 | 18.63 | 0.0 | 366.0 | 87.41751472951259 | 71.0 |
| pf | DOUBLE | 354 | 0.26 | 0.0 | 386.0 | 128.59613283810356 | 126.0 |
| pts | DOUBLE | 1855 | 0.26 | 0.0 | 3041.0 | 562.8029276818877 | 415.0 |
| triple_doubles | DOUBLE | 18 | 0.26 | 0.0 | 18.0 | 0.10017478697837011 | 0.0 |
| awards | VARCHAR | 298 | 89.43 | nan | nan | nan | nan |

## br_schedule

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_key | VARCHAR | 1321 | 0.0 | nan | nan | nan | nan |
| season_year | INTEGER | 1 | 0.0 | 2025 | 2025 | 2025.0 | 2025.0 |
| season_id | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |
| game_date | DATE | 214 | 0.0 | nan | nan | nan | nan |
| start_time | VARCHAR | 856 | 0.0 | nan | nan | nan | nan |
| start_time_str | VARCHAR | 27 | 0.0 | nan | nan | nan | nan |
| away_team | VARCHAR | 30 | 0.0 | nan | nan | nan | nan |
| away_team_score | INTEGER | 73 | 0.0 | 67 | 162 | 112.54201362604088 | 113.0 |
| home_team | VARCHAR | 30 | 0.0 | nan | nan | nan | nan |
| home_team_score | INTEGER | 72 | 0.0 | 79 | 155 | 114.40878122634368 | 115.0 |
| overtime_periods | INTEGER | 3 | 0.0 | 0 | 2 | 0.05299015897047691 | 0.0 |
| attendance | INTEGER | 674 | 0.0 | 11457 | 22491 | 18185.425435276306 | 18175.0 |
| arena | VARCHAR | 68 | 0.0 | nan | nan | nan | nan |
| created_at | TIMESTAMP | 1 | 0.0 | nan | nan | nan | nan |
| updated_at | TIMESTAMP | 1 | 0.0 | nan | nan | nan | nan |

## common_player_info

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| person_id | VARCHAR | 4171 | 0.0 | nan | nan | nan | nan |
| first_name | VARCHAR | 1434 | 0.0 | nan | nan | nan | nan |
| last_name | VARCHAR | 2576 | 0.0 | nan | nan | nan | nan |
| display_first_last | VARCHAR | 4139 | 0.0 | nan | nan | nan | nan |
| display_last_comma_first | VARCHAR | 4139 | 0.0 | nan | nan | nan | nan |
| display_fi_last | VARCHAR | 3686 | 0.0 | nan | nan | nan | nan |
| player_slug | VARCHAR | 4139 | 0.0 | nan | nan | nan | nan |
| birthdate | VARCHAR | 3895 | 0.0 | nan | nan | nan | nan |
| school | VARCHAR | 643 | 0.36 | nan | nan | nan | nan |
| country | VARCHAR | 73 | 0.02 | nan | nan | nan | nan |
| last_affiliation | VARCHAR | 859 | 0.0 | nan | nan | nan | nan |
| height | VARCHAR | 27 | 2.3 | nan | nan | nan | nan |
| weight | VARCHAR | 141 | 2.4 | nan | nan | nan | nan |
| season_exp | VARCHAR | 23 | 0.0 | nan | nan | nan | nan |
| jersey | VARCHAR | 106 | 23.5 | nan | nan | nan | nan |
| position | VARCHAR | 7 | 1.51 | nan | nan | nan | nan |
| rosterstatus | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| games_played_current_season_flag | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |
| team_id | VARCHAR | 46 | 0.0 | nan | nan | nan | nan |
| team_name | VARCHAR | 50 | 16.83 | nan | nan | nan | nan |
| team_abbreviation | VARCHAR | 69 | 16.83 | nan | nan | nan | nan |
| team_code | VARCHAR | 43 | 16.83 | nan | nan | nan | nan |
| team_city | VARCHAR | 54 | 16.83 | nan | nan | nan | nan |
| playercode | VARCHAR | 4158 | 0.02 | nan | nan | nan | nan |
| from_year | VARCHAR | 77 | 0.36 | nan | nan | nan | nan |
| to_year | VARCHAR | 78 | 0.36 | nan | nan | nan | nan |
| dleague_flag | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| nba_flag | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| games_played_flag | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| draft_year | VARCHAR | 77 | 0.0 | nan | nan | nan | nan |
| draft_round | VARCHAR | 20 | 3.93 | nan | nan | nan | nan |
| draft_number | VARCHAR | 162 | 5.35 | nan | nan | nan | nan |
| greatest_75_flag | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## common_player_info_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| person_id | BIGINT | 4171 | 0.0 | 2 | 1631347 | 332750.8597458643 | 77593.0 |
| first_name | VARCHAR | 1434 | 0.0 | nan | nan | nan | nan |
| last_name | VARCHAR | 2576 | 0.0 | nan | nan | nan | nan |
| display_first_last | VARCHAR | 4139 | 0.0 | nan | nan | nan | nan |
| display_last_comma_first | VARCHAR | 4139 | 0.0 | nan | nan | nan | nan |
| display_fi_last | VARCHAR | 3686 | 0.0 | nan | nan | nan | nan |
| player_slug | VARCHAR | 4139 | 0.0 | nan | nan | nan | nan |
| birthdate | DATE | 3895 | 0.0 | nan | nan | nan | nan |
| school | VARCHAR | 643 | 0.36 | nan | nan | nan | nan |
| country | VARCHAR | 73 | 0.02 | nan | nan | nan | nan |
| last_affiliation | VARCHAR | 859 | 0.0 | nan | nan | nan | nan |
| height | VARCHAR | 27 | 2.3 | nan | nan | nan | nan |
| weight | BIGINT | 141 | 2.4 | 133 | 360 | 211.13338246131173 | 210.0 |
| season_exp | BIGINT | 23 | 0.0 | 0 | 22 | 5.1951570366818505 | 3.0 |
| jersey | VARCHAR | 106 | 23.5 | nan | nan | nan | nan |
| position | VARCHAR | 7 | 1.51 | nan | nan | nan | nan |
| rosterstatus | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| games_played_current_season_flag | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |
| team_id | BIGINT | 46 | 0.0 | 0 | 1610612766 | 1339538483.6772957 | 1610612746.0 |
| team_name | VARCHAR | 50 | 16.83 | nan | nan | nan | nan |
| team_abbreviation | VARCHAR | 69 | 16.83 | nan | nan | nan | nan |
| team_code | VARCHAR | 43 | 16.83 | nan | nan | nan | nan |
| team_city | VARCHAR | 54 | 16.83 | nan | nan | nan | nan |
| playercode | VARCHAR | 4158 | 0.02 | nan | nan | nan | nan |
| from_year | BIGINT | 77 | 0.36 | 1946 | 2022 | 1989.303176130895 | 1992.0 |
| to_year | BIGINT | 78 | 0.36 | 1946 | 2023 | 1993.7466313763234 | 1998.0 |
| dleague_flag | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| nba_flag | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| games_played_flag | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| draft_year | VARCHAR | 77 | 0.0 | nan | nan | nan | nan |
| draft_round | VARCHAR | 20 | 3.93 | nan | nan | nan | nan |
| draft_number | VARCHAR | 162 | 5.35 | nan | nan | nan | nan |
| greatest_75_flag | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## draft_combine_stats

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| season | VARCHAR | 18 | 0.0 | nan | nan | nan | nan |
| player_id | VARCHAR | 1176 | 0.0 | nan | nan | nan | nan |
| first_name | VARCHAR | 696 | 0.0 | nan | nan | nan | nan |
| last_name | VARCHAR | 853 | 0.0 | nan | nan | nan | nan |
| player_name | VARCHAR | 1178 | 0.0 | nan | nan | nan | nan |
| position | VARCHAR | 13 | 0.42 | nan | nan | nan | nan |
| height_wo_shoes | VARCHAR | 71 | 4.08 | nan | nan | nan | nan |
| height_wo_shoes_ft_in | VARCHAR | 120 | 4.08 | nan | nan | nan | nan |
| height_w_shoes | VARCHAR | 82 | 16.14 | nan | nan | nan | nan |
| height_w_shoes_ft_in | VARCHAR | 115 | 16.14 | nan | nan | nan | nan |
| weight | VARCHAR | 542 | 4.16 | nan | nan | nan | nan |
| wingspan | VARCHAR | 88 | 4.08 | nan | nan | nan | nan |
| wingspan_ft_in | VARCHAR | 138 | 4.08 | nan | nan | nan | nan |
| standing_reach | VARCHAR | 55 | 4.16 | nan | nan | nan | nan |
| standing_reach_ft_in | VARCHAR | 116 | 4.16 | nan | nan | nan | nan |
| body_fat_pct | VARCHAR | 184 | 16.56 | nan | nan | nan | nan |
| hand_length | VARCHAR | 13 | 40.18 | nan | nan | nan | nan |
| hand_width | VARCHAR | 21 | 40.18 | nan | nan | nan | nan |
| standing_vertical_leap | VARCHAR | 38 | 15.39 | nan | nan | nan | nan |
| max_vertical_leap | VARCHAR | 41 | 15.39 | nan | nan | nan | nan |
| lane_agility_time | VARCHAR | 251 | 16.14 | nan | nan | nan | nan |
| modified_lane_agility_time | VARCHAR | 106 | 65.81 | nan | nan | nan | nan |
| three_quarter_sprint | VARCHAR | 74 | 15.81 | nan | nan | nan | nan |
| bench_press | VARCHAR | 27 | 32.78 | nan | nan | nan | nan |
| spot_fifteen_corner_left | VARCHAR | 8 | 93.84 | nan | nan | nan | nan |
| spot_fifteen_break_left | VARCHAR | 5 | 93.68 | nan | nan | nan | nan |
| spot_fifteen_top_key | VARCHAR | 5 | 93.68 | nan | nan | nan | nan |
| spot_fifteen_break_right | VARCHAR | 6 | 93.68 | nan | nan | nan | nan |
| spot_fifteen_corner_right | VARCHAR | 6 | 93.68 | nan | nan | nan | nan |
| spot_college_corner_left | VARCHAR | 23 | 79.62 | nan | nan | nan | nan |
| spot_college_break_left | VARCHAR | 8 | 86.19 | nan | nan | nan | nan |
| spot_college_top_key | VARCHAR | 8 | 86.19 | nan | nan | nan | nan |
| spot_college_break_right | VARCHAR | 6 | 86.19 | nan | nan | nan | nan |
| spot_college_corner_right | VARCHAR | 6 | 86.19 | nan | nan | nan | nan |
| spot_nba_corner_left | VARCHAR | 9 | 81.95 | nan | nan | nan | nan |
| spot_nba_break_left | VARCHAR | 8 | 81.95 | nan | nan | nan | nan |
| spot_nba_top_key | VARCHAR | 7 | 81.95 | nan | nan | nan | nan |
| spot_nba_break_right | VARCHAR | 7 | 81.95 | nan | nan | nan | nan |
| spot_nba_corner_right | VARCHAR | 6 | 81.95 | nan | nan | nan | nan |
| off_drib_fifteen_break_left | VARCHAR | 22 | 86.19 | nan | nan | nan | nan |
| off_drib_fifteen_top_key | VARCHAR | 17 | 86.19 | nan | nan | nan | nan |
| off_drib_fifteen_break_right | VARCHAR | 20 | 86.19 | nan | nan | nan | nan |
| off_drib_college_break_left | VARCHAR | 27 | 90.85 | nan | nan | nan | nan |
| off_drib_college_top_key | VARCHAR | 13 | 97.42 | nan | nan | nan | nan |
| off_drib_college_break_right | VARCHAR | 12 | 97.42 | nan | nan | nan | nan |
| on_move_fifteen | VARCHAR | 109 | 87.69 | nan | nan | nan | nan |
| on_move_college | VARCHAR | 50 | 90.35 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## draft_combine_stats_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| season | BIGINT | 18 | 0.0 | 2001 | 2023 | 2012.536605657238 | 2012.0 |
| player_id | BIGINT | 1176 | 0.0 | -1 | 1962937123 | 2350132.544093178 | 203147.0 |
| first_name | VARCHAR | 696 | 0.0 | nan | nan | nan | nan |
| last_name | VARCHAR | 853 | 0.0 | nan | nan | nan | nan |
| player_name | VARCHAR | 1178 | 0.0 | nan | nan | nan | nan |
| position | VARCHAR | 13 | 0.42 | nan | nan | nan | nan |
| height_wo_shoes | BIGINT | 21 | 4.08 | 68 | 89 | 77.68603642671292 | 78.0 |
| height_wo_shoes_ft_in | VARCHAR | 120 | 4.08 | nan | nan | nan | nan |
| height_w_shoes | BIGINT | 20 | 16.14 | 69 | 91 | 78.94642857142857 | 79.0 |
| height_w_shoes_ft_in | VARCHAR | 115 | 16.14 | nan | nan | nan | nan |
| weight | BIGINT | 127 | 4.16 | 154 | 314 | 214.90538194444446 | 213.0 |
| wingspan | BIGINT | 26 | 4.08 | 70 | 98 | 82.5949696444059 | 83.0 |
| wingspan_ft_in | VARCHAR | 138 | 4.08 | nan | nan | nan | nan |
| standing_reach | BIGINT | 28 | 4.16 | 90 | 123 | 103.83420138888889 | 104.0 |
| standing_reach_ft_in | VARCHAR | 116 | 4.16 | nan | nan | nan | nan |
| body_fat_pct | BIGINT | 17 | 16.56 | 3 | 21 | 7.406779661016949 | 7.0 |
| hand_length | BIGINT | 4 | 40.18 | 8 | 11 | 8.853963838664813 | 9.0 |
| hand_width | BIGINT | 6 | 40.18 | 7 | 12 | 9.599443671766343 | 10.0 |
| standing_vertical_leap | BIGINT | 19 | 15.39 | 21 | 40 | 29.49852507374631 | 29.0 |
| max_vertical_leap | BIGINT | 22 | 15.39 | 25 | 46 | 34.89380530973451 | 35.0 |
| lane_agility_time | BIGINT | 4 | 16.14 | 10 | 13 | 11.391865079365079 | 11.0 |
| modified_lane_agility_time | BIGINT | 3 | 65.81 | 2 | 4 | 2.995133819951338 | 3.0 |
| three_quarter_sprint | BIGINT | 2 | 15.81 | 3 | 4 | 3.0701581027667983 | 3.0 |
| bench_press | BIGINT | 27 | 32.78 | 0 | 26 | 10.155940594059405 | 10.0 |
| spot_fifteen_corner_left | VARCHAR | 8 | 93.84 | nan | nan | nan | nan |
| spot_fifteen_break_left | VARCHAR | 5 | 93.68 | nan | nan | nan | nan |
| spot_fifteen_top_key | VARCHAR | 5 | 93.68 | nan | nan | nan | nan |
| spot_fifteen_break_right | VARCHAR | 6 | 93.68 | nan | nan | nan | nan |
| spot_fifteen_corner_right | VARCHAR | 6 | 93.68 | nan | nan | nan | nan |
| spot_college_corner_left | VARCHAR | 23 | 79.62 | nan | nan | nan | nan |
| spot_college_break_left | VARCHAR | 8 | 86.19 | nan | nan | nan | nan |
| spot_college_top_key | VARCHAR | 8 | 86.19 | nan | nan | nan | nan |
| spot_college_break_right | VARCHAR | 6 | 86.19 | nan | nan | nan | nan |
| spot_college_corner_right | VARCHAR | 6 | 86.19 | nan | nan | nan | nan |
| spot_nba_corner_left | VARCHAR | 9 | 81.95 | nan | nan | nan | nan |
| spot_nba_break_left | VARCHAR | 8 | 81.95 | nan | nan | nan | nan |
| spot_nba_top_key | VARCHAR | 7 | 81.95 | nan | nan | nan | nan |
| spot_nba_break_right | VARCHAR | 7 | 81.95 | nan | nan | nan | nan |
| spot_nba_corner_right | VARCHAR | 6 | 81.95 | nan | nan | nan | nan |
| off_drib_fifteen_break_left | VARCHAR | 22 | 86.19 | nan | nan | nan | nan |
| off_drib_fifteen_top_key | VARCHAR | 17 | 86.19 | nan | nan | nan | nan |
| off_drib_fifteen_break_right | VARCHAR | 20 | 86.19 | nan | nan | nan | nan |
| off_drib_college_break_left | VARCHAR | 27 | 90.85 | nan | nan | nan | nan |
| off_drib_college_top_key | VARCHAR | 13 | 97.42 | nan | nan | nan | nan |
| off_drib_college_break_right | VARCHAR | 12 | 97.42 | nan | nan | nan | nan |
| on_move_fifteen | VARCHAR | 109 | 87.69 | nan | nan | nan | nan |
| on_move_college | VARCHAR | 50 | 90.35 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## draft_history

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| person_id | VARCHAR | 8235 | 0.0 | nan | nan | nan | nan |
| player_name | VARCHAR | 8060 | 0.0 | nan | nan | nan | nan |
| season | VARCHAR | 79 | 0.0 | nan | nan | nan | nan |
| round_number | VARCHAR | 22 | 0.0 | nan | nan | nan | nan |
| round_pick | VARCHAR | 31 | 0.0 | nan | nan | nan | nan |
| overall_pick | VARCHAR | 240 | 0.0 | nan | nan | nan | nan |
| draft_type | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| team_id | VARCHAR | 39 | 0.0 | nan | nan | nan | nan |
| team_city | VARCHAR | 51 | 0.0 | nan | nan | nan | nan |
| team_name | VARCHAR | 47 | 0.0 | nan | nan | nan | nan |
| team_abbreviation | VARCHAR | 67 | 0.0 | nan | nan | nan | nan |
| organization | VARCHAR | 928 | 0.0 | nan | nan | nan | nan |
| organization_type | VARCHAR | 4 | 0.0 | nan | nan | nan | nan |
| player_profile_flag | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## draft_history_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| person_id | BIGINT | 8235 | 0.0 | 2 | 1643008 | 200884.2007403869 | 80753.0 |
| player_name | VARCHAR | 8060 | 0.0 | nan | nan | nan | nan |
| season | BIGINT | 79 | 0.0 | 1947 | 2025 | 1980.0259135419155 | 1978.0 |
| round_number | BIGINT | 22 | 0.0 | 0 | 21 | 4.4835204203486985 | 3.0 |
| round_pick | BIGINT | 31 | 0.0 | 0 | 30 | 9.504776689754001 | 8.0 |
| overall_pick | BIGINT | 240 | 0.0 | 0 | 239 | 65.61726773346071 | 48.0 |
| draft_type | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| team_id | BIGINT | 39 | 0.0 | 1610610024 | 1610612766 | 1610612664.6798425 | 1610612751.0 |
| team_city | VARCHAR | 51 | 0.0 | nan | nan | nan | nan |
| team_name | VARCHAR | 47 | 0.0 | nan | nan | nan | nan |
| team_abbreviation | VARCHAR | 67 | 0.0 | nan | nan | nan | nan |
| organization | VARCHAR | 928 | 0.0 | nan | nan | nan | nan |
| organization_type | VARCHAR | 4 | 0.0 | nan | nan | nan | nan |
| player_profile_flag | BIGINT | 2 | 0.0 | 0 | 1 | 0.45020300931454504 | 0.0 |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## franchise_history_raw

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| league_id | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |
| team_id | BIGINT | 30 | 0.0 | 1610612737 | 1610612766 | 1610612752.4594595 | 1610612752.5 |
| team_city | VARCHAR | 47 | 0.0 | nan | nan | nan | nan |
| team_name | VARCHAR | 39 | 0.0 | nan | nan | nan | nan |
| start_year | BIGINT | 38 | 0.0 | 1946 | 2015 | 1972.581081081081 | 1970.5 |
| end_year | BIGINT | 24 | 0.0 | 1950 | 2025 | 1999.581081081081 | 2019.5 |
| years_active | BIGINT | 39 | 0.0 | 1 | 80 | 27.675675675675677 | 23.5 |
| games_played | BIGINT | 57 | 0.0 | 80 | 6231 | 2183.7297297297296 | 1886.5 |
| wins | BIGINT | 60 | 0.0 | 18 | 3717 | 1090.7432432432433 | 860.0 |
| losses | BIGINT | 59 | 0.0 | 35 | 3175 | 1092.9594594594594 | 1003.5 |
| win_pct | DOUBLE | 56 | 0.0 | 0.225 | 0.599 | 0.46760810810810804 | 0.4725 |
| playoff_appearances | BIGINT | 32 | 0.0 | 0 | 62 | 15.675675675675675 | 11.0 |
| division_titles | BIGINT | 18 | 0.0 | 0 | 35 | 4.95945945945946 | 3.0 |
| conference_titles | BIGINT | 10 | 0.0 | 0 | 19 | 1.6486486486486487 | 0.0 |
| championships | BIGINT | 8 | 0.0 | 0 | 18 | 1.2432432432432432 | 0.0 |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## franchise_leaders_raw

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| team_id | BIGINT | 30 | 0.0 | 1610612737 | 1610612766 | 1610612751.5 | 1610612751.5 |
| player_id | BIGINT | 0 | 100.0 | nan | nan | nan | nan |
| player_name | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |
| stat_category | VARCHAR | 5 | 0.0 | nan | nan | nan | nan |
| stat_value | BIGINT | 148 | 0.0 | 600 | 36374 | 7897.053333333333 | 4958.5 |
| stat_rank | BIGINT | 0 | 100.0 | nan | nan | nan | nan |
| games_played | BIGINT | 0 | 100.0 | nan | nan | nan | nan |
| field_goals_made | BIGINT | 0 | 100.0 | nan | nan | nan | nan |
| field_goals_attempted | BIGINT | 0 | 100.0 | nan | nan | nan | nan |
| three_pointers_made | BIGINT | 0 | 100.0 | nan | nan | nan | nan |
| three_pointers_attempted | BIGINT | 0 | 100.0 | nan | nan | nan | nan |
| free_throws_made | BIGINT | 0 | 100.0 | nan | nan | nan | nan |
| free_throws_attempted | BIGINT | 0 | 100.0 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## game

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| season_id | VARCHAR | 225 | 0.0 | nan | nan | nan | nan |
| team_id_home | VARCHAR | 63 | 0.0 | nan | nan | nan | nan |
| team_abbreviation_home | VARCHAR | 97 | 0.0 | nan | nan | nan | nan |
| team_name_home | VARCHAR | 98 | 0.0 | nan | nan | nan | nan |
| game_id | VARCHAR | 65642 | 0.0 | nan | nan | nan | nan |
| game_date | VARCHAR | 12882 | 0.0 | nan | nan | nan | nan |
| matchup_home | VARCHAR | 2292 | 0.0 | nan | nan | nan | nan |
| wl_home | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| min | VARCHAR | 11 | 0.0 | nan | nan | nan | nan |
| fgm_home | VARCHAR | 64 | 0.02 | nan | nan | nan | nan |
| fga_home | VARCHAR | 87 | 23.51 | nan | nan | nan | nan |
| fg_pct_home | VARCHAR | 415 | 23.58 | nan | nan | nan | nan |
| fg3m_home | VARCHAR | 29 | 20.12 | nan | nan | nan | nan |
| fg3a_home | VARCHAR | 69 | 28.44 | nan | nan | nan | nan |
| fg3_pct_home | VARCHAR | 395 | 29.03 | nan | nan | nan | nan |
| ftm_home | VARCHAR | 61 | 0.02 | nan | nan | nan | nan |
| fta_home | VARCHAR | 76 | 4.57 | nan | nan | nan | nan |
| ft_pct_home | VARCHAR | 442 | 4.58 | nan | nan | nan | nan |
| oreb_home | VARCHAR | 37 | 28.82 | nan | nan | nan | nan |
| dreb_home | VARCHAR | 48 | 28.92 | nan | nan | nan | nan |
| reb_home | VARCHAR | 68 | 23.94 | nan | nan | nan | nan |
| ast_home | VARCHAR | 50 | 24.06 | nan | nan | nan | nan |
| stl_home | VARCHAR | 27 | 28.69 | nan | nan | nan | nan |
| blk_home | VARCHAR | 24 | 28.35 | nan | nan | nan | nan |
| tov_home | VARCHAR | 37 | 28.44 | nan | nan | nan | nan |
| pf_home | VARCHAR | 55 | 4.35 | nan | nan | nan | nan |
| pts_home | VARCHAR | 131 | 0.0 | nan | nan | nan | nan |
| plus_minus_home | VARCHAR | 121 | 0.0 | nan | nan | nan | nan |
| video_available_home | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| team_id_away | VARCHAR | 72 | 0.0 | nan | nan | nan | nan |
| team_abbreviation_away | VARCHAR | 101 | 0.0 | nan | nan | nan | nan |
| team_name_away | VARCHAR | 101 | 0.0 | nan | nan | nan | nan |
| matchup_away | VARCHAR | 2292 | 0.0 | nan | nan | nan | nan |
| wl_away | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| fgm_away | VARCHAR | 64 | 0.02 | nan | nan | nan | nan |
| fga_away | VARCHAR | 89 | 23.51 | nan | nan | nan | nan |
| fg_pct_away | VARCHAR | 410 | 23.58 | nan | nan | nan | nan |
| fg3m_away | VARCHAR | 32 | 20.12 | nan | nan | nan | nan |
| fg3a_away | VARCHAR | 68 | 28.44 | nan | nan | nan | nan |
| fg3_pct_away | VARCHAR | 384 | 28.86 | nan | nan | nan | nan |
| ftm_away | VARCHAR | 56 | 0.02 | nan | nan | nan | nan |
| fta_away | VARCHAR | 70 | 4.57 | nan | nan | nan | nan |
| ft_pct_away | VARCHAR | 439 | 4.58 | nan | nan | nan | nan |
| oreb_away | VARCHAR | 37 | 28.82 | nan | nan | nan | nan |
| dreb_away | VARCHAR | 50 | 28.92 | nan | nan | nan | nan |
| reb_away | VARCHAR | 68 | 23.94 | nan | nan | nan | nan |
| ast_away | VARCHAR | 50 | 24.05 | nan | nan | nan | nan |
| stl_away | VARCHAR | 26 | 28.69 | nan | nan | nan | nan |
| blk_away | VARCHAR | 20 | 28.35 | nan | nan | nan | nan |
| tov_away | VARCHAR | 39 | 28.44 | nan | nan | nan | nan |
| pf_away | VARCHAR | 61 | 4.34 | nan | nan | nan | nan |
| pts_away | VARCHAR | 133 | 0.0 | nan | nan | nan | nan |
| plus_minus_away | VARCHAR | 121 | 0.0 | nan | nan | nan | nan |
| video_available_away | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| season_type | VARCHAR | 5 | 0.0 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## game_gold_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_id | BIGINT | 70228 | 0.0 | 10500001 | 49900088 | 25710146.421541266 | 25400252.5 |
| season_id | BIGINT | 225 | 6.53 | 12005 | 42022 | 22941.630053928886 | 21997.0 |
| game_date | DATE | 12882 | 6.53 | nan | nan | nan | nan |
| team_id_home | BIGINT | 63 | 6.53 | 45 | 1610616834 | 1609925696.4542062 | 1610612751.0 |
| team_abbreviation_home | VARCHAR | 97 | 6.53 | nan | nan | nan | nan |
| team_name_home | VARCHAR | 98 | 6.53 | nan | nan | nan | nan |
| matchup_home | VARCHAR | 2292 | 6.53 | nan | nan | nan | nan |
| wl_home | VARCHAR | 2 | 6.53 | nan | nan | nan | nan |
| min | BIGINT | 11 | 6.53 | 0 | 365 | 220.9849029584717 | 240.0 |
| fgm_home | BIGINT | 64 | 6.55 | 4 | 84 | 39.661079705617944 | 40.0 |
| fga_home | BIGINT | 87 | 28.53 | 0 | 240 | 83.96471760135472 | 84.0 |
| fg_pct_home | BIGINT | 2 | 28.59 | 0 | 1 | 0.30702663901738714 | 0.0 |
| fg3m_home | BIGINT | 29 | 25.32 | 0 | 28 | 5.73309689966823 | 5.0 |
| fg3a_home | BIGINT | 69 | 33.1 | 0 | 77 | 17.734722547412783 | 16.0 |
| fg3_pct_home | BIGINT | 2 | 33.66 | 0 | 1 | 0.1517675087463244 | 0.0 |
| ftm_home | BIGINT | 61 | 6.55 | 0 | 61 | 20.69486179258221 | 20.0 |
| fta_home | BIGINT | 76 | 10.81 | 0 | 86 | 27.14339538299435 | 27.0 |
| ft_pct_home | BIGINT | 5 | 10.81 | 0 | 4 | 0.9930548903151643 | 1.0 |
| oreb_home | BIGINT | 37 | 33.47 | 0 | 44 | 12.105746388443018 | 12.0 |
| dreb_home | BIGINT | 48 | 33.56 | 3 | 56 | 31.408126526938407 | 31.0 |
| reb_home | BIGINT | 68 | 28.93 | 0 | 85 | 43.747039849337845 | 43.0 |
| ast_home | BIGINT | 50 | 29.04 | 0 | 60 | 23.931135501735657 | 24.0 |
| stl_home | BIGINT | 27 | 33.34 | 0 | 27 | 7.987225497735623 | 8.0 |
| blk_home | BIGINT | 24 | 33.03 | 0 | 23 | 5.313851387264803 | 5.0 |
| tov_home | BIGINT | 37 | 33.11 | 0 | 39 | 14.778305200195833 | 15.0 |
| pf_home | BIGINT | 55 | 10.6 | 0 | 122 | 22.384608033638074 | 22.0 |
| pts_home | BIGINT | 131 | 6.53 | 18 | 192 | 104.59809268456172 | 105.0 |
| plus_minus_home | BIGINT | 121 | 6.53 | -68 | 73 | 3.6314707047317265 | 4.0 |
| video_available_home | BIGINT | 2 | 6.53 | 0 | 1 | 0.20138021388745012 | 0.0 |
| team_id_away | BIGINT | 72 | 6.53 | 41 | 1610616834 | 1608944249.4706743 | 1610612751.0 |
| team_abbreviation_away | VARCHAR | 101 | 6.53 | nan | nan | nan | nan |
| team_name_away | VARCHAR | 101 | 6.53 | nan | nan | nan | nan |
| matchup_away | VARCHAR | 2292 | 6.53 | nan | nan | nan | nan |
| wl_away | VARCHAR | 2 | 6.53 | nan | nan | nan | nan |
| fgm_away | BIGINT | 64 | 6.55 | 4 | 82 | 38.33956025537491 | 38.0 |
| fga_away | BIGINT | 89 | 28.53 | 0 | 149 | 83.73788225918916 | 83.0 |
| fg_pct_away | BIGINT | 3 | 28.59 | 0 | 4 | 0.22848084860327397 | 0.0 |
| fg3m_away | BIGINT | 32 | 25.32 | 0 | 35 | 5.635529878351066 | 5.0 |
| fg3a_away | BIGINT | 68 | 33.1 | 0 | 90 | 17.769310998063048 | 16.0 |
| fg3_pct_away | BIGINT | 2 | 33.5 | 0 | 1 | 0.1341912551924971 | 0.0 |
| ftm_away | BIGINT | 56 | 6.55 | 0 | 57 | 19.786710143381736 | 19.0 |
| fta_away | BIGINT | 70 | 10.81 | 0 | 91 | 26.0359526166225 | 25.0 |
| ft_pct_away | BIGINT | 5 | 10.81 | 0 | 5 | 0.9919694744236541 | 1.0 |
| oreb_away | BIGINT | 37 | 33.47 | 0 | 40 | 11.682439807383627 | 11.0 |
| dreb_away | BIGINT | 50 | 33.55 | 0 | 60 | 30.233804084606646 | 30.0 |
| reb_away | BIGINT | 68 | 28.92 | 0 | 90 | 42.10445339263177 | 42.0 |
| ast_away | BIGINT | 50 | 29.03 | 0 | 89 | 22.12505768343332 | 22.0 |
| stl_away | BIGINT | 26 | 33.34 | 0 | 27 | 7.849589848756729 | 8.0 |
| blk_away | BIGINT | 20 | 33.02 | 0 | 19 | 4.6813929755931625 | 4.0 |
| tov_away | BIGINT | 39 | 33.11 | 0 | 40 | 15.196560091957938 | 15.0 |
| pf_away | BIGINT | 61 | 10.59 | 0 | 115 | 23.100619515535666 | 23.0 |
| pts_away | BIGINT | 133 | 6.53 | 19 | 196 | 100.96662197982998 | 101.0 |
| plus_minus_away | BIGINT | 121 | 6.53 | -73 | 68 | -3.6314707047317265 | -4.0 |
| video_available_away | BIGINT | 2 | 6.53 | 0 | 1 | 0.20138021388745012 | 0.0 |
| season_type | VARCHAR | 4 | 6.53 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 6.53 | nan | nan | nan | nan |

## game_info

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_id | VARCHAR | 58013 | 0.0 | nan | nan | nan | nan |
| game_date | VARCHAR | 12598 | 0.0 | nan | nan | nan | nan |
| attendance | VARCHAR | 15718 | 9.27 | nan | nan | nan | nan |
| game_time | VARCHAR | 144 | 48.42 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## game_info_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_id | BIGINT | 58013 | 0.0 | 10500001 | 49800087 | 25797903.99975884 | 25900300.0 |
| game_date | DATE | 12598 | 0.0 | nan | nan | nan | nan |
| attendance | BIGINT | 15718 | 9.27 | 0 | 200049 | 15097.689157632944 | 16205.0 |
| game_time | VARCHAR | 144 | 48.42 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## game_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| season_id | BIGINT | 225 | 0.0 | 12005 | 42022 | 22941.630053928886 | 21997.0 |
| team_id_home | BIGINT | 63 | 0.0 | 45 | 1610616834 | 1609925696.4542062 | 1610612751.0 |
| team_abbreviation_home | VARCHAR | 97 | 0.0 | nan | nan | nan | nan |
| team_name_home | VARCHAR | 98 | 0.0 | nan | nan | nan | nan |
| game_id | BIGINT | 65642 | 0.0 | 10500001 | 49800087 | 25839395.15087901 | 26300040.5 |
| game_date | DATE | 12882 | 0.0 | nan | nan | nan | nan |
| matchup_home | VARCHAR | 2292 | 0.0 | nan | nan | nan | nan |
| wl_home | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| min | BIGINT | 11 | 0.0 | 0 | 365 | 220.9849029584717 | 240.0 |
| fgm_home | BIGINT | 64 | 0.02 | 4 | 84 | 39.661079705617944 | 40.0 |
| fga_home | BIGINT | 87 | 23.53 | 0 | 240 | 83.96471760135472 | 84.0 |
| fg_pct_home | BIGINT | 2 | 23.6 | 0 | 1 | 0.30702663901738714 | 0.0 |
| fg3m_home | BIGINT | 29 | 20.1 | 0 | 28 | 5.73309689966823 | 5.0 |
| fg3a_home | BIGINT | 69 | 28.43 | 0 | 77 | 17.734722547412783 | 16.0 |
| fg3_pct_home | BIGINT | 2 | 29.02 | 0 | 1 | 0.1517675087463244 | 0.0 |
| ftm_home | BIGINT | 61 | 0.02 | 0 | 61 | 20.69486179258221 | 20.0 |
| fta_home | BIGINT | 76 | 4.58 | 0 | 86 | 27.14339538299435 | 27.0 |
| ft_pct_home | BIGINT | 5 | 4.58 | 0 | 4 | 0.9930548903151643 | 1.0 |
| oreb_home | BIGINT | 37 | 28.82 | 0 | 44 | 12.105746388443018 | 12.0 |
| dreb_home | BIGINT | 48 | 28.91 | 3 | 56 | 31.408126526938407 | 31.0 |
| reb_home | BIGINT | 68 | 23.96 | 0 | 85 | 43.747039849337845 | 43.0 |
| ast_home | BIGINT | 50 | 24.08 | 0 | 60 | 23.931135501735657 | 24.0 |
| stl_home | BIGINT | 27 | 28.69 | 0 | 27 | 7.987225497735623 | 8.0 |
| blk_home | BIGINT | 24 | 28.35 | 0 | 23 | 5.313851387264803 | 5.0 |
| tov_home | BIGINT | 37 | 28.43 | 0 | 39 | 14.778305200195833 | 15.0 |
| pf_home | BIGINT | 55 | 4.35 | 0 | 122 | 22.384608033638074 | 22.0 |
| pts_home | BIGINT | 131 | 0.0 | 18 | 192 | 104.59809268456172 | 105.0 |
| plus_minus_home | BIGINT | 121 | 0.0 | -68 | 73 | 3.6314707047317265 | 4.0 |
| video_available_home | BIGINT | 2 | 0.0 | 0 | 1 | 0.20138021388745012 | 0.0 |
| team_id_away | BIGINT | 72 | 0.0 | 41 | 1610616834 | 1608944249.4706743 | 1610612751.0 |
| team_abbreviation_away | VARCHAR | 101 | 0.0 | nan | nan | nan | nan |
| team_name_away | VARCHAR | 101 | 0.0 | nan | nan | nan | nan |
| matchup_away | VARCHAR | 2292 | 0.0 | nan | nan | nan | nan |
| wl_away | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| fgm_away | BIGINT | 64 | 0.02 | 4 | 82 | 38.33956025537491 | 38.0 |
| fga_away | BIGINT | 89 | 23.53 | 0 | 149 | 83.73788225918916 | 83.0 |
| fg_pct_away | BIGINT | 3 | 23.6 | 0 | 4 | 0.22848084860327397 | 0.0 |
| fg3m_away | BIGINT | 32 | 20.1 | 0 | 35 | 5.635529878351066 | 5.0 |
| fg3a_away | BIGINT | 68 | 28.43 | 0 | 90 | 17.769310998063048 | 16.0 |
| fg3_pct_away | BIGINT | 2 | 28.85 | 0 | 1 | 0.1341912551924971 | 0.0 |
| ftm_away | BIGINT | 56 | 0.02 | 0 | 57 | 19.786710143381736 | 19.0 |
| fta_away | BIGINT | 70 | 4.58 | 0 | 91 | 26.0359526166225 | 25.0 |
| ft_pct_away | BIGINT | 5 | 4.58 | 0 | 5 | 0.9919694744236541 | 1.0 |
| oreb_away | BIGINT | 37 | 28.82 | 0 | 40 | 11.682439807383627 | 11.0 |
| dreb_away | BIGINT | 50 | 28.91 | 0 | 60 | 30.233804084606646 | 30.0 |
| reb_away | BIGINT | 68 | 23.96 | 0 | 90 | 42.10445339263177 | 42.0 |
| ast_away | BIGINT | 50 | 24.07 | 0 | 89 | 22.12505768343332 | 22.0 |
| stl_away | BIGINT | 26 | 28.69 | 0 | 27 | 7.849589848756729 | 8.0 |
| blk_away | BIGINT | 20 | 28.34 | 0 | 19 | 4.6813929755931625 | 4.0 |
| tov_away | BIGINT | 39 | 28.43 | 0 | 40 | 15.196560091957938 | 15.0 |
| pf_away | BIGINT | 61 | 4.34 | 0 | 115 | 23.100619515535666 | 23.0 |
| pts_away | BIGINT | 133 | 0.0 | 19 | 196 | 100.96662197982998 | 101.0 |
| plus_minus_away | BIGINT | 121 | 0.0 | -73 | 68 | -3.6314707047317265 | -4.0 |
| video_available_away | BIGINT | 2 | 0.0 | 0 | 1 | 0.20138021388745012 | 0.0 |
| season_type | VARCHAR | 5 | 0.0 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## game_summary

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_date_est | VARCHAR | 12610 | 0.0 | nan | nan | nan | nan |
| game_sequence | VARCHAR | 16 | 43.94 | nan | nan | nan | nan |
| game_id | VARCHAR | 58021 | 0.0 | nan | nan | nan | nan |
| game_status_id | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| game_status_text | VARCHAR | 5 | 44.72 | nan | nan | nan | nan |
| gamecode | VARCHAR | 58021 | 0.0 | nan | nan | nan | nan |
| home_team_id | VARCHAR | 63 | 0.0 | nan | nan | nan | nan |
| visitor_team_id | VARCHAR | 71 | 0.0 | nan | nan | nan | nan |
| season | VARCHAR | 77 | 0.0 | nan | nan | nan | nan |
| live_period | VARCHAR | 9 | 0.0 | nan | nan | nan | nan |
| live_pc_time | VARCHAR | 3 | 96.52 | nan | nan | nan | nan |
| natl_tv_broadcaster_abbreviation | VARCHAR | 20 | 89.33 | nan | nan | nan | nan |
| live_period_time_bcast | VARCHAR | 67 | 0.0 | nan | nan | nan | nan |
| wh_status | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## game_summary_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_date_est | DATE | 12598 | 0.0 | nan | nan | nan | nan |
| game_sequence | BIGINT | 16 | 43.94 | 0 | 15 | 4.249616305482228 | 4.0 |
| game_id | BIGINT | 58021 | 0.0 | 10500001 | 49800087 | 25804934.25744278 | 26200018.5 |
| game_status_id | BIGINT | 2 | 0.0 | 1 | 3 | 2.996730339012218 | 3.0 |
| game_status_text | VARCHAR | 5 | 44.72 | nan | nan | nan | nan |
| gamecode | VARCHAR | 58021 | 0.0 | nan | nan | nan | nan |
| home_team_id | BIGINT | 63 | 0.0 | 45 | 1610616834 | 1609864371.4911203 | 1610612751.0 |
| visitor_team_id | BIGINT | 71 | 0.0 | 41 | 1610616834 | 1608838862.1499398 | 1610612751.0 |
| season | BIGINT | 77 | 0.0 | 1946 | 2022 | 1994.5477026329374 | 1997.0 |
| live_period | BIGINT | 9 | 0.0 | 0 | 9 | 4.055618654276373 | 4.0 |
| live_pc_time | VARCHAR | 3 | 96.52 | nan | nan | nan | nan |
| natl_tv_broadcaster_abbreviation | VARCHAR | 20 | 89.33 | nan | nan | nan | nan |
| live_period_time_bcast | VARCHAR | 67 | 0.0 | nan | nan | nan | nan |
| wh_status | BIGINT | 1 | 0.0 | 1 | 1 | 1.0 | 1.0 |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## games

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_id | BIGINT | 70228 | 0.0 | 10500001 | 49900088 | 25710146.421541266 | 25400252.5 |
| season_id | BIGINT | 225 | 6.53 | 12005 | 42022 | 22941.630053928886 | 21997.0 |
| game_date | DATE | 12882 | 6.53 | nan | nan | nan | nan |
| home_team_id | BIGINT | 63 | 6.53 | 45 | 1610616834 | 1609925696.4542062 | 1610612751.0 |
| visitor_team_id | BIGINT | 72 | 6.53 | 41 | 1610616834 | 1608944249.4706743 | 1610612751.0 |
| home_pts | BIGINT | 131 | 6.53 | 18 | 192 | 104.59809268456172 | 105.0 |
| visitor_pts | BIGINT | 133 | 6.53 | 19 | 196 | 100.96662197982998 | 101.0 |
| home_wl | VARCHAR | 2 | 6.53 | nan | nan | nan | nan |
| visitor_wl | VARCHAR | 2 | 6.53 | nan | nan | nan | nan |
| season_type | VARCHAR | 4 | 6.53 | nan | nan | nan | nan |

## games_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_id | BIGINT | 70228 | 0.0 | 10500001 | 49900088 | 25710146.421541266 | 25400252.5 |
| season_id | BIGINT | 225 | 6.53 | 12005 | 42022 | 22941.630053928886 | 21997.0 |
| game_date | DATE | 12882 | 6.53 | nan | nan | nan | nan |
| home_team_id | BIGINT | 63 | 6.53 | 45 | 1610616834 | 1609925696.4542062 | 1610612751.0 |
| visitor_team_id | BIGINT | 72 | 6.53 | 41 | 1610616834 | 1608944249.4706743 | 1610612751.0 |
| home_pts | BIGINT | 131 | 6.53 | 18 | 192 | 104.59809268456172 | 105.0 |
| visitor_pts | BIGINT | 133 | 6.53 | 19 | 196 | 100.96662197982998 | 101.0 |
| home_wl | VARCHAR | 2 | 6.53 | nan | nan | nan | nan |
| visitor_wl | VARCHAR | 2 | 6.53 | nan | nan | nan | nan |
| season_type | VARCHAR | 4 | 6.53 | nan | nan | nan | nan |

## inactive_players

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_id | VARCHAR | 20424 | 0.0 | nan | nan | nan | nan |
| player_id | VARCHAR | 2233 | 0.0 | nan | nan | nan | nan |
| first_name | VARCHAR | 1140 | 0.0 | nan | nan | nan | nan |
| last_name | VARCHAR | 1438 | 0.0 | nan | nan | nan | nan |
| jersey_num | VARCHAR | 175 | 0.04 | nan | nan | nan | nan |
| team_id | VARCHAR | 32 | 0.0 | nan | nan | nan | nan |
| team_city | VARCHAR | 37 | 0.0 | nan | nan | nan | nan |
| team_name | VARCHAR | 41 | 0.0 | nan | nan | nan | nan |
| team_abbreviation | VARCHAR | 45 | 0.0 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## inactive_players_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_id | BIGINT | 25095 | 0.0 | 10500008 | 42200405 | 22363519.438883394 | 21700063.0 |
| player_id | BIGINT | 2483 | 0.0 | 0 | 1962935994 | 664491.9551052264 | 202695.0 |
| first_name | VARCHAR | 1140 | 0.0 | nan | nan | nan | nan |
| last_name | VARCHAR | 1438 | 0.0 | nan | nan | nan | nan |
| jersey_num | BIGINT | 78 | 0.04 | 0 | 99 | 18.663389258089115 | 14.0 |
| team_id | BIGINT | 42 | 0.0 | 12308 | 1610616834 | 1610495820.9124339 | 1610612751.0 |
| team_city | VARCHAR | 37 | 0.0 | nan | nan | nan | nan |
| team_name | VARCHAR | 41 | 0.0 | nan | nan | nan | nan |
| team_abbreviation | VARCHAR | 45 | 0.0 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## line_score

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_date_est | VARCHAR | 12610 | 0.0 | nan | nan | nan | nan |
| game_sequence | VARCHAR | 16 | 43.98 | nan | nan | nan | nan |
| game_id | VARCHAR | 58013 | 0.0 | nan | nan | nan | nan |
| team_id_home | VARCHAR | 67 | 0.0 | nan | nan | nan | nan |
| team_abbreviation_home | VARCHAR | 103 | 0.0 | nan | nan | nan | nan |
| team_city_name_home | VARCHAR | 76 | 0.0 | nan | nan | nan | nan |
| team_nickname_home | VARCHAR | 79 | 0.0 | nan | nan | nan | nan |
| team_wins_losses_home | VARCHAR | 2505 | 0.0 | nan | nan | nan | nan |
| pts_qtr1_home | VARCHAR | 57 | 1.73 | nan | nan | nan | nan |
| pts_qtr2_home | VARCHAR | 53 | 1.74 | nan | nan | nan | nan |
| pts_qtr3_home | VARCHAR | 55 | 1.8 | nan | nan | nan | nan |
| pts_qtr4_home | VARCHAR | 54 | 1.8 | nan | nan | nan | nan |
| pts_ot1_home | VARCHAR | 26 | 44.37 | nan | nan | nan | nan |
| pts_ot2_home | VARCHAR | 22 | 46.6 | nan | nan | nan | nan |
| pts_ot3_home | VARCHAR | 16 | 46.93 | nan | nan | nan | nan |
| pts_ot4_home | VARCHAR | 10 | 46.97 | nan | nan | nan | nan |
| pts_ot5_home | VARCHAR | 2 | 78.51 | nan | nan | nan | nan |
| pts_ot6_home | VARCHAR | 1 | 78.51 | nan | nan | nan | nan |
| pts_ot7_home | VARCHAR | 1 | 78.51 | nan | nan | nan | nan |
| pts_ot8_home | VARCHAR | 1 | 78.51 | nan | nan | nan | nan |
| pts_ot9_home | VARCHAR | 1 | 78.51 | nan | nan | nan | nan |
| pts_ot10_home | VARCHAR | 1 | 78.51 | nan | nan | nan | nan |
| pts_home | VARCHAR | 132 | 0.0 | nan | nan | nan | nan |
| team_id_away | VARCHAR | 75 | 0.0 | nan | nan | nan | nan |
| team_abbreviation_away | VARCHAR | 109 | 0.0 | nan | nan | nan | nan |
| team_city_name_away | VARCHAR | 84 | 0.0 | nan | nan | nan | nan |
| team_nickname_away | VARCHAR | 85 | 0.0 | nan | nan | nan | nan |
| team_wins_losses_away | VARCHAR | 2473 | 0.0 | nan | nan | nan | nan |
| pts_qtr1_away | VARCHAR | 50 | 1.74 | nan | nan | nan | nan |
| pts_qtr2_away | VARCHAR | 56 | 1.74 | nan | nan | nan | nan |
| pts_qtr3_away | VARCHAR | 55 | 1.8 | nan | nan | nan | nan |
| pts_qtr4_away | VARCHAR | 54 | 1.8 | nan | nan | nan | nan |
| pts_ot1_away | VARCHAR | 25 | 44.37 | nan | nan | nan | nan |
| pts_ot2_away | VARCHAR | 20 | 46.6 | nan | nan | nan | nan |
| pts_ot3_away | VARCHAR | 18 | 46.93 | nan | nan | nan | nan |
| pts_ot4_away | VARCHAR | 10 | 46.97 | nan | nan | nan | nan |
| pts_ot5_away | VARCHAR | 2 | 78.51 | nan | nan | nan | nan |
| pts_ot6_away | VARCHAR | 1 | 78.51 | nan | nan | nan | nan |
| pts_ot7_away | VARCHAR | 1 | 78.51 | nan | nan | nan | nan |
| pts_ot8_away | VARCHAR | 1 | 78.51 | nan | nan | nan | nan |
| pts_ot9_away | VARCHAR | 1 | 78.51 | nan | nan | nan | nan |
| pts_ot10_away | VARCHAR | 1 | 78.51 | nan | nan | nan | nan |
| pts_away | VARCHAR | 130 | 0.0 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## line_score_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_date_est | DATE | 12598 | 0.0 | nan | nan | nan | nan |
| game_sequence | BIGINT | 16 | 43.98 | 0 | 15 | 4.252759755235079 | 4.0 |
| game_id | BIGINT | 58013 | 0.0 | 10500001 | 49800087 | 25797903.99975884 | 25900300.0 |
| team_id_home | BIGINT | 67 | 0.0 | 41 | 1610616834 | 1609502967.6452725 | 1610612751.0 |
| team_abbreviation_home | VARCHAR | 103 | 0.0 | nan | nan | nan | nan |
| team_city_name_home | VARCHAR | 76 | 0.0 | nan | nan | nan | nan |
| team_nickname_home | VARCHAR | 79 | 0.0 | nan | nan | nan | nan |
| team_wins_losses_home | VARCHAR | 2505 | 0.0 | nan | nan | nan | nan |
| pts_qtr1_home | BIGINT | 52 | 1.73 | 2 | 55 | 25.91796525793616 | 26.0 |
| pts_qtr2_home | BIGINT | 52 | 1.74 | 3 | 60 | 25.57859396914446 | 25.0 |
| pts_qtr3_home | BIGINT | 52 | 1.8 | 0 | 57 | 25.624280802694358 | 25.0 |
| pts_qtr4_home | BIGINT | 52 | 1.8 | 0 | 53 | 25.633022856040274 | 25.0 |
| pts_ot1_home | BIGINT | 26 | 44.37 | 0 | 25 | 1.0423608100575958 | 0.0 |
| pts_ot2_home | BIGINT | 22 | 46.6 | 0 | 22 | 0.1506031868911683 | 0.0 |
| pts_ot3_home | BIGINT | 16 | 46.93 | 0 | 19 | 0.023012009087958456 | 0.0 |
| pts_ot4_home | BIGINT | 10 | 46.97 | 0 | 17 | 0.005067732189845044 | 0.0 |
| pts_ot5_home | BIGINT | 2 | 78.51 | 0 | 16 | 0.0012824623276691247 | 0.0 |
| pts_ot6_home | BIGINT | 1 | 78.51 | 0 | 0 | 0.0 | 0.0 |
| pts_ot7_home | BIGINT | 1 | 78.51 | 0 | 0 | 0.0 | 0.0 |
| pts_ot8_home | BIGINT | 1 | 78.51 | 0 | 0 | 0.0 | 0.0 |
| pts_ot9_home | BIGINT | 1 | 78.51 | 0 | 0 | 0.0 | 0.0 |
| pts_ot10_home | BIGINT | 1 | 78.51 | 0 | 0 | 0.0 | 0.0 |
| pts_home | BIGINT | 132 | 0.0 | 19 | 196 | 102.96656503539869 | 103.0 |
| team_id_away | BIGINT | 75 | 0.0 | 41 | 1610616834 | 1609197789.3403096 | 1610612751.0 |
| team_abbreviation_away | VARCHAR | 109 | 0.0 | nan | nan | nan | nan |
| team_city_name_away | VARCHAR | 84 | 0.0 | nan | nan | nan | nan |
| team_nickname_away | VARCHAR | 85 | 0.0 | nan | nan | nan | nan |
| team_wins_losses_away | VARCHAR | 2473 | 0.0 | nan | nan | nan | nan |
| pts_qtr1_away | BIGINT | 50 | 1.74 | 2 | 95 | 25.79866065950248 | 26.0 |
| pts_qtr2_away | BIGINT | 55 | 1.74 | 2 | 60 | 25.500192847124826 | 25.0 |
| pts_qtr3_away | BIGINT | 53 | 1.8 | 0 | 59 | 25.53654814321048 | 25.0 |
| pts_qtr4_away | BIGINT | 54 | 1.8 | 0 | 58 | 25.584384373848824 | 25.0 |
| pts_ot1_away | BIGINT | 25 | 44.37 | 0 | 24 | 1.034185916888586 | 0.0 |
| pts_ot2_away | BIGINT | 20 | 46.6 | 0 | 21 | 0.14986129927101477 | 0.0 |
| pts_ot3_away | BIGINT | 18 | 46.93 | 0 | 20 | 0.024407659850697826 | 0.0 |
| pts_ot4_away | BIGINT | 10 | 46.97 | 0 | 20 | 0.005977325146996719 | 0.0 |
| pts_ot5_away | BIGINT | 2 | 78.51 | 0 | 17 | 0.0013626162231484451 | 0.0 |
| pts_ot6_away | BIGINT | 1 | 78.51 | 0 | 0 | 0.0 | 0.0 |
| pts_ot7_away | BIGINT | 1 | 78.51 | 0 | 0 | 0.0 | 0.0 |
| pts_ot8_away | BIGINT | 1 | 78.51 | 0 | 0 | 0.0 | 0.0 |
| pts_ot9_away | BIGINT | 1 | 78.51 | 0 | 0 | 0.0 | 0.0 |
| pts_ot10_away | BIGINT | 1 | 78.51 | 0 | 0 | 0.0 | 0.0 |
| pts_away | BIGINT | 130 | 0.0 | 18 | 186 | 102.6175391452638 | 103.0 |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## officials

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_id | VARCHAR | 23575 | 0.0 | nan | nan | nan | nan |
| official_id | VARCHAR | 235 | 0.0 | nan | nan | nan | nan |
| first_name | VARCHAR | 167 | 0.0 | nan | nan | nan | nan |
| last_name | VARCHAR | 197 | 0.0 | nan | nan | nan | nan |
| jersey_num | VARCHAR | 239 | 0.27 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## officials_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_id | BIGINT | 23575 | 0.0 | 10500001 | 49600088 | 22012151.698707923 | 21300764.0 |
| official_id | BIGINT | 235 | 0.0 | 1 | 1962937777 | 695409.0093700244 | 2002.0 |
| first_name | VARCHAR | 167 | 0.0 | nan | nan | nan | nan |
| last_name | VARCHAR | 197 | 0.0 | nan | nan | nan | nan |
| jersey_num | BIGINT | 155 | 0.27 | 0 | 166 | 39.341857278083104 | 38.0 |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## other_stats

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_id | VARCHAR | 28261 | 0.0 | nan | nan | nan | nan |
| league_id | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |
| team_id_home | VARCHAR | 49 | 0.0 | nan | nan | nan | nan |
| team_abbreviation_home | VARCHAR | 58 | 0.0 | nan | nan | nan | nan |
| team_city_home | VARCHAR | 54 | 0.0 | nan | nan | nan | nan |
| pts_paint_home | VARCHAR | 47 | 0.0 | nan | nan | nan | nan |
| pts_2nd_chance_home | VARCHAR | 38 | 0.0 | nan | nan | nan | nan |
| pts_fb_home | VARCHAR | 53 | 0.0 | nan | nan | nan | nan |
| largest_lead_home | VARCHAR | 61 | 0.0 | nan | nan | nan | nan |
| lead_changes | VARCHAR | 37 | 0.0 | nan | nan | nan | nan |
| times_tied | VARCHAR | 29 | 0.0 | nan | nan | nan | nan |
| team_turnovers_home | VARCHAR | 7 | 0.01 | nan | nan | nan | nan |
| total_turnovers_home | VARCHAR | 34 | 1.12 | nan | nan | nan | nan |
| team_rebounds_home | VARCHAR | 25 | 7.07 | nan | nan | nan | nan |
| pts_off_to_home | VARCHAR | 45 | 7.51 | nan | nan | nan | nan |
| team_id_away | VARCHAR | 45 | 0.0 | nan | nan | nan | nan |
| team_abbreviation_away | VARCHAR | 56 | 0.0 | nan | nan | nan | nan |
| team_city_away | VARCHAR | 50 | 0.0 | nan | nan | nan | nan |
| pts_paint_away | VARCHAR | 44 | 0.0 | nan | nan | nan | nan |
| pts_2nd_chance_away | VARCHAR | 38 | 0.0 | nan | nan | nan | nan |
| pts_fb_away | VARCHAR | 52 | 0.0 | nan | nan | nan | nan |
| largest_lead_away | VARCHAR | 62 | 0.0 | nan | nan | nan | nan |
| team_turnovers_away | VARCHAR | 7 | 0.01 | nan | nan | nan | nan |
| total_turnovers_away | VARCHAR | 32 | 1.12 | nan | nan | nan | nan |
| team_rebounds_away | VARCHAR | 25 | 7.07 | nan | nan | nan | nan |
| pts_off_to_away | VARCHAR | 44 | 7.51 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## other_stats_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_id | BIGINT | 28261 | 0.0 | 11000001 | 49800086 | 23144513.48763751 | 21400309.0 |
| league_id | BIGINT | 1 | 0.0 | 0 | 0 | 0.0 | 0.0 |
| team_id_home | BIGINT | 49 | 0.0 | 41 | 1610616834 | 1608618800.5179865 | 1610612751.0 |
| team_abbreviation_home | VARCHAR | 58 | 0.0 | nan | nan | nan | nan |
| team_city_home | VARCHAR | 54 | 0.0 | nan | nan | nan | nan |
| pts_paint_home | BIGINT | 47 | 0.0 | 8 | 120 | 41.90449577305366 | 42.0 |
| pts_2nd_chance_home | BIGINT | 38 | 0.0 | 0 | 37 | 13.24388949807223 | 13.0 |
| pts_fb_home | BIGINT | 53 | 0.0 | 0 | 106 | 13.006119344911747 | 12.0 |
| largest_lead_home | BIGINT | 61 | 0.0 | 0 | 70 | 11.94938275971844 | 10.0 |
| lead_changes | BIGINT | 37 | 0.0 | 0 | 40 | 6.075377595415797 | 5.0 |
| times_tied | BIGINT | 29 | 0.0 | 0 | 29 | 5.098086378267483 | 4.0 |
| team_turnovers_home | BIGINT | 7 | 0.01 | 0 | 6 | 0.6287452686688599 | 0.0 |
| total_turnovers_home | BIGINT | 34 | 1.12 | 1 | 34 | 14.56419245215525 | 14.0 |
| team_rebounds_home | BIGINT | 25 | 7.07 | 0 | 27 | 8.456971034902752 | 8.0 |
| pts_off_to_home | BIGINT | 45 | 7.51 | 0 | 47 | 15.227550864310846 | 15.0 |
| team_id_away | BIGINT | 45 | 0.0 | 41 | 1610616834 | 1609416382.0656502 | 1610612752.0 |
| team_abbreviation_away | VARCHAR | 56 | 0.0 | nan | nan | nan | nan |
| team_city_away | VARCHAR | 50 | 0.0 | nan | nan | nan | nan |
| pts_paint_away | BIGINT | 44 | 0.0 | 8 | 108 | 41.658307099147535 | 42.0 |
| pts_2nd_chance_away | BIGINT | 38 | 0.0 | 0 | 38 | 13.328145449400445 | 13.0 |
| pts_fb_away | BIGINT | 52 | 0.0 | 0 | 107 | 12.882423685048282 | 12.0 |
| largest_lead_away | BIGINT | 62 | 0.0 | 0 | 78 | 11.641045594425384 | 10.0 |
| team_turnovers_away | BIGINT | 7 | 0.01 | 0 | 7 | 0.6333439456648625 | 0.0 |
| total_turnovers_away | BIGINT | 32 | 1.12 | 2 | 33 | 14.595421212663208 | 14.0 |
| team_rebounds_away | BIGINT | 25 | 7.07 | 0 | 24 | 8.461005595097628 | 8.0 |
| pts_off_to_away | BIGINT | 44 | 7.51 | 0 | 44 | 15.329050022946305 | 15.0 |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## play_by_play_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_id | BIGINT | 1 | 0.0 | 42200405 | 42200405 | 42200405.0 | 42200405.0 |
| action_number | BIGINT | 463 | 0.0 | 2 | 649 | 328.4349593495935 | 330.5 |
| clock | VARCHAR | 282 | 0.0 | nan | nan | nan | nan |
| period | INTEGER | 4 | 0.0 | 1 | 4 | 2.4430894308943087 | 2.0 |
| team_id | BIGINT | 3 | 0.0 | 0 | 1610612748 | 1473121413.5772357 | 1610612743.0 |
| team_tricode | VARCHAR | 3 | 0.0 | nan | nan | nan | nan |
| person_id | BIGINT | 23 | 0.0 | 0 | 1610612748 | 108944875.74593496 | 1628389.0 |
| player_name | VARCHAR | 20 | 0.0 | nan | nan | nan | nan |
| player_name_i | VARCHAR | 20 | 0.0 | nan | nan | nan | nan |
| x_legacy | DOUBLE | 126 | 0.0 | -232.0 | 238.0 | -1.91869918699187 | 0.0 |
| y_legacy | DOUBLE | 116 | 0.0 | -6.0 | 666.0 | 31.640243902439025 | 0.0 |
| shot_distance | DOUBLE | 30 | 0.0 | 0.0 | 67.0 | 4.203252032520325 | 0.0 |
| shot_result | VARCHAR | 3 | 0.0 | nan | nan | nan | nan |
| is_field_goal | INTEGER | 2 | 0.0 | 0 | 1 | 0.36585365853658536 | 0.0 |
| score_home | VARCHAR | 53 | 0.0 | nan | nan | nan | nan |
| score_away | VARCHAR | 49 | 0.0 | nan | nan | nan | nan |
| points_total | INTEGER | 99 | 0.0 | 0 | 183 | 20.443089430894307 | 0.0 |
| location | VARCHAR | 3 | 0.0 | nan | nan | nan | nan |
| description | VARCHAR | 456 | 0.0 | nan | nan | nan | nan |
| action_type | VARCHAR | 13 | 0.0 | nan | nan | nan | nan |
| sub_type | VARCHAR | 60 | 0.0 | nan | nan | nan | nan |
| video_available | INTEGER | 2 | 0.0 | 0 | 1 | 0.8556910569105691 | 1.0 |
| shot_value | INTEGER | 3 | 0.0 | 0 | 3 | 0.9166666666666666 | 0.0 |
| action_id | INTEGER | 492 | 0.0 | 1 | 492 | 246.5 | 246.5 |

## player

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| id | VARCHAR | 5116 | 0.0 | nan | nan | nan | nan |
| full_name | VARCHAR | 5075 | 0.0 | nan | nan | nan | nan |
| first_name | VARCHAR | 1702 | 0.0 | nan | nan | nan | nan |
| last_name | VARCHAR | 3061 | 0.0 | nan | nan | nan | nan |
| is_active | VARCHAR | 4 | 0.0 | nan | nan | nan | nan |
| filename | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |

## player_game_stats_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_id | BIGINT | 37475 | 0.0 | 20000001 | 49900088 | 23521308.004326213 | 21500761.0 |
| team_id | BIGINT | 33 | 0.0 | 1610612737 | 1610612766 | 1610612751.5004585 | 1610612752.0 |
| player_id | BIGINT | 2811 | 0.0 | 2 | 1643141 | 386742.09249147953 | 101153.0 |
| player_name | VARCHAR | 3941 | 0.0 | nan | nan | nan | nan |
| start_position | VARCHAR | 0 | 100.0 | nan | nan | nan | nan |
| comment | VARCHAR | 0 | 100.0 | nan | nan | nan | nan |
| min | BIGINT | 62 | 0.0 | 0 | 64 | 22.875396764508157 | 23.0 |
| fgm | INTEGER | 27 | 0.0 | 0 | 28 | 3.660067903457979 | 3.0 |
| fga | INTEGER | 45 | 0.0 | 0 | 50 | 8.040994339644723 | 7.0 |
| fg_pct | DOUBLE | 303 | 0.0 | 0.0 | 1.0 | 0.41682453418773596 | 0.429 |
| fg3m | INTEGER | 17 | 0.0 | 0 | 14 | 0.7748289085123785 | 0.0 |
| fg3a | INTEGER | 26 | 0.0 | 0 | 24 | 2.1705856575725617 | 1.0 |
| fg3_pct | DOUBLE | 104 | 0.0 | 0.0 | 1.0 | 0.19755338977651543 | 0.0 |
| ftm | INTEGER | 27 | 0.0 | 0 | 26 | 1.7582678506644058 | 1.0 |
| fta | INTEGER | 32 | 0.0 | 0 | 39 | 2.3159669350990137 | 2.0 |
| ft_pct | DOUBLE | 170 | 0.0 | 0.0 | 1.0 | 0.4369577222304061 | 0.5 |
| oreb | INTEGER | 21 | 0.0 | 0 | 18 | 1.0781773994093882 | 1.0 |
| dreb | INTEGER | 26 | 0.0 | 0 | 25 | 3.0448472302228904 | 2.0 |
| reb | INTEGER | 32 | 0.0 | 0 | 33 | 4.123024629632279 | 3.0 |
| ast | INTEGER | 27 | 0.0 | 0 | 25 | 2.1767102322006986 | 1.0 |
| stl | INTEGER | 13 | 0.0 | 0 | 11 | 0.7397588920111361 | 0.0 |
| blk | INTEGER | 16 | 0.0 | 0 | 13 | 0.47404727755505943 | 0.0 |
| tov | INTEGER | 16 | 0.0 | 0 | 14 | 1.334113100478133 | 1.0 |
| pf | INTEGER | 9 | 0.0 | 0 | 7 | 2.0277413322965336 | 2.0 |
| pts | INTEGER | 69 | 0.0 | 0 | 81 | 9.853232566092743 | 8.0 |
| plus_minus | DOUBLE | 124 | 0.0 | -58.0 | 57.0 | -0.00028737388382553153 | 0.0 |

## player_gold

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| id | BIGINT | 5104 | 0.0 | 2 | 1643141 | 402814.5127351097 | 77771.5 |
| full_name | VARCHAR | 5064 | 0.0 | nan | nan | nan | nan |
| first_name | VARCHAR | 1568 | 5.47 | nan | nan | nan | nan |
| last_name | VARCHAR | 2904 | 5.35 | nan | nan | nan | nan |
| is_active | BIGINT | 2 | 5.35 | 0 | 1 | 0.1204719519768164 | 0.0 |

## player_gold_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| id | BIGINT | 5104 | 0.0 | 2 | 1643141 | 402814.5127351097 | 77771.5 |
| full_name | VARCHAR | 5064 | 0.0 | nan | nan | nan | nan |
| first_name | VARCHAR | 1568 | 5.47 | nan | nan | nan | nan |
| last_name | VARCHAR | 2904 | 5.35 | nan | nan | nan | nan |
| is_active | BIGINT | 2 | 5.35 | 0 | 1 | 0.1204719519768164 | 0.0 |

## player_season_averages

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| player_id | BIGINT | 2828 | 0.0 | 2 | 1643141 | 377422.5025873566 | 101141.0 |
| player_name | VARCHAR | 2816 | 0.0 | nan | nan | nan | nan |
| season_id | BIGINT | 50 | 7.97 | 21996 | 42022 | 27660.440901976697 | 22016.0 |
| games_played | BIGINT | 228 | 0.0 | 1 | 286 | 41.02603360896239 | 39.0 |
| ppg | DOUBLE | 9631 | 0.0 | 0.0 | 37.4 | 8.145038152752463 | 6.538461538461538 |
| rpg | DOUBLE | 7487 | 0.0 | 0.0 | 17.5 | 3.523086191527466 | 2.9411764705882355 |
| apg | DOUBLE | 6158 | 0.0 | 0.0 | 13.272727272727273 | 1.7774743032189628 | 1.1666666666666667 |
| spg | DOUBLE | 3187 | 0.0 | 0.0 | 4.0 | 0.6237335445793609 | 0.5384615384615384 |
| bpg | DOUBLE | 3030 | 0.0 | 0.0 | 4.0 | 0.4012346954679073 | 0.25 |
| topg | DOUBLE | 4576 | 0.0 | 0.0 | 6.25 | 1.137035776345845 | 0.9444444444444444 |
| fg_pct | DOUBLE | 8486 | 1.17 | 0.0 | 1.0 | 0.43375573042874194 | 0.4369602763385147 |
| fg3_pct | DOUBLE | 3617 | 17.07 | 0.0 | 1.0 | 0.2897469865555215 | 0.3294908422474697 |
| ft_pct | DOUBLE | 4522 | 7.66 | 0.0 | 1.0 | 0.7304984492908204 | 0.7526212725024048 |
| avg_game_score | DOUBLE | 13943 | 0.0 | -5.1 | 29.857142857142858 | 6.120585186747539 | 4.996153846153846 |

## player_season_stats_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| player_id | BIGINT | 2615 | 0.0 | 2 | 1643141 | 424628.2735687172 | 200764.0 |
| player_name | VARCHAR | 2605 | 0.0 | nan | nan | nan | nan |
| team_id | BIGINT | 30 | 0.0 | 1610612737 | 1610612766 | 1610612751.3032084 | 1610612751.0 |
| team_abbreviation | VARCHAR | 30 | 0.0 | nan | nan | nan | nan |
| season_id | BIGINT | 59 | 0.0 | 21996 | 42024 | 26227.22427330872 | 22016.0 |
| season_type | VARCHAR | 2 | 0.0 | nan | nan | nan | nan |
| games_played | BIGINT | 78 | 0.0 | 5 | 82 | 39.56518121782538 | 35.0 |
| minutes_played | DOUBLE | 3040 | 0.0 | 2.0 | 3443.0 | 909.3306640320316 | 616.0 |
| fgm | HUGEINT | 775 | 0.0 | 0 | 978 | 145.61562061255265 | 83.0 |
| fga | HUGEINT | 1491 | 0.0 | 0 | 2173 | 319.7275232697208 | 189.0 |
| fg_pct | DOUBLE | 8864 | 0.0 | 0.0 | 1.0 | 0.44078385299125983 | 0.43902439024390244 |
| fg3m | HUGEINT | 280 | 0.0 | 0 | 402 | 30.83277000675992 | 10.0 |
| fg3a | HUGEINT | 633 | 0.0 | 0 | 1028 | 86.3021163746035 | 31.0 |
| fg3_pct | DOUBLE | 3636 | 0.0 | 0.0 | 1.0 | 0.25732878944300513 | 0.3125 |
| ftm | HUGEINT | 561 | 0.0 | 0 | 756 | 69.92449690603713 | 34.0 |
| fta | HUGEINT | 681 | 0.0 | 0 | 972 | 92.0818990172118 | 47.0 |
| ft_pct | DOUBLE | 4496 | 0.0 | 0.0 | 1.0 | 0.7116657611106575 | 0.75 |
| oreb | HUGEINT | 331 | 0.0 | 0 | 443 | 42.853153762154854 | 22.0 |
| dreb | HUGEINT | 701 | 0.0 | 0 | 894 | 121.07581509021892 | 75.0 |
| reb | HUGEINT | 918 | 0.0 | 0 | 1247 | 163.92896885237377 | 100.0 |
| ast | HUGEINT | 679 | 0.0 | 0 | 925 | 86.59783682595808 | 42.0 |
| stl | HUGEINT | 195 | 0.0 | 0 | 229 | 29.415163018043785 | 18.0 |
| blk | HUGEINT | 226 | 0.0 | 0 | 294 | 18.856637720347354 | 8.0 |
| tov | HUGEINT | 324 | 0.0 | 0 | 464 | 53.030315636212364 | 32.0 |
| pf | HUGEINT | 320 | 0.0 | 0 | 371 | 80.50746191045708 | 59.0 |
| pts | HUGEINT | 1861 | 0.0 | 0 | 2832 | 391.98850813790233 | 223.0 |
| plus_minus | DOUBLE | 1145 | 0.0 | -798.0 | 1072.0 | 1.1022307732307213 | -9.0 |
| ts_pct | DOUBLE | 17076 | 0.0 | 0.0 | 1.3333333333333333 | 0.523306953452553 | 0.5302986034009233 |
| efg_pct | DOUBLE | 10290 | 0.0 | 0.0 | 1.3333333333333333 | 0.4874747818287215 | 0.492 |

## player_splits_raw

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| season_id | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |
| season_type | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |
| player_id | BIGINT | 1 | 0.0 | 2544 | 2544 | 2544.0 | 2544.0 |
| player_name | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |
| team_id | BIGINT | 0 | 100.0 | nan | nan | nan | nan |
| team_abbreviation | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |
| split_type | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |
| split_category | VARCHAR | 6 | 0.0 | nan | nan | nan | nan |
| split_value | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |
| games_played | BIGINT | 6 | 0.0 | 10 | 70 | 22.666666666666668 | 13.5 |
| wins | BIGINT | 4 | 0.0 | 3 | 44 | 10.666666666666666 | 4.0 |
| losses | BIGINT | 6 | 0.0 | 7 | 26 | 12.0 | 9.5 |
| win_pct | DOUBLE | 5 | 0.0 | 0.25 | 0.629 | 0.353 | 0.3165 |
| minutes | DOUBLE | 6 | 0.0 | 1.72 | 2444.4466666666667 | 418.15277777777766 | 13.998333333333333 |
| fgm | BIGINT | 6 | 0.0 | 1 | 651 | 113.66666666666667 | 7.5 |
| fga | BIGINT | 6 | 0.0 | 5 | 1270 | 221.66666666666666 | 13.0 |
| fg_pct | DOUBLE | 6 | 0.0 | 0.2 | 0.625 | 0.45250000000000007 | 0.5065 |
| fg3m | BIGINT | 5 | 0.0 | 0 | 149 | 27.0 | 3.0 |
| fg3a | BIGINT | 6 | 0.0 | 4 | 396 | 72.83333333333333 | 8.5 |
| fg3_pct | DOUBLE | 5 | 0.0 | 0.0 | 0.467 | 0.24416666666666667 | 0.2715 |
| ftm | BIGINT | 3 | 0.0 | 1 | 259 | 44.333333333333336 | 1.5 |
| fta | BIGINT | 3 | 0.0 | 2 | 331 | 57.166666666666664 | 2.5 |
| ft_pct | DOUBLE | 3 | 0.0 | 0.5 | 0.782 | 0.6026666666666667 | 0.5835 |
| oreb | BIGINT | 3 | 0.0 | 1 | 72 | 13.166666666666666 | 1.5 |
| dreb | BIGINT | 5 | 0.0 | 1 | 474 | 81.33333333333333 | 3.0 |
| reb | BIGINT | 5 | 0.0 | 2 | 546 | 94.5 | 4.5 |
| ast | BIGINT | 3 | 0.0 | 0 | 575 | 96.5 | 1.0 |
| stl | BIGINT | 3 | 0.0 | 0 | 70 | 12.166666666666666 | 1.0 |
| blk | BIGINT | 2 | 0.0 | 0 | 39 | 6.5 | 0.0 |
| tov | BIGINT | 4 | 0.0 | 0 | 260 | 44.166666666666664 | 1.0 |
| pf | BIGINT | 3 | 0.0 | 1 | 99 | 17.833333333333332 | 2.0 |
| pts | BIGINT | 6 | 0.0 | 3 | 1710 | 298.6666666666667 | 19.5 |
| plus_minus | BIGINT | 6 | 0.0 | -54 | 31 | 0.6666666666666666 | 3.0 |
| efg_pct | DOUBLE | 0 | 100.0 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## team

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| id | VARCHAR | 30 | 0.0 | nan | nan | nan | nan |
| full_name | VARCHAR | 30 | 0.0 | nan | nan | nan | nan |
| abbreviation | VARCHAR | 30 | 0.0 | nan | nan | nan | nan |
| nickname | VARCHAR | 30 | 0.0 | nan | nan | nan | nan |
| city | VARCHAR | 29 | 0.0 | nan | nan | nan | nan |
| state | VARCHAR | 23 | 0.0 | nan | nan | nan | nan |
| year_founded | VARCHAR | 15 | 0.0 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## team_details

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| team_id | VARCHAR | 25 | 0.0 | nan | nan | nan | nan |
| abbreviation | VARCHAR | 25 | 0.0 | nan | nan | nan | nan |
| nickname | VARCHAR | 25 | 0.0 | nan | nan | nan | nan |
| yearfounded | VARCHAR | 14 | 0.0 | nan | nan | nan | nan |
| city | VARCHAR | 24 | 0.0 | nan | nan | nan | nan |
| arena | VARCHAR | 24 | 0.0 | nan | nan | nan | nan |
| arenacapacity | VARCHAR | 14 | 36.0 | nan | nan | nan | nan |
| owner | VARCHAR | 25 | 0.0 | nan | nan | nan | nan |
| generalmanager | VARCHAR | 25 | 0.0 | nan | nan | nan | nan |
| headcoach | VARCHAR | 24 | 4.0 | nan | nan | nan | nan |
| dleagueaffiliation | VARCHAR | 24 | 0.0 | nan | nan | nan | nan |
| facebook | VARCHAR | 25 | 0.0 | nan | nan | nan | nan |
| instagram | VARCHAR | 25 | 0.0 | nan | nan | nan | nan |
| twitter | VARCHAR | 25 | 0.0 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## team_details_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| team_id | BIGINT | 25 | 0.0 | 1610612737 | 1610612766 | 1610612752.92 | 1610612754.0 |
| abbreviation | VARCHAR | 25 | 0.0 | nan | nan | nan | nan |
| nickname | VARCHAR | 25 | 0.0 | nan | nan | nan | nan |
| yearfounded | BIGINT | 14 | 0.0 | 1946 | 1995 | 1969.52 | 1970.0 |
| city | VARCHAR | 24 | 0.0 | nan | nan | nan | nan |
| arena | VARCHAR | 24 | 0.0 | nan | nan | nan | nan |
| arenacapacity | BIGINT | 14 | 36.0 | 17500 | 21711 | 19039.4375 | 19043.0 |
| owner | VARCHAR | 25 | 0.0 | nan | nan | nan | nan |
| generalmanager | VARCHAR | 25 | 0.0 | nan | nan | nan | nan |
| headcoach | VARCHAR | 24 | 4.0 | nan | nan | nan | nan |
| dleagueaffiliation | VARCHAR | 24 | 0.0 | nan | nan | nan | nan |
| facebook | VARCHAR | 25 | 0.0 | nan | nan | nan | nan |
| instagram | VARCHAR | 25 | 0.0 | nan | nan | nan | nan |
| twitter | VARCHAR | 25 | 0.0 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## team_game_stats

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_id | BIGINT | 62398 | 0.0 | 10500001 | 49900088 | 25710146.421541266 | 25400252.5 |
| team_id | BIGINT | 74 | 6.53 | 41 | 1610616834 | 1609434972.9624403 | 1610612751.0 |
| season_id | BIGINT | 254 | 6.53 | 12005 | 42022 | 22941.630053928886 | 21997.0 |
| game_date | DATE | 13903 | 6.53 | nan | nan | nan | nan |
| is_home | BOOLEAN | 2 | 0.0 | nan | nan | nan | nan |
| pts | BIGINT | 155 | 6.53 | 18 | 196 | 102.78235733219584 | 103.0 |
| fgm | BIGINT | 71 | 6.55 | 4 | 84 | 39.00031998049643 | 39.0 |
| fga | BIGINT | 95 | 28.53 | 0 | 240 | 83.85129993027194 | 84.0 |
| fg_pct | BIGINT | 3 | 28.59 | 0 | 4 | 0.2677533522755595 | 0.0 |
| fg3m | BIGINT | 30 | 25.32 | 0 | 35 | 5.684313389009648 | 5.0 |
| fg3a | BIGINT | 65 | 33.1 | 0 | 90 | 17.752016772737914 | 16.0 |
| fg3_pct | BIGINT | 2 | 33.58 | 0 | 1 | 0.14296892585724547 | 0.0 |
| ftm | BIGINT | 59 | 6.55 | 0 | 61 | 20.240775589501354 | 20.0 |
| fta | BIGINT | 75 | 10.81 | 0 | 91 | 26.589673999808422 | 26.0 |
| ft_pct | BIGINT | 6 | 10.81 | 0 | 5 | 0.9925121737047976 | 1.0 |
| oreb | BIGINT | 39 | 33.47 | 0 | 44 | 11.894093097913323 | 12.0 |
| dreb | BIGINT | 45 | 33.56 | 0 | 60 | 30.820959014197697 | 31.0 |
| reb | BIGINT | 73 | 28.92 | 0 | 90 | 42.92571371331263 | 43.0 |
| ast | BIGINT | 52 | 29.03 | 0 | 89 | 23.02806035434098 | 23.0 |
| stl | BIGINT | 29 | 33.34 | 0 | 27 | 7.918407673246176 | 8.0 |
| blk | BIGINT | 24 | 33.02 | 0 | 23 | 4.997618819827577 | 5.0 |
| tov | BIGINT | 41 | 33.11 | 0 | 40 | 14.987430420298647 | 15.0 |
| pf | BIGINT | 62 | 10.59 | 0 | 122 | 22.742628029018054 | 22.0 |
| plus_minus | BIGINT | 109 | 6.53 | -73 | 73 | 0.0 | 0.0 |

## team_game_stats_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| game_id | BIGINT | 62398 | 0.0 | 10500001 | 49900088 | 25710146.421541266 | 25400252.5 |
| team_id | BIGINT | 74 | 6.53 | 41 | 1610616834 | 1609434972.9624403 | 1610612751.0 |
| season_id | BIGINT | 254 | 6.53 | 12005 | 42022 | 22941.630053928886 | 21997.0 |
| game_date | DATE | 13903 | 6.53 | nan | nan | nan | nan |
| is_home | BOOLEAN | 2 | 0.0 | nan | nan | nan | nan |
| pts | BIGINT | 155 | 6.53 | 18 | 196 | 102.78235733219584 | 103.0 |
| fgm | BIGINT | 71 | 6.55 | 4 | 84 | 39.00031998049643 | 39.0 |
| fga | BIGINT | 95 | 28.53 | 0 | 240 | 83.85129993027194 | 84.0 |
| fg_pct | BIGINT | 3 | 28.59 | 0 | 4 | 0.2677533522755595 | 0.0 |
| fg3m | BIGINT | 30 | 25.32 | 0 | 35 | 5.684313389009648 | 5.0 |
| fg3a | BIGINT | 65 | 33.1 | 0 | 90 | 17.752016772737914 | 16.0 |
| fg3_pct | BIGINT | 2 | 33.58 | 0 | 1 | 0.14296892585724547 | 0.0 |
| ftm | BIGINT | 59 | 6.55 | 0 | 61 | 20.240775589501354 | 20.0 |
| fta | BIGINT | 75 | 10.81 | 0 | 91 | 26.589673999808422 | 26.0 |
| ft_pct | BIGINT | 6 | 10.81 | 0 | 5 | 0.9925121737047976 | 1.0 |
| oreb | BIGINT | 39 | 33.47 | 0 | 44 | 11.894093097913323 | 12.0 |
| dreb | BIGINT | 45 | 33.56 | 0 | 60 | 30.820959014197697 | 31.0 |
| reb | BIGINT | 73 | 28.92 | 0 | 90 | 42.92571371331263 | 43.0 |
| ast | BIGINT | 52 | 29.03 | 0 | 89 | 23.02806035434098 | 23.0 |
| stl | BIGINT | 29 | 33.34 | 0 | 27 | 7.918407673246176 | 8.0 |
| blk | BIGINT | 24 | 33.02 | 0 | 23 | 4.997618819827577 | 5.0 |
| tov | BIGINT | 41 | 33.11 | 0 | 40 | 14.987430420298647 | 15.0 |
| pf | BIGINT | 62 | 10.59 | 0 | 122 | 22.742628029018054 | 22.0 |
| plus_minus | BIGINT | 109 | 6.53 | -73 | 73 | 0.0 | 0.0 |

## team_gold

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| id | BIGINT | 82 | 0.0 | 41 | 1610616834 | 923160825.7439024 | 1610610028.5 |
| full_name | VARCHAR | 81 | 0.0 | nan | nan | nan | nan |
| abbreviation | VARCHAR | 80 | 0.0 | nan | nan | nan | nan |
| nickname | VARCHAR | 30 | 63.41 | nan | nan | nan | nan |
| city | VARCHAR | 29 | 63.41 | nan | nan | nan | nan |
| state | VARCHAR | 23 | 63.41 | nan | nan | nan | nan |
| year_founded | BIGINT | 15 | 63.41 | 1946 | 2002 | 1969.7 | 1970.0 |

## team_gold_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| id | BIGINT | 82 | 0.0 | 41 | 1610616834 | 923160825.7439024 | 1610610028.5 |
| full_name | VARCHAR | 81 | 0.0 | nan | nan | nan | nan |
| abbreviation | VARCHAR | 80 | 0.0 | nan | nan | nan | nan |
| nickname | VARCHAR | 30 | 63.41 | nan | nan | nan | nan |
| city | VARCHAR | 29 | 63.41 | nan | nan | nan | nan |
| state | VARCHAR | 23 | 63.41 | nan | nan | nan | nan |
| year_founded | BIGINT | 15 | 63.41 | 1946 | 2002 | 1969.7 | 1970.0 |

## team_history

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| team_id | VARCHAR | 25 | 0.0 | nan | nan | nan | nan |
| city | VARCHAR | 43 | 0.0 | nan | nan | nan | nan |
| nickname | VARCHAR | 34 | 0.0 | nan | nan | nan | nan |
| year_founded | VARCHAR | 35 | 0.0 | nan | nan | nan | nan |
| year_active_till | VARCHAR | 24 | 0.0 | nan | nan | nan | nan |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## team_history_silver

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| team_id | BIGINT | 25 | 0.0 | 1610612737 | 1610612766 | 1610612753.7884614 | 1610612755.5 |
| city | VARCHAR | 43 | 0.0 | nan | nan | nan | nan |
| nickname | VARCHAR | 34 | 0.0 | nan | nan | nan | nan |
| year_founded | BIGINT | 35 | 0.0 | 1946 | 2014 | 1973.2884615384614 | 1971.5 |
| year_active_till | BIGINT | 24 | 0.0 | 1950 | 2019 | 1996.5192307692307 | 2012.0 |
| filename | VARCHAR | 1 | 0.0 | nan | nan | nan | nan |

## team_rolling_metrics

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| team_id | BIGINT | 74 | 6.53 | 41 | 1610616834 | 1609434972.9624403 | 1610612751.0 |
| game_id | BIGINT | 62398 | 0.0 | 10500001 | 49900088 | 25710146.421541266 | 25400252.5 |
| game_date | DATE | 13903 | 6.53 | nan | nan | nan | nan |
| season_id | BIGINT | 254 | 6.53 | 12005 | 42022 | 22941.630053928886 | 21997.0 |
| pts | BIGINT | 155 | 6.53 | 18 | 196 | 102.78235733219584 | 103.0 |
| pts_allowed | BIGINT | 155 | 6.53 | 18 | 196 | 102.78235733219584 | 103.0 |
| is_win | INTEGER | 2 | 0.0 | 0 | 1 | 0.4673492054451216 | 0.0 |
| rolling_pts_avg | DOUBLE | 1959 | 6.53 | 33.0 | 196.0 | 102.71233714573962 | 103.16666666666667 |
| rolling_pts_allowed_avg | DOUBLE | 2157 | 6.53 | 33.0 | 196.0 | 102.57225682248138 | 103.1 |
| rolling_win_pct | DOUBLE | 32 | 0.0 | 0.0 | 1.0 | 0.47218516322344456 | 0.5 |

## team_standings

| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |
|--------|------|----------|--------|-----|-----|------|--------|
| team_id | BIGINT | 82 | 0.0 | 41 | 1610616834 | 1577191308.4038208 | 1610612751.0 |
| team_name | VARCHAR | 81 | 0.0 | nan | nan | nan | nan |
| season_id | BIGINT | 225 | 0.0 | 12005 | 42022 | 26149.2546113307 | 22003.0 |
| games_played | BIGINT | 47 | 0.0 | 1 | 82 | 43.24242424242424 | 41.5 |
| wins | HUGEINT | 72 | 0.0 | 0 | 73 | 21.62121212121212 | 15.0 |
| losses | HUGEINT | 73 | 0.0 | 0 | 73 | 21.62121212121212 | 11.0 |
| win_pct | DOUBLE | 273 | 0.0 | 0.0 | 1.0 | 0.46645185936084593 | 0.5 |

