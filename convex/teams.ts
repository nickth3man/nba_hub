import { query } from "./_generated/server";
import { v } from "convex/values";

export const listTeams = query({
  args: {
    activeOnly: v.optional(v.boolean()),
    paginationOpts: v.optional(
      v.object({
        numItems: v.number(),
        cursor: v.optional(v.union(v.string(), v.null())),
      })
    ),
  },
  handler: async (ctx, args) => {
    const paginationOpts = {
      numItems: args.paginationOpts?.numItems ?? 200,
      cursor: args.paginationOpts?.cursor ?? null,
    };
    if (args.activeOnly === false) {
      return await ctx.db
        .query("team_history")
        .withIndex("by_team_history_id", (q) => q.gte("team_history_id", 0))
        .paginate(paginationOpts);
    }
    return await ctx.db
      .query("team_history")
      .withIndex("by_active", (q) => q.eq("is_active", true))
      .paginate(paginationOpts);
  },
});
