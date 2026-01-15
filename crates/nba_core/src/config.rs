use std::env;
use std::path::{PathBuf};

pub fn convex_url() -> String {
    env::var("CONVEX_URL").unwrap_or_else(|_| "http://localhost:3210".to_string())
}

pub fn convex_admin_key() -> Option<String> {
    env::var("CONVEX_ADMIN_KEY").ok()
}

pub fn data_dir() -> PathBuf {
    env::var("NBA_HUB_DATA_DIR")
        .map(PathBuf::from)
        .unwrap_or_else(|_| PathBuf::from("data"))
}

pub fn raw_data_dir() -> PathBuf {
    data_dir().join("raw")
}

pub fn duckdb_path() -> PathBuf {
    env::var("DUCKDB_PATH")
        .map(PathBuf::from)
        .unwrap_or_else(|_| data_dir().join("nba.duckdb"))
}
