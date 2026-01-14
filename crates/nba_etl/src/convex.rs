use std::env;
use reqwest::Client;
use serde::Serialize;
use serde_json::Value;
use anyhow::{Result, Context};
use log::info;

pub struct ConvexClient {
    client: Client,
    url: String,
    admin_key: Option<String>,
}

impl ConvexClient {
    pub fn new() -> Result<Self> {
        let url = env::var("CONVEX_URL").unwrap_or_else(|_| "http://localhost:3210".to_string());
        let admin_key = env::var("CONVEX_ADMIN_KEY").ok();
        
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
            let text = response.text().await?;
            return Err(anyhow::anyhow!("Convex mutation failed: {}", text));
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
            let text = response.text().await?;
            return Err(anyhow::anyhow!("Convex query failed: {}", text));
        }

        let result: Value = response.json().await?;
        Ok(result)
    }
}
