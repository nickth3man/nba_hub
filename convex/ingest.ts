import { mutation } from "./_generated/server";
import { v } from "convex/values";

export const upsertLeagues = mutation({
  args: {
    leagues: v.array(
      v.object({
        league_id: v.number(),
        league_code: v.string(),
        league_name: v.string(),
      })
    ),
  },
  handler: async (ctx, args) => {
    for (const league of args.leagues) {
      const existing = await ctx.db
        .query("leagues")
        .withIndex("by_league_id", (q) => q.eq("league_id", league.league_id))
        .first();
      if (!existing) {
        await ctx.db.insert("leagues", league);
      }
    }
  },
});

export const upsertSeasons = mutation({
  args: {
    seasons: v.array(
      v.object({
        season_id: v.number(),
        league_id: v.number(),
        season_year: v.number(),
        start_date: v.optional(v.string()),
        end_date: v.optional(v.string()),
      })
    ),
  },
  handler: async (ctx, args) => {
    for (const season of args.seasons) {
      const existing = await ctx.db
        .query("seasons")
        .withIndex("by_season_id", (q) => q.eq("season_id", season.season_id))
        .first();
      if (!existing) {
        await ctx.db.insert("seasons", season);
      }
    }
  },
});

export const upsertArenas = mutation({
  args: {
    arenas: v.array(
      v.object({
        arena_id: v.number(),
        arena_name: v.string(),
        city: v.optional(v.string()),
      })
    ),
  },
  handler: async (ctx, args) => {
    for (const arena of args.arenas) {
      const existing = await ctx.db
        .query("arenas")
        .withIndex("by_arena_id", (q) => q.eq("arena_id", arena.arena_id))
        .first();
      if (!existing) {
        await ctx.db.insert("arenas", arena);
      }
    }
  },
});

export const upsertTeams = mutation({
  args: {
    teams: v.array(
      v.object({
        team_id: v.number(),
        league_id: v.number(),
        franchise_code: v.optional(v.string()),
        nba_api_team_id: v.optional(v.number()),
      })
    ),
  },
  handler: async (ctx, args) => {
    for (const team of args.teams) {
      const existing = await ctx.db
        .query("teams")
        .withIndex("by_team_id", (q) => q.eq("team_id", team.team_id))
        .first();
      if (!existing) {
        await ctx.db.insert("teams", team);
      }
    }
  },
});

export const upsertTeamHistory = mutation({
  args: {
    history: v.array(
      v.object({
        team_history_id: v.number(),
        team_id: v.number(),
        effective_start: v.string(),
        effective_end: v.optional(v.string()),
        city: v.string(),
        nickname: v.string(),
        abbreviation: v.optional(v.string()),
        is_active: v.boolean(),
      })
    ),
  },
  handler: async (ctx, args) => {
    for (const row of args.history) {
      const existing = await ctx.db
        .query("team_history")
        .withIndex("by_team_history_id", (q) =>
          q.eq("team_history_id", row.team_history_id)
        )
        .first();
      if (!existing) {
        await ctx.db.insert("team_history", row);
      }
    }
  },
});

export const upsertPlayers = mutation({
  args: {
    players: v.array(
      v.object({
        player_id: v.number(),
        nba_api_person_id: v.optional(v.number()),
        first_name: v.optional(v.string()),
        last_name: v.optional(v.string()),
        display_name: v.optional(v.string()),
        birth_date: v.optional(v.string()),
        from_year: v.optional(v.number()),
        to_year: v.optional(v.number()),
      })
    ),
  },
  handler: async (ctx, args) => {
    for (const player of args.players) {
      const existing = await ctx.db
        .query("players")
        .withIndex("by_player_id", (q) => q.eq("player_id", player.player_id))
        .first();
      if (!existing) {
        await ctx.db.insert("players", player);
      }
    }
  },
});

