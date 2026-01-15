import { query } from "./_generated/server";
import { v } from "convex/values";

type DirectoryAccumulator = {
  player_bref_id: string;
  player_name?: string;
  first_season: number;
  last_season: number;
  seasons: Set<number>;
  teams: Set<string>;
};

const displayName = (playerBrefId: string, playerName?: string | null) =>
  playerName && playerName.trim().length > 0 ? playerName : playerBrefId;

export const listPlayerDirectory = query({
  args: {
    limit: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    const rows = await ctx.db.query("player_season_totals").collect();
    const map = new Map<string, DirectoryAccumulator>();

    for (const row of rows) {
      const existing = map.get(row.player_bref_id);
      if (!existing) {
        map.set(row.player_bref_id, {
          player_bref_id: row.player_bref_id,
          player_name: row.player_name ?? undefined,
          first_season: row.season_year,
          last_season: row.season_year,
          seasons: new Set([row.season_year]),
          teams: new Set([row.team_abbrev]),
        });
        continue;
      }

      existing.first_season = Math.min(existing.first_season, row.season_year);
      existing.last_season = Math.max(existing.last_season, row.season_year);
      existing.seasons.add(row.season_year);
      existing.teams.add(row.team_abbrev);
      if (!existing.player_name && row.player_name) {
        existing.player_name = row.player_name;
      }
    }

    const list = Array.from(map.values()).map((entry) => ({
      player_bref_id: entry.player_bref_id,
      player_name: displayName(entry.player_bref_id, entry.player_name),
      first_season: entry.first_season,
      last_season: entry.last_season,
      seasons_count: entry.seasons.size,
      teams_count: entry.teams.size,
    }));

    list.sort((a, b) => a.player_name.localeCompare(b.player_name));

    const limit = args.limit ?? list.length;
    return list.slice(0, limit);
  },
});

export const getPlayerProfile = query({
  args: {
    playerBrefId: v.string(),
  },
  handler: async (ctx, args) => {
    const totals = await ctx.db
      .query("player_season_totals")
      .withIndex("by_player_season", (q) =>
        q.eq("player_bref_id", args.playerBrefId)
      )
      .collect();

    const advanced = await ctx.db
      .query("player_season_advanced")
      .withIndex("by_player_season", (q) =>
        q.eq("player_bref_id", args.playerBrefId)
      )
      .collect();

    totals.sort(
      (a, b) =>
        b.season_year - a.season_year ||
        a.team_abbrev.localeCompare(b.team_abbrev)
    );
    advanced.sort(
      (a, b) =>
        b.season_year - a.season_year ||
        a.team_abbrev.localeCompare(b.team_abbrev)
    );

    const seasons = totals.map((row) => row.season_year);
    const firstSeason = seasons.length ? Math.min(...seasons) : null;
    const lastSeason = seasons.length ? Math.max(...seasons) : null;

    const teams = new Set<string>();
    let playerName: string | undefined;

    for (const row of totals) {
      teams.add(row.team_abbrev);
      if (!playerName && row.player_name) {
        playerName = row.player_name;
      }
    }

    return {
      player: {
        player_bref_id: args.playerBrefId,
        player_name: displayName(args.playerBrefId, playerName),
        first_season: firstSeason,
        last_season: lastSeason,
        teams: Array.from(teams).sort(),
      },
      totals,
      advanced,
    };
  },
});
