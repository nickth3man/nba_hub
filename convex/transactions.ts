import { query } from "./_generated/server";
import { v } from "convex/values";

export const listTransactionsBySeason = query({
  args: {
    seasonYear: v.number(),
  },
  handler: async (ctx, args) => {
    const transactions = await ctx.db
      .query("transactions")
      .withIndex("by_season_year", (q) => q.eq("season_year", args.seasonYear))
      .collect();

    transactions.sort((a, b) => a.transaction_id.localeCompare(b.transaction_id));
    return transactions;
  },
});