export const upsertGames = mutation({
  args: {
    games: v.array(
      v.object({
        game_id: v.string(),
        league_id: v.number(),
        season_id: v.number(),
        season_type: v.string(),
        game_date: v.string(),
        home_team_id: v.number(),
        away_team_id: v.number(),
        home_points: v.optional(v.number()),
        away_points: v.optional(v.number()),
        attendance: v.optional(v.number()),
        arena_id: v.optional(v.number()),
      })
    ),
  },
  handler: async (ctx, args) => {
    for (const game of args.games) {
      const existing = await ctx.db
        .query("games")
        .withIndex("by_game_id", (q) => q.eq("game_id", game.game_id))
        .first();
      if (!existing) {
        await ctx.db.insert("games", game);
      }
    }
  },
});

export const upsertPlayerBoxscores = mutation({
  args: {
    boxscores: v.array(
      v.object({
        game_id: v.string(),
        player_id: v.number(),
        team_id: v.number(),
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
        pf: v.optional(v.number()),
        turnovers: v.optional(v.number()),
        plus_minus: v.optional(v.number()),
      })
    ),
  },
  handler: async (ctx, args) => {
    for (const row of args.boxscores) {
      const existing = await ctx.db
        .query("player_boxscores")
        .withIndex("by_game_player", (q) =>
          q.eq("game_id", row.game_id).eq("player_id", row.player_id)
        )
        .first();
      if (!existing) {
        await ctx.db.insert("player_boxscores", row);
      }
    }
  },
});

