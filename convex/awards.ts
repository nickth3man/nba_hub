import { query } from "./_generated/server";
import { v } from "convex/values";

export const listAwardsBySeason = query({
  args: {
    seasonYear: v.number(),
  },
  handler: async (ctx, args) => {
    const awards = await ctx.db
      .query("awards")
      .withIndex("by_season_year", (q) => q.eq("season_year", args.seasonYear))
      .collect();

    awards.sort((a, b) => {
      const typeSort = a.award_type.localeCompare(b.award_type);
      if (typeSort !== 0) {
        return typeSort;
      }
      return (a.rank ?? 99) - (b.rank ?? 99);
    });

    return awards;
  },
});
