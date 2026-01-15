use crate::models::TeamHistoryRow;

pub fn format_optional_i32(value: Option<i32>) -> String {
    value
        .map(|val| val.to_string())
        .unwrap_or_else(|| "-".to_string())
}

pub fn format_optional_f64(value: Option<f64>, precision: usize) -> String {
    value
        .map(|val| format!("{:.precision$}", val, precision = precision))
        .unwrap_or_else(|| "-".to_string())
}

pub fn format_percent(value: Option<f64>) -> String {
    value
        .map(|val| {
            let percent = if val.abs() <= 1.0 { val * 100.0 } else { val };
            format!("{:.1}%", percent)
        })
        .unwrap_or_else(|| "-".to_string())
}

pub fn percent_from_counts(made: Option<i32>, attempts: Option<i32>) -> Option<f64> {
    match (made, attempts) {
        (Some(made), Some(attempts)) if attempts > 0 => Some(made as f64 / attempts as f64),
        _ => None,
    }
}

pub fn format_team_label(city: &str, nickname: &str) -> String {
    format!("{} {}", city, nickname)
}

pub fn build_team_lookup(
    histories: &[TeamHistoryRow],
) -> std::collections::HashMap<String, String> {
    let mut map = std::collections::HashMap::new();
    let mut sorted = histories.to_vec();
    sorted.sort_by(|a, b| a.effective_start.cmp(&b.effective_start));

    for team in sorted {
        if let Some(abbrev) = &team.abbreviation {
            map.insert(
                abbrev.clone(),
                format_team_label(&team.city, &team.nickname),
            );
        }
    }

    map
}
