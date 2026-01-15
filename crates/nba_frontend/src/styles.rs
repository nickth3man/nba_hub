pub const APP_STYLES: &str = r#"
:root {
  --bg: #f8fafc;
  --panel: #ffffff;
  --text: #0f172a;
  --muted: #475569;
  --border: #e2e8f0;
  --accent: #1d4ed8;
  --accent-soft: #e0e7ff;
  --callout-bg: #eef2ff;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: "Inter", "Segoe UI", sans-serif;
  color: var(--text);
  background: var(--bg);
}

a {
  color: var(--accent);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

nav {
  position: sticky;
  top: 0;
  z-index: 10;
  background: var(--panel);
  border-bottom: 1px solid var(--border);
}

nav .nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  gap: 20px;
}

nav .logo {
  font-weight: 700;
  color: var(--text);
}

nav .nav-links {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 0.95rem;
}

main {
  max-width: 1200px;
  margin: 0 auto;
  padding: 24px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.page-header h1 {
  margin: 0;
  font-size: 2rem;
}

.page-header p {
  margin: 0;
  color: var(--muted);
}

.callout {
  background: var(--callout-bg);
  border-left: 4px solid var(--accent);
  padding: 12px 16px;
  border-radius: 8px;
  color: var(--text);
}

.section {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-title {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.toc {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 12px 16px;
}

.table-container {
  overflow-x: auto;
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 8px;
}

table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
}

th,
td {
  padding: 8px 12px;
  border-bottom: 1px solid var(--border);
  text-align: left;
}

th {
  background: #f1f5f9;
  position: sticky;
  top: 0;
  z-index: 1;
}

tr:hover {
  background: #f8fafc;
}

.num {
  text-align: right;
  font-variant-numeric: tabular-nums;
}

.badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: var(--accent-soft);
  color: var(--text);
  border-radius: 999px;
  padding: 2px 10px;
  font-size: 0.8rem;
}

.control-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}

.input {
  padding: 8px 12px;
  border: 1px solid #cbd5f5;
  border-radius: 6px;
  background: var(--panel);
  min-width: 200px;
}

.toggle {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
}

.card {
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.footer-note {
  color: var(--muted);
  font-size: 0.85rem;
}

.tooltip {
  text-decoration: underline dotted;
  text-underline-offset: 4px;
}
"#;
