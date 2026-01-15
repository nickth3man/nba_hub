use reqwest::Client;
use serde::Serialize;
use serde_json::Value;
use anyhow::Result;
use log::info;
use nba_core::config;

#[derive(Debug)]
pub struct ConvexError {
    status: u16,
    body: String,
}

impl ConvexError {
    pub fn new(status: u16, body: String) -> Self {
        Self { status, body }
    }

    pub fn is_payload_limit(&self) -> bool {
        self.status == 413 || self.body.to_lowercase().contains("limit")
    }
}

impl std::fmt::Display for ConvexError {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(f, "Convex request failed (status {}): {}", self.status, self.body)
    }
}

impl std::error::Error for ConvexError {}

pub struct ConvexClient {
    client: Client,
    url: String,
    admin_key: Option<String>,
}

impl ConvexClient {
    pub fn new() -> Result<Self> {
        let url = config::convex_url();
        let admin_key = config::convex_admin_key();
        
        info!("Using Convex URL: {}", url);
        if admin_key.is_some() {
            info!("Convex Admin Key found");
        } else {
            info!("No Convex Admin Key found (running in public/dev mode)");
        }

        Ok(Self {
            client: Client::new(),
            url,
            admin_key,
        })
    }

    pub async fn mutation<T: Serialize>(&self, function: &str, args: &T) -> Result<Value> {
        let url = format!("{}/api/mutation", self.url);
        
        let body = serde_json::json!({
            "path": function,
            "args": args
        });

        let mut request = self.client.post(&url)
            .header("Content-Type", "application/json");

        if let Some(key) = &self.admin_key {
            // Convex expects "Convex <key>" for admin auth
            request = request.header("Authorization", format!("Convex {}", key));
        }

        let response = request
            .json(&body)
            .send()
            .await?;

        if !response.status().is_success() {
            let status = response.status().as_u16();
            let text = response.text().await.unwrap_or_default();
            return Err(ConvexError::new(status, text).into());
        }

        let result: Value = response.json().await?;
        info!("Successfully called mutation {}", function);
        Ok(result)
    }

    #[allow(dead_code)]
    pub async fn query<T: Serialize>(&self, function: &str, args: &T) -> Result<Value> {
        let url = format!("{}/api/query", self.url);
        
        let body = serde_json::json!({
            "path": function,
            "args": args
        });

        let mut request = self.client.post(&url)
            .header("Content-Type", "application/json");

        if let Some(key) = &self.admin_key {
            request = request.header("Authorization", format!("Convex {}", key));
        }

        let response = request
            .json(&body)
            .send()
            .await?;

        if !response.status().is_success() {
            let status = response.status().as_u16();
            let text = response.text().await.unwrap_or_default();
            return Err(ConvexError::new(status, text).into());
        }

        let result: Value = response.json().await?;
        Ok(result)
    }
}
