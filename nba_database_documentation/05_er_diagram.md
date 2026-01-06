# NBA Database - Entity-Relationship Diagram

*Generated: 2026-01-05 17:03:21*

## Core Tables ERD

```mermaid
erDiagram
    team {
        VARCHAR id
        VARCHAR full_name
        VARCHAR abbreviation
        VARCHAR nickname
        VARCHAR city
        VARCHAR state
        VARCHAR year_founded
        VARCHAR filename
    }
    games {
        BIGINT game_id
        BIGINT season_id
        DATE game_date
        BIGINT home_team_id
        BIGINT visitor_team_id
        BIGINT home_pts
        BIGINT visitor_pts
        VARCHAR home_wl
        VARCHAR visitor_wl
        VARCHAR season_type
    }
    common_player_info {
        VARCHAR person_id
        VARCHAR first_name
        VARCHAR last_name
        VARCHAR display_first_last
        VARCHAR display_last_comma_first
        VARCHAR display_fi_last
        VARCHAR player_slug
        VARCHAR birthdate
        VARCHAR school
        VARCHAR country
    }
    team_game_stats {
        BIGINT game_id
        BIGINT team_id
        BIGINT season_id
        DATE game_date
        BOOLEAN is_home
        BIGINT pts
        BIGINT fgm
        BIGINT fga
        BIGINT fg_pct
        BIGINT fg3m
    }
    player_game_stats {
        BIGINT game_id
        BIGINT team_id
        BIGINT player_id
        VARCHAR player_name
        VARCHAR start_position
        VARCHAR comment
        VARCHAR min
        INTEGER fgm
        INTEGER fga
        DOUBLE fg_pct
    }
    team ||--o{ team_game_stats : has
    games ||--o{ team_game_stats : contains
    games ||--o{ player_game_stats : contains
    common_player_info ||--o{ player_game_stats : plays
```

## Notes

- This diagram shows core tables and their primary relationships
- Full database contains 75+ tables across raw, silver, and gold layers
- See [Semantic Analysis](03_semantic_analysis.md) for complete relationship details
