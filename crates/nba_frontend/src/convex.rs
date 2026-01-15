use gloo_net::http::Request;
use serde::de::DeserializeOwned;
use serde_json::Value;

pub async fn convex_query<T: DeserializeOwned>(path: &str, args: Value) -> Result<T, String> {
    let url = format!("{}/api/query", convex_url());
    let payload = serde_json::json!({ "path": path, "args": args });
    let response = Request::post(&url)
        .json(&payload)
        .map_err(|err| err.to_string())?
        .send()
        .await
        .map_err(|err| err.to_string())?;

    let value: Value = response.json().await.map_err(|err| err.to_string())?;
    let status = value
        .get("status")
        .and_then(|status| status.as_str())
        .unwrap_or("error");
    if status != "success" {
        let message = value
            .get("errorMessage")
            .and_then(|msg| msg.as_str())
            .unwrap_or("Convex query failed");
        return Err(message.to_string());
    }

    let payload = value
        .get("value")
        .cloned()
        .ok_or_else(|| "Convex response missing value".to_string())?;
    serde_json::from_value(payload).map_err(|err| err.to_string())
}

fn convex_url() -> String {
    option_env!("CONVEX_URL")
        .unwrap_or("http://localhost:3210")
        .to_string()
}
