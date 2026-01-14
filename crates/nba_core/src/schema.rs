use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct League {
    pub league_id: i32,
    pub league_code: String,
    pub league_name: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Season {
    pub season_id: i32,
    pub league_id: i32,
    pub season_year: i32,
    pub start_date: Option<String>,
    pub end_date: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Arena {
    pub arena_id: i32,
    pub arena_name: String,
    pub city: Option<String>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Team {
    pub team_id: i64,
    pub league_id: i32,
    pub franchise_code: Option<String>,
    pub nba_api_team_id: Option<i64>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct TeamHistory {
    pub team_history_id: i32,
    pub team_id: i64,
    pub effective_start: String,
    pub effective_end: Option<String>,
    pub city: String,
    pub nickname: String,
    pub abbreviation: Option<String>,
    pub is_active: bool,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Player {
    pub player_id: i64,
    pub nba_api_person_id: Option<i64>,
    pub first_name: Option<String>,
    pub last_name: Option<String>,
    pub display_name: Option<String>,
    pub birth_date: Option<String>,
    pub from_year: Option<i32>,
    pub to_year: Option<i32>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Coach {
    pub coach_id: String,
    pub nba_api_coach_id: Option<i64>,
    pub display_name: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Referee {
    pub referee_id: String,
    pub nba_api_ref_id: Option<i64>,
    pub display_name: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Game {
    pub game_id: String,
    pub league_id: i32,
    pub season_id: i32,
    pub season_type: String,
    pub game_date: String,
    pub home_team_id: i64,
    pub away_team_id: i64,
    pub home_points: Option<i32>,
    pub away_points: Option<i32>,
    pub attendance: Option<i32>,
    pub arena_id: Option<i32>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct PlayerBoxscore {
    pub game_id: String,
    pub player_id: i64,
    pub team_id: i64,
    pub minutes: Option<f64>,
    pub points: Option<i32>,
    pub assists: Option<i32>,
    pub rebounds_total: Option<i32>,
    pub steals: Option<i32>,
    pub blocks: Option<i32>,
    pub fgm: Option<i32>,
    pub fga: Option<i32>,
    pub fg3m: Option<i32>,
    pub fg3a: Option<i32>,
    pub ftm: Option<i32>,
    pub fta: Option<i32>,
    pub pf: Option<i32>,
    pub turnovers: Option<i32>,
    pub plus_minus: Option<i32>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Draft {
    pub season_year: i32,
    pub pick_overall: i32,
    pub round_number: Option<i32>,
    pub pick_in_round: Option<i32>,
    pub team_id: Option<i64>,
    pub player_id: Option<i64>,
    pub college: Option<String>,
}
