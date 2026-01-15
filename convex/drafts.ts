import { query } from "./_generated/server";
import { v } from "convex/values";

export const listDraftBySeason = query({
  args: {
    seasonYear: v.number(),
  },
  handler: async (ctx, args) => {
    const drafts = await ctx.db
      .query("drafts")
      .withIndex("by_season_pick", (q) => q.eq("season_year", args.seasonYear))
      .collect();

    drafts.sort((a, b) => a.pick_overall - b.pick_overall);
    return drafts;
  },
});
