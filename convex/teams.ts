import { query } from "./_generated/server";
import { v } from "convex/values";

const seasonSort = (a: { season_year: number }, b: { season_year: number }) =>
  b.season_year - a.season_year;

export const listTeams = query({
  args: {
    activeOnly: v.optional(v.boolean()),
  },
  handler: async (ctx, args) => {
    if (args.activeOnly === false) {
      return await ctx.db
        .query("team_history")
        .withIndex("by_team_history_id", (q) => q.gte("team_history_id", 0))
        .collect();
    }
    return await ctx.db
      .query("team_history")
      .withIndex("by_active", (q) => q.eq("is_active", true))
      .collect();
  },
});

export const getTeamProfile = query({
  args: {
    teamAbbrev: v.string(),
  },
  handler: async (ctx, args) => {
    const history = await ctx.db
      .query("team_history")
      .withIndex("by_abbreviation", (q) => q.eq("abbreviation", args.teamAbbrev))
      .collect();

    const sortedHistory = [...history].sort((a, b) =>
      a.effective_start.localeCompare(b.effective_start)
    );
    const team = history.find((row) => row.is_active) ?? sortedHistory.at(-1) ?? null;

    const totals = await ctx.db
      .query("team_season_totals")
      .withIndex("by_team_season", (q) => q.eq("team_abbrev", args.teamAbbrev))
      .collect();
    totals.sort(seasonSort);

    const advanced = await ctx.db
      .query("team_season_advanced")
      .withIndex("by_team_season", (q) => q.eq("team_abbrev", args.teamAbbrev))
      .collect();
    advanced.sort(seasonSort);

    const standings = await ctx.db
      .query("standings")
      .withIndex("by_team_season", (q) => q.eq("team_abbrev", args.teamAbbrev))
      .collect();
    standings.sort(seasonSort);

    return {
      team,
      totals,
      advanced,
      standings,
    };
  },
});
