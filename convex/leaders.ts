import { query } from "./_generated/server";
import { v } from "convex/values";

type LeaderAccumulator = {
  player_bref_id: string;
  player_name?: string;
  games: number;
  points: number;
  rebounds: number;
  assists: number;
  steals: number;
  blocks: number;
  teams: Set<string>;
};

type LeaderRow = {
  player_bref_id: string;
  player_name: string;
  teams: string[];
  value: number;
  per_game: number;
  games: number;
};

const toNumber = (value?: number | null) => value ?? 0;

const buildLeaders = (
  map: Map<string, LeaderAccumulator>,
  key: "points" | "rebounds" | "assists" | "steals" | "blocks"
): LeaderRow[] => {
  const list = Array.from(map.values()).map((entry) => ({
    player_bref_id: entry.player_bref_id,
    player_name: entry.player_name ?? entry.player_bref_id,
    teams: Array.from(entry.teams).sort(),
    value: entry[key],
    per_game: entry.games ? entry[key] / entry.games : 0,
    games: entry.games,
  }));

  list.sort((a, b) => b.value - a.value);
  return list.slice(0, 10);
};

export const getSeasonLeaders = query({
  args: {
    seasonYear: v.number(),
  },
  handler: async (ctx, args) => {
    const rows = await ctx.db
      .query("player_season_totals")
      .withIndex("by_season_year", (q) => q.eq("season_year", args.seasonYear))
      .collect();

    const map = new Map<string, LeaderAccumulator>();

    for (const row of rows) {
      const existing = map.get(row.player_bref_id);
      if (!existing) {
        map.set(row.player_bref_id, {
          player_bref_id: row.player_bref_id,
          player_name: row.player_name ?? undefined,
          games: row.games,
          points: toNumber(row.points),
          rebounds: toNumber(row.rebounds_total),
          assists: toNumber(row.assists),
          steals: toNumber(row.steals),
          blocks: toNumber(row.blocks),
          teams: new Set([row.team_abbrev]),
        });
        continue;
      }

      existing.games += row.games;
      existing.points += toNumber(row.points);
      existing.rebounds += toNumber(row.rebounds_total);
      existing.assists += toNumber(row.assists);
      existing.steals += toNumber(row.steals);
      existing.blocks += toNumber(row.blocks);
      existing.teams.add(row.team_abbrev);
      if (!existing.player_name && row.player_name) {
        existing.player_name = row.player_name;
      }
    }

    return {
      points: buildLeaders(map, "points"),
      rebounds: buildLeaders(map, "rebounds"),
      assists: buildLeaders(map, "assists"),
      steals: buildLeaders(map, "steals"),
      blocks: buildLeaders(map, "blocks"),
    };
  },
});
