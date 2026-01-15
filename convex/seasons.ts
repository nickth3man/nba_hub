import { query } from "./_generated/server";
import { v } from "convex/values";

export const listSeasons = query({
  args: {
    leagueId: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    const seasons = args.leagueId !== undefined
      ? await ctx.db
          .query("seasons")
          .withIndex("by_league_year", (q) =>
            q.eq("league_id", args.leagueId as number).gte("season_year", 0)
          )
          .collect()
      : await ctx.db
          .query("seasons")
          .withIndex("by_season_id", (q) => q.gte("season_id", 0))
          .collect();

    seasons.sort((a, b) => b.season_year - a.season_year);
    return seasons;
  },
});

export const getSeasonSummary = query({
  args: {
    seasonYear: v.number(),
  },
  handler: async (ctx, args) => {
    const season = await ctx.db
      .query("seasons")
      .withIndex("by_league_year", (q) =>
        q.eq("league_id", 1).eq("season_year", args.seasonYear)
      )
      .first();

    const standings = await ctx.db
      .query("standings")
      .withIndex("by_season_year", (q) => q.eq("season_year", args.seasonYear))
      .collect();
    standings.sort((a, b) => b.wins - a.wins || a.losses - b.losses);

    const teamTotals = await ctx.db
      .query("team_season_totals")
      .withIndex("by_season_year", (q) => q.eq("season_year", args.seasonYear))
      .collect();
    teamTotals.sort((a, b) => (b.points ?? 0) - (a.points ?? 0));

    const teamAdvanced = await ctx.db
      .query("team_season_advanced")
      .withIndex("by_season_year", (q) => q.eq("season_year", args.seasonYear))
      .collect();
    teamAdvanced.sort((a, b) => b.wins - a.wins);

    return {
      season,
      standings,
      teamTotals,
      teamAdvanced,
    };
  },
});
