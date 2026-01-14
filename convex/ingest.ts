import { MutationCtx } from "./_generated/server";

export const insertLeague = async (
  ctx: MutationCtx,
  args: {
    league_id: number;
    league_code: string;
    league_name: string;
  }
) => {
  const existing = await ctx.db
    .query("leagues")
    .withIndex("by_league_id", (q) => q.eq("league_id", args.league_id))
    .first();
  
  if (!existing) {
    await ctx.db.insert("leagues", args);
  }
};

export const insertSeason = async (
  ctx: MutationCtx,
  args: {
    season_id: number;
    league_id: number;
    season_year: number;
    start_date?: string;
    end_date?: string;
  }
) => {
  const existing = await ctx.db
    .query("seasons")
    .withIndex("by_season_id", (q) => q.eq("season_id", args.season_id))
    .first();
  
  if (!existing) {
    await ctx.db.insert("seasons", args);
  }
};

export const insertReferee = async (
  ctx: MutationCtx,
  args: {
    referee_id: string;
    nba_api_ref_id?: number;
    display_name: string;
  }
) => {
  const existing = await ctx.db
    .query("referees")
    .withIndex("by_referee_id", (q) => q.eq("referee_id", args.referee_id))
    .first();
  
  if (!existing) {
    await ctx.db.insert("referees", args);
  }
};

export const insertCoach = async (
  ctx: MutationCtx,
  args: {
    coach_id: string;
    nba_api_coach_id?: number;
    display_name: string;
  }
) => {
  const existing = await ctx.db
    .query("coaches")
    .withIndex("by_coach_id", (q) => q.eq("coach_id", args.coach_id))
    .first();
  
  if (!existing) {
    await ctx.db.insert("coaches", args);
  }
};