export const upsertTeamBoxscores = mutation({
  args: {
    boxscores: v.array(
      v.object({
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
    ),
  },
  handler: async (ctx, args) => {
    for (const row of args.boxscores) {
      const existing = await ctx.db
        .query("team_boxscores")
        .withIndex("by_game_team", (q) =>
          q.eq("game_id", row.game_id).eq("team_id", row.team_id)
        )
        .first();
      if (!existing) {
        await ctx.db.insert("team_boxscores", row);
      }
    }
  },
});

export const upsertDrafts = mutation({
  args: {
    drafts: v.array(
      v.object({
        season_year: v.number(),
        pick_overall: v.number(),
        round_number: v.optional(v.number()),
        pick_in_round: v.optional(v.number()),
        team_abbrev: v.optional(v.string()),
        player_bref_id: v.optional(v.string()),
        player_name: v.optional(v.string()),
        college: v.optional(v.string()),
      })
    ),
  },
  handler: async (ctx, args) => {
    for (const draft of args.drafts) {
      const existing = await ctx.db
        .query("drafts")
        .withIndex("by_season_pick", (q) =>
          q.eq("season_year", draft.season_year).eq(
            "pick_overall",
            draft.pick_overall
          )
        )
        .first();
      if (!existing) {
        await ctx.db.insert("drafts", draft);
      }
    }
  },
});

export const upsertPlayerSeasonTotals = mutation({
  args: {
    totals: v.array(
      v.object({
        season_year: v.number(),
        player_bref_id: v.string(),
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
    ),
  },
  handler: async (ctx, args) => {
    for (const row of args.totals) {
      const existing = await ctx.db
        .query("player_season_totals")
        .withIndex("by_player_season_team", (q) =>
          q.eq("player_bref_id", row.player_bref_id)
            .eq("season_year", row.season_year)
            .eq("team_abbrev", row.team_abbrev)
        )
        .first();
      if (!existing) {
        await ctx.db.insert("player_season_totals", row);
      }
    }
  },
});

export const upsertPlayerSeasonAdvanced = mutation({
  args: {
    advanced: v.array(
      v.object({
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
    ),
  },
  handler: async (ctx, args) => {
    for (const row of args.advanced) {
      const existing = await ctx.db
        .query("player_season_advanced")
        .withIndex("by_player_season_team", (q) =>
          q.eq("player_bref_id", row.player_bref_id)
            .eq("season_year", row.season_year)
            .eq("team_abbrev", row.team_abbrev)
        )
        .first();
      if (!existing) {
        await ctx.db.insert("player_season_advanced", row);
      }
    }
  },
});

export const upsertTeamSeasonTotals = mutation({
  args: {
    totals: v.array(
      v.object({
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
    ),
  },
  handler: async (ctx, args) => {
    for (const row of args.totals) {
      const existing = await ctx.db
        .query("team_season_totals")
        .withIndex("by_team_season", (q) =>
          q.eq("team_abbrev", row.team_abbrev).eq(
            "season_year",
            row.season_year
          )
        )
        .first();
      if (!existing) {
        await ctx.db.insert("team_season_totals", row);
      }
    }
  },
});

export const upsertTeamSeasonAdvanced = mutation({
  args: {
    advanced: v.array(
      v.object({
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
    ),
  },
  handler: async (ctx, args) => {
    for (const row of args.advanced) {
      const existing = await ctx.db
        .query("team_season_advanced")
        .withIndex("by_team_season", (q) =>
          q.eq("team_abbrev", row.team_abbrev).eq(
            "season_year",
            row.season_year
          )
        )
        .first();
      if (!existing) {
        await ctx.db.insert("team_season_advanced", row);
      }
    }
  },
});

export const upsertStandings = mutation({
  args: {
    standings: v.array(
      v.object({
        season_year: v.number(),
        team_abbrev: v.string(),
        wins: v.number(),
        losses: v.number(),
        playoffs: v.boolean(),
      })
    ),
  },
  handler: async (ctx, args) => {
    for (const row of args.standings) {
      const existing = await ctx.db
        .query("standings")
        .withIndex("by_team_season", (q) =>
          q.eq("team_abbrev", row.team_abbrev).eq(
            "season_year",
            row.season_year
          )
        )
        .first();
      if (!existing) {
        await ctx.db.insert("standings", row);
      }
    }
  },
});

export const upsertAwards = mutation({
  args: {
    awards: v.array(
      v.object({
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
    ),
  },
  handler: async (ctx, args) => {
    for (const row of args.awards) {
      const existing = await ctx.db
        .query("awards")
        .withIndex("by_award_key", (q) => q.eq("award_key", row.award_key))
        .first();
      if (!existing) {
        await ctx.db.insert("awards", row);
      }
    }
  },
});

export const upsertCoaches = mutation({
  args: {
    coaches: v.array(
      v.object({
        coach_id: v.string(),
        nba_api_coach_id: v.optional(v.number()),
        display_name: v.string(),
      })
    ),
  },
  handler: async (ctx, args) => {
    for (const coach of args.coaches) {
      const existing = await ctx.db
        .query("coaches")
        .withIndex("by_coach_id", (q) => q.eq("coach_id", coach.coach_id))
        .first();
      if (!existing) {
        await ctx.db.insert("coaches", coach);
      }
    }
  },
});

export const upsertReferees = mutation({
  args: {
    referees: v.array(
      v.object({
        referee_id: v.string(),
        nba_api_ref_id: v.optional(v.number()),
        display_name: v.string(),
      })
    ),
  },
  handler: async (ctx, args) => {
    for (const referee of args.referees) {
      const existing = await ctx.db
        .query("referees")
        .withIndex("by_referee_id", (q) =>
          q.eq("referee_id", referee.referee_id)
        )
        .first();
      if (!existing) {
        await ctx.db.insert("referees", referee);
      }
    }
  },
});

export const upsertTransactions = mutation({
  args: {
    transactions: v.array(
      v.object({
        transaction_id: v.string(),
        season_year: v.number(),
        team_abbrev: v.optional(v.string()),
        player_bref_id: v.optional(v.string()),
        details: v.string(),
      })
    ),
  },
  handler: async (ctx, args) => {
    for (const row of args.transactions) {
      const existing = await ctx.db
        .query("transactions")
        .withIndex("by_transaction_id", (q) =>
          q.eq("transaction_id", row.transaction_id)
        )
        .first();
      if (!existing) {
        await ctx.db.insert("transactions", row);
      }
    }
  },
});
