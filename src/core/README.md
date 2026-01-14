# Core Infrastructure

This directory contains the foundational code for the application.

## Modules

- **`config.py`**: Central configuration file. Defines file paths (`DATA_DIR`, `DB_PATH`) and other global settings.
- **`database.py`**: Manages the DuckDB connection. Provides helper functions like `get_db_connection()`, `query_db()`, and `execute_db()`.
- **`utils.py`**: Core utility functions used across the application.

## Usage

Import these modules in other parts of the application to ensure consistent access to resources.

```python
from src.core.config import DB_PATH
from src.core.database import get_db_connection

con = get_db_connection()
```
