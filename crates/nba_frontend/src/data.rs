#[derive(Clone, Copy)]
pub struct NavItem {
    pub label: &'static str,
    pub href: &'static str,
}

pub const NAV_ITEMS: &[NavItem] = &[
    NavItem {
        label: "Home",
        href: "/",
    },
    NavItem {
        label: "Players",
        href: "/players",
    },
    NavItem {
        label: "Teams",
        href: "/teams",
    },
    NavItem {
        label: "Seasons",
        href: "/seasons",
    },
    NavItem {
        label: "Leaders",
        href: "/leaders",
    },
    NavItem {
        label: "Awards",
        href: "/awards",
    },
    NavItem {
        label: "Draft",
        href: "/draft",
    },
    NavItem {
        label: "Transactions",
        href: "/transactions",
    },
    NavItem {
        label: "Glossary",
        href: "/glossary",
    },
];

#[derive(Clone, Copy)]
pub struct StatDefinition {
    pub abbr: &'static str,
    pub label: &'static str,
    pub description: &'static str,
}

pub const STAT_GLOSSARY: &[StatDefinition] = &[
    StatDefinition {
        abbr: "G",
        label: "Games",
        description: "Games played.",
    },
    StatDefinition {
        abbr: "PTS",
        label: "Points",
        description: "Total points scored.",
    },
    StatDefinition {
        abbr: "REB",
        label: "Rebounds",
        description: "Total rebounds (offensive + defensive).",
    },
    StatDefinition {
        abbr: "AST",
        label: "Assists",
        description: "Total assists.",
    },
    StatDefinition {
        abbr: "FG%",
        label: "Field Goal %",
        description: "Field goals made divided by field goals attempted.",
    },
    StatDefinition {
        abbr: "3P%",
        label: "3-Point %",
        description: "3-point field goals made divided by attempts.",
    },
    StatDefinition {
        abbr: "FT%",
        label: "Free Throw %",
        description: "Free throws made divided by attempts.",
    },
    StatDefinition {
        abbr: "PER",
        label: "Player Efficiency Rating",
        description: "Overall per-minute productivity metric.",
    },
    StatDefinition {
        abbr: "TS%",
        label: "True Shooting %",
        description: "Scoring efficiency including 2P, 3P, and FT.",
    },
    StatDefinition {
        abbr: "USG%",
        label: "Usage Rate",
        description: "Estimated percentage of team plays used.",
    },
    StatDefinition {
        abbr: "WS",
        label: "Win Shares",
        description: "Estimated wins contributed.",
    },
    StatDefinition {
        abbr: "BPM",
        label: "Box Plus/Minus",
        description: "Estimated point impact per 100 possessions.",
    },
    StatDefinition {
        abbr: "VORP",
        label: "Value Over Replacement",
        description: "Value contributed over a replacement-level player.",
    },
    StatDefinition {
        abbr: "SRS",
        label: "Simple Rating System",
        description: "Team rating based on point differential and schedule.",
    },
    StatDefinition {
        abbr: "PACE",
        label: "Pace",
        description: "Estimated possessions per 48 minutes.",
    },
    StatDefinition {
        abbr: "ORtg",
        label: "Offensive Rating",
        description: "Points scored per 100 possessions.",
    },
    StatDefinition {
        abbr: "DRtg",
        label: "Defensive Rating",
        description: "Points allowed per 100 possessions.",
    },
    StatDefinition {
        abbr: "NetRtg",
        label: "Net Rating",
        description: "Offensive rating minus defensive rating.",
    },
    StatDefinition {
        abbr: "W",
        label: "Wins",
        description: "Regular season wins.",
    },
    StatDefinition {
        abbr: "L",
        label: "Losses",
        description: "Regular season losses.",
    },
];

pub fn stat_definition(abbr: &str) -> Option<&'static StatDefinition> {
    STAT_GLOSSARY
        .iter()
        .find(|stat| stat.abbr.eq_ignore_ascii_case(abbr))
}
