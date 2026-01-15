pub fn build_award_key(
    award_type: &str,
    season_year: i32,
    player_bref_id: Option<&str>,
    player_name: Option<&str>,
) -> Option<String> {
    if let Some(id) = player_bref_id {
        let trimmed = id.trim();
        if !trimmed.is_empty() {
            return Some(format!("{award_type}|{season_year}|{trimmed}"));
        }
    }

    if let Some(name) = player_name {
        let normalized = normalize_name(name);
        if !normalized.is_empty() {
            return Some(format!("{award_type}|{season_year}|{normalized}"));
        }
    }

    None
}

fn normalize_name(name: &str) -> String {
    name.split_whitespace().collect::<Vec<_>>().join(" ")
}
