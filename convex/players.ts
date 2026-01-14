import { query } from "./_generated/server";
import { v } from "convex/values";

export const listPlayers = query({
  args: {
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
    return await ctx.db
      .query("players")
      .withIndex("by_last_name", (q) => q.gte("last_name", ""))
      .paginate(paginationOpts);
  },
});
