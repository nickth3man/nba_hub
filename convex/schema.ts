import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

export default defineSchema({
  leagues: defineTable({
    league_id: v.number(),
    league_code: v.string(),
    league_name: v.string(),
  }).index("by_league_id", ["league_id"]),

  seasons: defineTable({
    season_id: v.number(),
    league_id: v.number(),
    season_year: v.number(),
    start_date: v.optional(v.string()),
    end_date: v.optional(v.string()),
  })
    .index("by_season_id", ["season_id"])
    .index("by_league_year", ["league_id", "season_year"]),

  arenas: defineTable({
    arena_id: v.number(),
    arena_name: v.string(),
    city: v.optional(v.string()),
  }).index("by_arena_id", ["arena_id"]),

  teams: defineTable({
    team_id: v.number(), // BIGINT in SQL
    league_id: v.number(),
    franchise_code: v.optional(v.string()),
    nba_api_team_id: v.optional(v.number()),
  }).index("by_team_id", ["team_id"]),

  team_history: defineTable({
    team_history_id: v.number(),
    team_id: v.number(),
    effective_start: v.string(), // DATE
    effective_end: v.optional(v.string()), // DATE
    city: v.string(),
    nickname: v.string(),
    abbreviation: v.optional(v.string()),
    is_active: v.boolean(),
  })
    .index("by_team_history_id", ["team_history_id"])
    .index("by_team_id", ["team_id"])
    .index("by_abbreviation", ["abbreviation"])
    .index("by_active", ["is_active", "team_id"]),

  players: defineTable({
    player_id: v.number(), // BIGINT
    nba_api_person_id: v.optional(v.number()),
    first_name: v.optional(v.string()),
    last_name: v.optional(v.string()),
    display_name: v.optional(v.string()),
    birth_date: v.optional(v.string()),
    from_year: v.optional(v.number()),
    to_year: v.optional(v.number()),
  })
    .index("by_player_id", ["player_id"])
    .index("by_last_name", ["last_name", "first_name"]),

  coaches: defineTable({
    coach_id: v.string(),
    nba_api_coach_id: v.optional(v.number()),
    display_name: v.string(),
  }).index("by_coach_id", ["coach_id"]),

  referees: defineTable({
    referee_id: v.string(),
    nba_api_ref_id: v.optional(v.number()),
    display_name: v.string(),
  }).index("by_referee_id", ["referee_id"]),

  games: defineTable({
    game_id: v.string(),
    league_id: v.number(),
    season_id: v.number(),
    season_type: v.string(),
    game_date: v.string(), // DATE
    home_team_id: v.number(),
    away_team_id: v.number(),
    home_points: v.optional(v.number()),
    away_points: v.optional(v.number()),
    attendance: v.optional(v.number()),
    arena_id: v.optional(v.number()),
  })
    .index("by_game_id", ["game_id"])
    .index("by_season_id", ["season_id"])
    .index("by_home_team", ["home_team_id"])
    .index("by_away_team", ["away_team_id"]),

  player_boxscores: defineTable({
    game_id: v.string(),
    player_id: v.number(),
    team_id: v.number(),
    minutes: v.optional(v.number()), // DOUBLE
    points: v.optional(v.number()),
    assists: v.optional(v.number()),
    rebounds_total: v.optional(v.number()),
    steals: v.optional(v.number()),
    blocks: v.optional(v.number()),
    fgm: v.optional(v.number()),
    fga: v.optional(v.number()),
    fg3m: v.optional(v.number()),
    fg3a: v.optional(v.number()),
    ftm: v.optional(v.number()),
    fta: v.optional(v.number()),
    pf: v.optional(v.number()),
    turnovers: v.optional(v.number()),
    plus_minus: v.optional(v.number()),
  })
    .index("by_game_id", ["game_id"])
    .index("by_player_id", ["player_id"])
    .index("by_game_player", ["game_id", "player_id"]),

  team_boxscores: defineTable({
    game_id: v.string(),
    team_id: v.number(),
    minutes: v.optional(v.number()),
    points: v.optional(v.number()),
    assists: v.optional(v.number()),
    rebounds_total: v.optional(v.number()),
    fgm: v.optional(v.number()),
    fga: v.optional(v.number()),
    fg3m: v.optional(v.number()),
    fg3a: v.optional(v.number()),
    ftm: v.optional(v.number()),
    fta: v.optional(v.number()),
    turnovers: v.optional(v.number()),
    pf: v.optional(v.number()),
  })
    .index("by_game_id", ["game_id"])
    .index("by_team_id", ["team_id"])
    .index("by_game_team", ["game_id", "team_id"]),

  player_season_totals: defineTable({
    season_year: v.number(),
    player_bref_id: v.string(),
    player_name: v.optional(v.string()),
    team_abbrev: v.string(),
    games: v.number(),
    games_started: v.optional(v.number()),
    minutes: v.optional(v.number()),
    points: v.optional(v.number()),
    assists: v.optional(v.number()),
    rebounds_total: v.optional(v.number()),
    steals: v.optional(v.number()),
    blocks: v.optional(v.number()),
    fgm: v.optional(v.number()),
    fga: v.optional(v.number()),
    fg3m: v.optional(v.number()),
    fg3a: v.optional(v.number()),
    ftm: v.optional(v.number()),
    fta: v.optional(v.number()),
    turnovers: v.optional(v.number()),
    pf: v.optional(v.number()),
  })
    .index("by_player_season_team", ["player_bref_id", "season_year", "team_abbrev"])
    .index("by_player_season", ["player_bref_id", "season_year"])
    .index("by_season_year", ["season_year"])
    .index("by_season_team", ["season_year", "team_abbrev"]),

  player_season_advanced: defineTable({
    season_year: v.number(),
    player_bref_id: v.string(),
    team_abbrev: v.string(),
    minutes: v.optional(v.number()),
    per: v.optional(v.number()),
    ts_percent: v.optional(v.number()),
    usg_percent: v.optional(v.number()),
    ows: v.optional(v.number()),
    dws: v.optional(v.number()),
    ws: v.optional(v.number()),
    bpm: v.optional(v.number()),
    vorp: v.optional(v.number()),
  })
    .index("by_player_season_team", ["player_bref_id", "season_year", "team_abbrev"])
    .index("by_player_season", ["player_bref_id", "season_year"])
    .index("by_season_year", ["season_year"])
    .index("by_season_team", ["season_year", "team_abbrev"]),

  team_season_totals: defineTable({
    season_year: v.number(),
    team_abbrev: v.string(),
    games: v.number(),
    minutes: v.optional(v.number()),
    points: v.optional(v.number()),
    assists: v.optional(v.number()),
    rebounds_total: v.optional(v.number()),
    fgm: v.optional(v.number()),
    fga: v.optional(v.number()),
    fg3m: v.optional(v.number()),
    fg3a: v.optional(v.number()),
    ftm: v.optional(v.number()),
    fta: v.optional(v.number()),
    turnovers: v.optional(v.number()),
    pf: v.optional(v.number()),
  })
    .index("by_team_season", ["team_abbrev", "season_year"])
    .index("by_season_year", ["season_year"]),

  team_season_advanced: defineTable({
    season_year: v.number(),
    team_abbrev: v.string(),
    wins: v.number(),
    losses: v.number(),
    srs: v.optional(v.number()),
    pace: v.optional(v.number()),
    off_rtg: v.optional(v.number()),
    def_rtg: v.optional(v.number()),
    net_rtg: v.optional(v.number()),
  })
    .index("by_team_season", ["team_abbrev", "season_year"])
    .index("by_season_year", ["season_year"]),

  standings: defineTable({
    season_year: v.number(),
    team_abbrev: v.string(),
    wins: v.number(),
    losses: v.number(),
    playoffs: v.boolean(),
  })
    .index("by_team_season", ["team_abbrev", "season_year"])
    .index("by_season_year", ["season_year"]),

  drafts: defineTable({
    season_year: v.number(),
    pick_overall: v.number(),
    round_number: v.optional(v.number()),
    pick_in_round: v.optional(v.number()),
    team_abbrev: v.optional(v.string()),
    player_bref_id: v.optional(v.string()),
    player_name: v.optional(v.string()),
    college: v.optional(v.string()),
  })
    .index("by_season_pick", ["season_year", "pick_overall"])
    .index("by_team_abbrev", ["team_abbrev"])
    .index("by_player_bref_id", ["player_bref_id"]),

  awards: defineTable({
    award_key: v.string(),
    award_type: v.string(),
    season_year: v.number(),
    player_bref_id: v.optional(v.string()),
    player_name: v.optional(v.string()),
    team_abbrev: v.optional(v.string()),
    rank: v.optional(v.number()),
    points_won: v.optional(v.number()),
    points_max: v.optional(v.number()),
    share: v.optional(v.number()),
  })
    .index("by_award_key", ["award_key"])
    .index("by_award_season", ["award_type", "season_year"])
    .index("by_season_year", ["season_year"])
    .index("by_player_bref_id", ["player_bref_id"]),

  transactions: defineTable({
    transaction_id: v.string(),
    season_year: v.number(),
    team_abbrev: v.optional(v.string()),
    player_bref_id: v.optional(v.string()),
    details: v.string(),
  })
    .index("by_transaction_id", ["transaction_id"])
    .index("by_season_year", ["season_year"])
    .index("by_player_bref_id", ["player_bref_id"]),
});
