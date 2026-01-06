#!/usr/bin/env python3
"""
NBA Database Analyzer
Comprehensive analysis of nba.duckdb database

Usage:
    python analyze_database.py --phase all
    python analyze_database.py --phase 1
    python analyze_database.py --table team_game_stats
"""

import duckdb
import pandas as pd
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import sys

# Configuration
DB_PATH = Path(r"c:\Users\nicolas\Documents\GitHub\nba_hub\nba.duckdb")
OUTPUT_DIR = Path(
    r"c:\Users\nicolas\Documents\GitHub\nba_hub\nba_database_documentation"
)
DATA_DIR = OUTPUT_DIR / "data"
SQL_DIR = OUTPUT_DIR / "sql_queries"


class NBADatabaseAnalyzer:
    """Comprehensive analyzer for NBA DuckDB database"""

    def __init__(self, db_path=DB_PATH):
        print(f"Connecting to database: {db_path}")
        try:
            self.conn = duckdb.connect(str(db_path), read_only=True)
            print("[OK] Connected successfully")
        except Exception as e:
            print(f"[ERROR] Failed to connect: {e}")
            sys.exit(1)

        self.output_dir = OUTPUT_DIR
        self.data_dir = DATA_DIR
        self.sql_dir = SQL_DIR

        # Create directories if they don't exist
        self.output_dir.mkdir(exist_ok=True)
        self.data_dir.mkdir(exist_ok=True)
        self.sql_dir.mkdir(exist_ok=True)

        # Cache for metadata
        self.tables_cache = None
        self.columns_cache = None

    def _cache_metadata(self):
        """Cache database metadata for faster access"""
        if self.tables_cache is None:
            print("Caching database metadata...")
            self.tables_cache = self.conn.execute("""
                SELECT table_name, table_type
                FROM information_schema.tables
                WHERE table_schema = 'main'
                ORDER BY table_type, table_name
            """).fetchdf()

            self.columns_cache = self.conn.execute("""
                SELECT table_name, column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_schema = 'main'
                ORDER BY table_name, ordinal_position
            """).fetchdf()
            print(
                f"[OK] Cached {len(self.tables_cache)} tables and {len(self.columns_cache)} columns"
            )

    # ============================================================================
    # PHASE 1: STRUCTURAL INVENTORY
    # ============================================================================

    def run_phase_1(self):
        """Phase 1: Structural Inventory"""
        print("\n" + "=" * 80)
        print("PHASE 1: STRUCTURAL INVENTORY")
        print("=" * 80 + "\n")

        self._cache_metadata()

        # Get all tables and views
        tables_info = self.get_tables_and_views()

        # Get row counts
        print("\nGetting row counts for all tables...")
        row_counts = self.get_row_counts()

        # Get constraints
        print("\nExtracting constraints...")
        constraints = self.get_constraints()

        # Get indexes
        print("\nExtracting indexes...")
        indexes = self.get_indexes()

        # Get view definitions
        print("\nExtracting view definitions...")
        views = self.get_view_definitions()

        # Check for custom functions
        print("\nChecking for custom functions...")
        functions = self.get_custom_functions()

        # Generate documentation
        print("\nGenerating structural inventory documentation...")
        self.generate_structural_docs(
            tables_info, row_counts, constraints, indexes, views, functions
        )

        # Save CSV outputs
        print("\nSaving table inventory CSV...")
        self.save_table_inventory(tables_info, row_counts)

        print("\n[OK] Phase 1 complete!")
        return {
            "tables": tables_info,
            "row_counts": row_counts,
            "constraints": constraints,
            "indexes": indexes,
            "views": views,
            "functions": functions,
        }

    def get_tables_and_views(self):
        """Get all tables and views with metadata"""
        print("Getting tables and views...")
        tables = self.tables_cache.copy()

        # Add column counts
        col_counts = (
            self.columns_cache.groupby("table_name")
            .size()
            .reset_index(name="column_count")
        )
        tables = tables.merge(col_counts, on="table_name", how="left")

        # Categorize by layer
        def categorize_layer(name):
            if "_raw" in name:
                return "raw"
            elif "_silver" in name:
                return "silver"
            elif "_gold" in name:
                return "gold"
            else:
                return "base"

        tables["layer"] = tables["table_name"].apply(categorize_layer)

        print(f"  Found {len(tables)} objects:")
        print(f"    - Tables: {len(tables[tables['table_type'] == 'BASE TABLE'])}")
        print(f"    - Views: {len(tables[tables['table_type'] == 'VIEW'])}")

        return tables

    def get_row_counts(self):
        """Get row counts for all tables"""
        base_tables = self.tables_cache[self.tables_cache["table_type"] == "BASE TABLE"]

        row_counts = []
        for idx, row in base_tables.iterrows():
            table_name = row["table_name"]
            try:
                count = self.conn.execute(
                    f'SELECT COUNT(*) FROM "{table_name}"'
                ).fetchone()[0]
                row_counts.append({"table_name": table_name, "row_count": count})
                print(f"  {table_name}: {count:,} rows")
            except Exception as e:
                print(f"  {table_name}: ERROR - {e}")
                row_counts.append({"table_name": table_name, "row_count": None})

        return pd.DataFrame(row_counts)

    def get_constraints(self):
        """Get all constraints"""
        try:
            constraints = self.conn.execute("""
                SELECT
                    table_name,
                    constraint_type,
                    constraint_text,
                    constraint_column_names,
                    constraint_index
                FROM duckdb_constraints()
                WHERE schema_name = 'main'
                ORDER BY table_name, constraint_index
            """).fetchdf()

            print(f"  Found {len(constraints)} constraints")
            print(
                f"    - PRIMARY KEY: {len(constraints[constraints['constraint_type'] == 'PRIMARY KEY'])}"
            )
            print(
                f"    - FOREIGN KEY: {len(constraints[constraints['constraint_type'] == 'FOREIGN KEY'])}"
            )
            print(
                f"    - NOT NULL: {len(constraints[constraints['constraint_type'] == 'NOT NULL'])}"
            )

            return constraints
        except Exception as e:
            print(f"  Error getting constraints: {e}")
            return pd.DataFrame()

    def get_indexes(self):
        """Get all indexes"""
        try:
            indexes = self.conn.execute("""
                SELECT
                    table_name,
                    index_name,
                    is_unique,
                    is_primary,
                    expressions,
                    sql
                FROM duckdb_indexes()
                WHERE schema_name = 'main'
                ORDER BY table_name, index_name
            """).fetchdf()

            print(f"  Found {len(indexes)} indexes")

            return indexes
        except Exception as e:
            print(f"  Error getting indexes: {e}")
            return pd.DataFrame()

    def get_view_definitions(self):
        """Get view definitions"""
        try:
            views = self.conn.execute("""
                SELECT
                    table_name,
                    view_definition
                FROM information_schema.views
                WHERE table_schema = 'main'
                ORDER BY table_name
            """).fetchdf()

            print(f"  Found {len(views)} view definitions")

            return views
        except Exception as e:
            print(f"  Error getting views: {e}")
            return pd.DataFrame()

    def get_custom_functions(self):
        """Check for custom functions and macros"""
        try:
            functions = self.conn.execute("""
                SELECT
                    function_name,
                    function_type,
                    return_type,
                    parameters,
                    parameter_types,
                    macro_definition
                FROM duckdb_functions()
                WHERE schema_name = 'main'
                    AND function_type IN ('macro', 'scalar', 'aggregate')
                    AND internal = false
                ORDER BY function_name
            """).fetchdf()

            print(f"  Found {len(functions)} custom functions/macros")

            return functions
        except Exception as e:
            print(f"  Error getting functions: {e}")
            return pd.DataFrame()

    def generate_structural_docs(
        self, tables, row_counts, constraints, indexes, views, functions
    ):
        """Generate Phase 1 documentation"""
        doc_path = self.output_dir / "01_structural_inventory.md"

        with open(doc_path, "w") as f:
            f.write("# NBA Database - Structural Inventory\n\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

            # Summary
            f.write("## Summary\n\n")
            total_rows = row_counts["row_count"].sum() if len(row_counts) > 0 else 0
            f.write(
                f"- **Total Tables**: {len(tables[tables['table_type'] == 'BASE TABLE'])}\n"
            )
            f.write(
                f"- **Total Views**: {len(tables[tables['table_type'] == 'VIEW'])}\n"
            )
            f.write(f"- **Total Rows**: {total_rows:,}\n")
            f.write(f"- **Total Constraints**: {len(constraints)}\n")
            f.write(f"- **Total Indexes**: {len(indexes)}\n")
            f.write(f"- **Custom Functions**: {len(functions)}\n\n")

            # Tables by layer
            f.write("## Tables by Layer\n\n")
            for layer in ["raw", "silver", "gold", "base"]:
                layer_tables = tables[tables["layer"] == layer]
                if len(layer_tables) > 0:
                    f.write(
                        f"### {layer.upper()} Layer ({len(layer_tables)} tables)\n\n"
                    )
                    for _, row in layer_tables.iterrows():
                        table_name = row["table_name"]
                        table_type = row["table_type"]
                        col_count = row.get("column_count", "N/A")

                        # Get row count if available
                        row_count_data = row_counts[
                            row_counts["table_name"] == table_name
                        ]
                        if (
                            len(row_count_data) > 0
                            and row_count_data.iloc[0]["row_count"] is not None
                        ):
                            rc = row_count_data.iloc[0]["row_count"]
                            f.write(
                                f"- **{table_name}** ({table_type}): {col_count} columns, {rc:,} rows\n"
                            )
                        else:
                            f.write(
                                f"- **{table_name}** ({table_type}): {col_count} columns\n"
                            )
                    f.write("\n")

            # Detailed schemas
            f.write("## Detailed Table Schemas\n\n")
            for _, table_row in tables.iterrows():
                table_name = table_row["table_name"]
                f.write(f"### {table_name}\n\n")

                # Columns
                cols = self.columns_cache[
                    self.columns_cache["table_name"] == table_name
                ]
                if len(cols) > 0:
                    f.write("| Column | Type | Nullable | Default |\n")
                    f.write("|--------|------|----------|---------|\n")
                    for _, col in cols.iterrows():
                        nullable = "YES" if col["is_nullable"] == "YES" else "NO"
                        default = (
                            col["column_default"] if col["column_default"] else "-"
                        )
                        f.write(
                            f"| {col['column_name']} | {col['data_type']} | {nullable} | {default} |\n"
                        )
                    f.write("\n")

                # Constraints for this table
                table_constraints = constraints[constraints["table_name"] == table_name]
                if len(table_constraints) > 0:
                    f.write("**Constraints:**\n")
                    for _, constraint in table_constraints.iterrows():
                        f.write(
                            f"- {constraint['constraint_type']}: {constraint['constraint_text']}\n"
                        )
                    f.write("\n")

                # Indexes for this table
                table_indexes = indexes[indexes["table_name"] == table_name]
                if len(table_indexes) > 0:
                    f.write("**Indexes:**\n")
                    for _, idx in table_indexes.iterrows():
                        unique_str = "UNIQUE" if idx["is_unique"] else ""
                        primary_str = "PRIMARY" if idx["is_primary"] else ""
                        f.write(f"- {idx['index_name']} {unique_str} {primary_str}\n")
                    f.write("\n")

            # Views
            if len(views) > 0:
                f.write("## View Definitions\n\n")
                for _, view in views.iterrows():
                    f.write(f"### {view['table_name']}\n\n")
                    f.write("```sql\n")
                    f.write(str(view["view_definition"]))
                    f.write("\n```\n\n")

            # Custom functions
            if len(functions) > 0:
                f.write("## Custom Functions/Macros\n\n")
                for _, func in functions.iterrows():
                    f.write(
                        f"### {func['function_name']} ({func['function_type']})\n\n"
                    )
                    f.write(f"- **Return Type**: {func['return_type']}\n")
                    if func["macro_definition"]:
                        f.write(f"- **Definition**: `{func['macro_definition']}`\n")
                    f.write("\n")

        print(f"  Saved documentation to: {doc_path}")

    def save_table_inventory(self, tables, row_counts):
        """Save table inventory as CSV"""
        inventory = tables.merge(row_counts, on="table_name", how="left")
        csv_path = self.data_dir / "table_inventory.csv"
        inventory.to_csv(csv_path, index=False)
        print(f"  Saved inventory to: {csv_path}")

    # ============================================================================
    # PHASE 2: STATISTICAL PROFILING
    # ============================================================================

    def run_phase_2(self):
        """Phase 2: Statistical Profiling"""
        print("\n" + "=" * 80)
        print("PHASE 2: STATISTICAL PROFILING")
        print("=" * 80 + "\n")

        self._cache_metadata()

        all_stats = []
        base_tables = self.tables_cache[self.tables_cache["table_type"] == "BASE TABLE"]

        for idx, table_row in base_tables.iterrows():
            table_name = table_row["table_name"]
            print(f"\nProfiling table: {table_name} ({idx + 1}/{len(base_tables)})")

            # Check row count first
            try:
                row_count = self.conn.execute(
                    f'SELECT COUNT(*) FROM "{table_name}"'
                ).fetchone()[0]
                if row_count == 0:
                    print("  Skipping (empty table)")
                    continue

                print(f"  {row_count:,} rows")

                # Try SUMMARIZE first for quick overview
                try:
                    self.conn.execute(f'SUMMARIZE "{table_name}"').fetchdf()
                    print("  [OK] SUMMARIZE complete")
                except Exception as e:
                    print(f"  SUMMARIZE failed: {e}")

                # Profile each column
                cols = self.columns_cache[
                    self.columns_cache["table_name"] == table_name
                ]
                for _, col in cols.iterrows():
                    column_name = col["column_name"]
                    data_type = col["data_type"]

                    try:
                        stats = self.profile_column(
                            table_name, column_name, data_type, row_count
                        )
                        all_stats.append(stats)
                        print(f"    [OK] {column_name} ({data_type})")
                    except Exception as e:
                        print(f"    [ERROR] {column_name}: {e}")

            except Exception as e:
                print(f"  Error: {e}")

        # Save results
        print("\nSaving profiling results...")
        stats_df = pd.DataFrame(all_stats)
        csv_path = self.data_dir / "column_statistics.csv"
        stats_df.to_csv(csv_path, index=False)
        print(f"  Saved to: {csv_path}")

        # Generate documentation
        print("\nGenerating statistical profile documentation...")
        self.generate_statistical_docs(stats_df)

        print("\n[OK] Phase 2 complete!")
        return stats_df

    def profile_column(self, table_name, column_name, data_type, total_rows):
        """Profile a single column with type-specific analysis"""
        stats = {
            "table": table_name,
            "column": column_name,
            "data_type": data_type,
            "total_rows": total_rows,
        }

        # Basic stats
        result = self.conn.execute(f"""
            SELECT
                COUNT("{column_name}") as non_null_count,
                COUNT(*) - COUNT("{column_name}") as null_count,
                ROUND(100.0 * (COUNT(*) - COUNT("{column_name}")) / COUNT(*), 2) as null_percentage
            FROM "{table_name}"
        """).fetchone()

        stats["non_null_count"] = result[0]
        stats["null_count"] = result[1]
        stats["null_percentage"] = result[2]

        # Cardinality
        if total_rows > 100000:
            # Use approximate for large tables
            distinct = self.conn.execute(
                f'SELECT approx_count_distinct("{column_name}") FROM "{table_name}"'
            ).fetchone()[0]
        else:
            distinct = self.conn.execute(
                f'SELECT COUNT(DISTINCT "{column_name}") FROM "{table_name}"'
            ).fetchone()[0]

        stats["distinct_count"] = distinct
        stats["cardinality_ratio"] = (
            round(100.0 * distinct / total_rows, 2) if total_rows > 0 else 0
        )

        # Type-specific analysis
        if data_type in ["BIGINT", "INTEGER", "DOUBLE", "FLOAT", "DECIMAL", "HUGEINT"]:
            stats.update(
                self.profile_numeric_column(
                    table_name, column_name, stats["non_null_count"]
                )
            )
        elif data_type in ["VARCHAR", "TEXT"]:
            stats.update(self.profile_text_column(table_name, column_name))
        elif data_type == "DATE":
            stats.update(self.profile_date_column(table_name, column_name))
        elif data_type == "BOOLEAN":
            stats.update(
                self.profile_boolean_column(
                    table_name, column_name, stats["non_null_count"]
                )
            )

        return stats

    def profile_numeric_column(self, table_name, column_name, non_null_count):
        """Profile numeric column"""
        stats = {}

        if non_null_count == 0:
            return stats

        try:
            numeric_stats = self.conn.execute(f"""
                SELECT
                    MIN("{column_name}")::VARCHAR as min_val,
                    MAX("{column_name}")::VARCHAR as max_val,
                    AVG("{column_name}")::VARCHAR as mean_val,
                    MEDIAN("{column_name}")::VARCHAR as median_val,
                    STDDEV("{column_name}")::VARCHAR as stddev_val,
                    PERCENTILE_CONT(0.25) WITHIN GROUP (ORDER BY "{column_name}")::VARCHAR as q25,
                    PERCENTILE_CONT(0.75) WITHIN GROUP (ORDER BY "{column_name}")::VARCHAR as q75
                FROM "{table_name}"
                WHERE "{column_name}" IS NOT NULL
            """).fetchone()

            stats["min"] = numeric_stats[0]
            stats["max"] = numeric_stats[1]
            stats["mean"] = numeric_stats[2]
            stats["median"] = numeric_stats[3]
            stats["stddev"] = numeric_stats[4]
            stats["q25"] = numeric_stats[5]
            stats["q75"] = numeric_stats[6]

            # Outlier detection using IQR
            if numeric_stats[5] and numeric_stats[6]:
                try:
                    q25 = float(numeric_stats[5])
                    q75 = float(numeric_stats[6])
                    iqr = q75 - q25
                    lower_bound = q25 - 1.5 * iqr
                    upper_bound = q75 + 1.5 * iqr

                    outlier_count = self.conn.execute(f"""
                        SELECT COUNT(*)
                        FROM "{table_name}"
                        WHERE "{column_name}" IS NOT NULL
                            AND ("{column_name}" < {lower_bound} OR "{column_name}" > {upper_bound})
                    """).fetchone()[0]

                    stats["outlier_count"] = outlier_count
                    stats["outlier_percentage"] = round(
                        100.0 * outlier_count / non_null_count, 2
                    )
                except Exception:
                    pass
        except Exception as e:
            stats["error"] = str(e)

        return stats

    def profile_text_column(self, table_name, column_name):
        """Profile text column"""
        stats = {}

        try:
            text_stats = self.conn.execute(f"""
                SELECT
                    MIN(LENGTH("{column_name}")) as min_length,
                    MAX(LENGTH("{column_name}")) as max_length,
                    AVG(LENGTH("{column_name}"))::INTEGER as avg_length
                FROM "{table_name}"
                WHERE "{column_name}" IS NOT NULL
            """).fetchone()

            stats["min_length"] = text_stats[0]
            stats["max_length"] = text_stats[1]
            stats["avg_length"] = text_stats[2]
        except Exception as e:
            stats["error"] = str(e)

        return stats

    def profile_date_column(self, table_name, column_name):
        """Profile date column"""
        stats = {}

        try:
            date_stats = self.conn.execute(f"""
                SELECT
                    MIN("{column_name}")::VARCHAR as min_date,
                    MAX("{column_name}")::VARCHAR as max_date,
                    COUNT(DISTINCT "{column_name}") as unique_dates
                FROM "{table_name}"
                WHERE "{column_name}" IS NOT NULL
            """).fetchone()

            stats["min_date"] = date_stats[0]
            stats["max_date"] = date_stats[1]
            stats["unique_dates"] = date_stats[2]
        except Exception as e:
            stats["error"] = str(e)

        return stats

    def profile_boolean_column(self, table_name, column_name, non_null_count):
        """Profile boolean column"""
        stats = {}

        if non_null_count == 0:
            return stats

        try:
            bool_stats = self.conn.execute(f"""
                SELECT
                    SUM(CASE WHEN "{column_name}" = true THEN 1 ELSE 0 END) as true_count,
                    SUM(CASE WHEN "{column_name}" = false THEN 1 ELSE 0 END) as false_count
                FROM "{table_name}"
                WHERE "{column_name}" IS NOT NULL
            """).fetchone()

            stats["true_count"] = bool_stats[0]
            stats["false_count"] = bool_stats[1]
            stats["true_percentage"] = round(100.0 * bool_stats[0] / non_null_count, 2)
        except Exception as e:
            stats["error"] = str(e)

        return stats

    def generate_statistical_docs(self, stats_df):
        """Generate Phase 2 documentation"""
        doc_path = self.output_dir / "02_statistical_profile.md"

        with open(doc_path, "w") as f:
            f.write("# NBA Database - Statistical Profile\n\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

            f.write("## Summary\n\n")
            f.write(f"- **Total Columns Profiled**: {len(stats_df)}\n")
            f.write(f"- **Total Tables**: {stats_df['table'].nunique()}\n\n")

            # Group by table
            for table_name in sorted(stats_df["table"].unique()):
                f.write(f"## {table_name}\n\n")

                table_stats = stats_df[stats_df["table"] == table_name]

                # Summary table
                f.write(
                    "| Column | Type | Distinct | NULL % | Min | Max | Mean | Median |\n"
                )
                f.write(
                    "|--------|------|----------|--------|-----|-----|------|--------|\n"
                )

                for _, row in table_stats.iterrows():
                    col_name = row["column"]
                    dtype = row["data_type"]
                    distinct = row.get("distinct_count", "-")
                    null_pct = row.get("null_percentage", "-")
                    min_val = row.get(
                        "min", row.get("min_date", row.get("min_length", "-"))
                    )
                    max_val = row.get(
                        "max", row.get("max_date", row.get("max_length", "-"))
                    )
                    mean_val = row.get("mean", "-")
                    median_val = row.get("median", "-")

                    f.write(
                        f"| {col_name} | {dtype} | {distinct} | {null_pct} | {min_val} | {max_val} | {mean_val} | {median_val} |\n"
                    )

                f.write("\n")

        print(f"  Saved documentation to: {doc_path}")

    # ============================================================================
    # PHASE 3: SEMANTIC & RELATIONAL ANALYSIS
    # ============================================================================

    def run_phase_3(self):
        """Phase 3: Semantic & Relational Analysis"""
        print("\n" + "=" * 80)
        print("PHASE 3: SEMANTIC & RELATIONAL ANALYSIS")
        print("=" * 80 + "\n")

        self._cache_metadata()

        # Find potential relationships
        print("Finding potential relationships...")
        relationships = self.find_potential_relationships()

        # Test relationships
        print("\nTesting relationship integrity...")
        tested_relationships = self.test_relationships(relationships)

        # Sample data from tables
        print("\nSampling data from tables...")
        samples = self.sample_tables()

        # Generate documentation
        print("\nGenerating semantic analysis documentation...")
        self.generate_semantic_docs(tested_relationships, samples)

        # Save relationship matrix
        if len(tested_relationships) > 0:
            csv_path = self.data_dir / "relationship_matrix.csv"
            pd.DataFrame(tested_relationships).to_csv(csv_path, index=False)
            print(f"  Saved relationships to: {csv_path}")

        print("\n[OK] Phase 3 complete!")
        return tested_relationships

    def find_potential_relationships(self):
        """Find potential FK relationships from column names"""
        # Get all columns ending in _id or _key
        id_columns = self.columns_cache[
            self.columns_cache["column_name"].str.contains(
                "_id$|_key$|^id$", regex=True, case=False
            )
        ]

        # Group by column name
        column_map = defaultdict(list)
        for _, row in id_columns.iterrows():
            column_map[row["column_name"]].append(row["table_name"])

        # Find columns appearing in multiple tables
        relationships = []
        for col_name, tables in column_map.items():
            if len(tables) > 1:
                print(f"  {col_name}: appears in {len(tables)} tables")
                relationships.append({"column_name": col_name, "tables": tables})

        return relationships

    def test_relationships(self, relationships):
        """Test referential integrity for discovered relationships"""
        tested = []

        # Common NBA relationships to test
        known_relationships = [
            ("team_game_stats", "team_id", "team", "id"),
            ("team_game_stats", "game_id", "games", "game_id"),
            ("player_game_stats", "game_id", "games", "game_id"),
            ("common_player_info", "team_id", "team", "id"),
        ]

        for fk_table, fk_col, pk_table, pk_col in known_relationships:
            # Check if both tables exist
            if (
                fk_table in self.tables_cache["table_name"].values
                and pk_table in self.tables_cache["table_name"].values
            ):
                try:
                    result = self.test_foreign_key(fk_table, fk_col, pk_table, pk_col)
                    tested.append(result)
                    print(
                        f"  {fk_table}.{fk_col} -> {pk_table}.{pk_col}: {result['integrity_percentage']}%"
                    )
                except Exception as e:
                    print(f"  {fk_table}.{fk_col} -> {pk_table}.{pk_col}: Error - {e}")

        return tested

    def test_foreign_key(self, fk_table, fk_column, pk_table, pk_column):
        """Test if all FK values exist in PK table"""
        orphan_count = self.conn.execute(f"""
            SELECT COUNT(*) as orphan_count
            FROM "{fk_table}" fk
            WHERE fk."{fk_column}" IS NOT NULL
                AND NOT EXISTS (
                    SELECT 1
                    FROM "{pk_table}" pk
                    WHERE pk."{pk_column}" = fk."{fk_column}"
                )
        """).fetchone()[0]

        total = self.conn.execute(f"""
            SELECT COUNT(*)
            FROM "{fk_table}"
            WHERE "{fk_column}" IS NOT NULL
        """).fetchone()[0]

        return {
            "fk_table": fk_table,
            "fk_column": fk_column,
            "pk_table": pk_table,
            "pk_column": pk_column,
            "orphan_count": orphan_count,
            "total_count": total,
            "integrity_percentage": round(100.0 * (total - orphan_count) / total, 2)
            if total > 0
            else 100,
        }

    def sample_tables(self):
        """Get sample data from each table"""
        samples = {}
        base_tables = self.tables_cache[self.tables_cache["table_type"] == "BASE TABLE"]

        for _, table_row in base_tables.iterrows():
            table_name = table_row["table_name"]

            try:
                # Check if table has data
                row_count = self.conn.execute(
                    f'SELECT COUNT(*) FROM "{table_name}"'
                ).fetchone()[0]
                if row_count == 0:
                    continue

                # Get sample
                sample_df = self.conn.execute(f"""
                    SELECT *
                    FROM "{table_name}"
                    USING SAMPLE 5 ROWS
                """).fetchdf()

                samples[table_name] = sample_df
                print(f"  {table_name}: {len(sample_df)} sample rows")
            except Exception as e:
                print(f"  {table_name}: Error - {e}")

        return samples

    def generate_semantic_docs(self, relationships, samples):
        """Generate Phase 3 documentation"""
        doc_path = self.output_dir / "03_semantic_analysis.md"

        with open(doc_path, "w") as f:
            f.write("# NBA Database - Semantic & Relational Analysis\n\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

            # Relationships
            f.write("## Discovered Relationships\n\n")
            if len(relationships) > 0:
                f.write(
                    "| FK Table | FK Column | PK Table | PK Column | Total Records | Orphans | Integrity % |\n"
                )
                f.write(
                    "|----------|-----------|----------|-----------|---------------|---------|-------------|\n"
                )

                for rel in relationships:
                    f.write(
                        f"| {rel['fk_table']} | {rel['fk_column']} | {rel['pk_table']} | {rel['pk_column']} | "
                    )
                    f.write(
                        f"{rel['total_count']:,} | {rel['orphan_count']:,} | {rel['integrity_percentage']}% |\n"
                    )
            else:
                f.write("No relationships tested.\n")

            f.write("\n")

            # Sample data
            f.write("## Sample Data\n\n")
            for table_name, sample_df in samples.items():
                f.write(f"### {table_name}\n\n")
                # Convert to string and replace NA for markdown compatibility
                sample_to_show = sample_df.head().astype(str).replace('<NA>', '-')
                f.write(sample_to_show.to_markdown(index=False))
                f.write("\n\n")

        print(f"  Saved documentation to: {doc_path}")

        # Also generate NBA glossary
        self.generate_nba_glossary()

    def generate_nba_glossary(self):
        """Generate NBA terminology glossary"""
        doc_path = self.output_dir / "06_nba_glossary.md"

        glossary = {
            # Advanced metrics
            "per": "Player Efficiency Rating - Overall efficiency measure, league average = 15.0",
            "ts_pct": "True Shooting Percentage - Points / (2 × (FGA + 0.44 × FTA))",
            "usg_pct": "Usage Percentage - Share of team plays used by player",
            "efg_pct": "Effective Field Goal % - (FGM + 0.5 × 3PM) / FGA",
            "ws": "Win Shares - Estimate of wins contributed by player",
            "ws_48": "Win Shares per 48 minutes",
            "bpm": "Box Plus-Minus - Points per 100 possessions vs league average",
            "obpm": "Offensive Box Plus-Minus",
            "dbpm": "Defensive Box Plus-Minus",
            "vorp": "Value Over Replacement Player",
            # Traditional stats
            "fgm": "Field Goals Made",
            "fga": "Field Goals Attempted",
            "fg_pct": "Field Goal Percentage",
            "fg3m": "3-Point Field Goals Made",
            "fg3a": "3-Point Field Goals Attempted",
            "fg3_pct": "3-Point Field Goal Percentage",
            "ftm": "Free Throws Made",
            "fta": "Free Throws Attempted",
            "ft_pct": "Free Throw Percentage",
            "oreb": "Offensive Rebounds",
            "dreb": "Defensive Rebounds",
            "reb": "Total Rebounds",
            "ast": "Assists",
            "stl": "Steals",
            "blk": "Blocks",
            "tov": "Turnovers",
            "pf": "Personal Fouls",
            "pts": "Points",
            "plus_minus": "Plus/Minus - Point differential while player is on court",
        }

        with open(doc_path, "w") as f:
            f.write("# NBA Statistics Glossary\n\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

            f.write("## Advanced Metrics\n\n")
            for term in [
                "per",
                "ts_pct",
                "usg_pct",
                "efg_pct",
                "ws",
                "ws_48",
                "bpm",
                "obpm",
                "dbpm",
                "vorp",
            ]:
                if term in glossary:
                    f.write(f"**{term.upper()}**: {glossary[term]}\n\n")

            f.write("## Traditional Statistics\n\n")
            for term in [
                "fgm",
                "fga",
                "fg_pct",
                "fg3m",
                "fg3a",
                "fg3_pct",
                "ftm",
                "fta",
                "ft_pct",
                "oreb",
                "dreb",
                "reb",
                "ast",
                "stl",
                "blk",
                "tov",
                "pf",
                "pts",
                "plus_minus",
            ]:
                if term in glossary:
                    f.write(f"**{term.upper()}**: {glossary[term]}\n\n")

            f.write("\n## Sources\n\n")
            f.write(
                "- [Basketball-Reference.com Glossary](https://www.basketball-reference.com/about/glossary.html)\n"
            )
            f.write(
                "- [NBA.com Stats Glossary](https://www.nba.com/stats/help/glossary)\n"
            )

        print(f"  Saved NBA glossary to: {doc_path}")

    # ============================================================================
    # PHASE 4: DATA QUALITY ASSESSMENT
    # ============================================================================

    def run_phase_4(self):
        """Phase 4: Data Quality Assessment"""
        print("\n" + "=" * 80)
        print("PHASE 4: DATA QUALITY ASSESSMENT")
        print("=" * 80 + "\n")

        self._cache_metadata()

        all_issues = []

        # Run integrity checks
        print("Running NBA-specific integrity checks...")
        integrity_issues = self.run_integrity_checks()
        all_issues.extend(integrity_issues)

        # Check for duplicates
        print("\nChecking for duplicates...")
        duplicate_issues = self.check_duplicates()
        all_issues.extend(duplicate_issues)

        # Generate documentation
        print("\nGenerating data quality report...")
        self.generate_quality_docs(all_issues)

        # Save issues CSV
        if len(all_issues) > 0:
            csv_path = self.data_dir / "quality_issues.csv"
            pd.DataFrame(all_issues).to_csv(csv_path, index=False)
            print(f"  Saved quality issues to: {csv_path}")

        print("\n[OK] Phase 4 complete!")
        return all_issues

    def run_integrity_checks(self):
        """Run NBA-specific business rule checks"""
        issues = []

        checks = [
            {
                "name": "Invalid player ages",
                "severity": "HIGH",
                "table": "common_player_info",
                "sql": """
                    SELECT 'common_player_info' as table_name,
                           'age' as column_name,
                           COUNT(*) as violation_count
                    FROM common_player_info
                    WHERE age < 18 OR age > 50
                """,
            },
            {
                "name": "Negative points",
                "severity": "CRITICAL",
                "table": "team_game_stats",
                "sql": """
                    SELECT 'team_game_stats' as table_name,
                           'pts' as column_name,
                           COUNT(*) as violation_count
                    FROM team_game_stats
                    WHERE pts < 0
                """,
            },
            {
                "name": "Field goals made > attempted",
                "severity": "CRITICAL",
                "table": "team_game_stats",
                "sql": """
                    SELECT 'team_game_stats' as table_name,
                           'fgm_fga' as column_name,
                           COUNT(*) as violation_count
                    FROM team_game_stats
                    WHERE fgm > fga
                """,
            },
        ]

        for check in checks:
            # Check if table exists
            if check["table"] not in self.tables_cache["table_name"].values:
                continue

            try:
                result = self.conn.execute(check["sql"]).fetchone()
                if result and result[2] > 0:  # violation_count
                    issues.append(
                        {
                            "check_name": check["name"],
                            "severity": check["severity"],
                            "table": check["table"],
                            "violation_count": result[2],
                        }
                    )
                    print(f"  [WARNING] {check['name']}: {result[2]} violations")
                else:
                    print(f"  [OK] {check['name']}: No issues")
            except Exception as e:
                print(f"  [ERROR] {check['name']}: Error - {e}")

        return issues

    def check_duplicates(self):
        """Check for duplicate rows"""
        issues = []

        # Only check a few key tables to avoid long execution
        key_tables = ["team", "games", "common_player_info"]

        for table_name in key_tables:
            if table_name not in self.tables_cache["table_name"].values:
                continue

            try:
                # Get all columns
                cols = self.columns_cache[
                    self.columns_cache["table_name"] == table_name
                ]
                col_list = ", ".join([f'"{col}"' for col in cols["column_name"]])

                # Find duplicates
                duplicate_count = self.conn.execute(f"""
                    SELECT COUNT(*) FROM (
                        SELECT {col_list}, COUNT(*) as dup_count
                        FROM "{table_name}"
                        GROUP BY {col_list}
                        HAVING COUNT(*) > 1
                    )
                """).fetchone()[0]

                if duplicate_count > 0:
                    issues.append(
                        {
                            "check_name": "Full row duplicates",
                            "severity": "MEDIUM",
                            "table": table_name,
                            "violation_count": duplicate_count,
                        }
                    )
                    print(f"  [WARNING] {table_name}: {duplicate_count} duplicate row groups")
                else:
                    print(f"  [OK] {table_name}: No duplicates")
            except Exception as e:
                print(f"  [ERROR] {table_name}: Error - {e}")

        return issues

    def generate_quality_docs(self, issues):
        """Generate Phase 4 documentation"""
        doc_path = self.output_dir / "04_data_quality_report.md"

        with open(doc_path, "w") as f:
            f.write("# NBA Database - Data Quality Report\n\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

            f.write("## Summary\n\n")
            f.write(f"- **Total Issues Found**: {len(issues)}\n")

            if len(issues) > 0:
                severity_counts = pd.DataFrame(issues)["severity"].value_counts()
                for severity, count in severity_counts.items():
                    f.write(f"- **{severity}**: {count}\n")

            f.write("\n## Issues by Severity\n\n")

            if len(issues) > 0:
                for severity in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
                    severity_issues = [i for i in issues if i["severity"] == severity]
                    if severity_issues:
                        f.write(f"### {severity}\n\n")
                        f.write("| Check | Table | Violations |\n")
                        f.write("|-------|-------|------------|\n")
                        for issue in severity_issues:
                            f.write(
                                f"| {issue['check_name']} | {issue['table']} | {issue['violation_count']:,} |\n"
                            )
                        f.write("\n")
            else:
                f.write("No issues found.\n")

        print(f"  Saved documentation to: {doc_path}")

    # ============================================================================
    # PHASE 5: FINAL DELIVERABLE
    # ============================================================================

    def run_phase_5(self):
        """Phase 5: Generate Final Documentation"""
        print("\n" + "=" * 80)
        print("PHASE 5: FINAL DELIVERABLE")
        print("=" * 80 + "\n")

        self._cache_metadata()

        # Generate README
        print("Generating executive summary (README.md)...")
        self.generate_readme()

        # Generate ERD
        print("\nGenerating Entity-Relationship Diagram...")
        self.generate_erd()

        # Generate SQL query library
        print("\nGenerating SQL query library...")
        self.generate_sql_library()

        print("\n[OK] Phase 5 complete!")
        print("\n" + "=" * 80)
        print("ALL PHASES COMPLETE!")
        print("=" * 80)
        print(f"\nDocumentation available at: {self.output_dir}")

    def generate_readme(self):
        """Generate executive summary README"""
        doc_path = self.output_dir / "README.md"

        # Get summary stats
        try:
            row_counts = pd.read_csv(self.data_dir / "table_inventory.csv")
            total_rows = row_counts["row_count"].sum()
            total_tables = len(row_counts)
        except Exception:
            total_rows = 0
            total_tables = 0

        with open(doc_path, "w") as f:
            f.write("# NBA Database Documentation\n\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

            f.write("## Overview\n\n")
            f.write("- **Database Size**: 222 MB\n")
            f.write(f"- **Total Tables**: {total_tables}\n")
            f.write(f"- **Total Rows**: {total_rows:,}\n")
            f.write("- **Architecture**: Medallion (Raw -> Silver -> Gold)\n")
            f.write("- **Domain**: NBA basketball data\n\n")

            f.write("## Documentation Structure\n\n")
            f.write(
                "1. **[Structural Inventory](01_structural_inventory.md)** - Complete database schema\n"
            )
            f.write(
                "2. **[Statistical Profile](02_statistical_profile.md)** - Column-level statistics\n"
            )
            f.write(
                "3. **[Semantic Analysis](03_semantic_analysis.md)** - Relationships and sample data\n"
            )
            f.write(
                "4. **[Data Quality Report](04_data_quality_report.md)** - Quality issues and integrity checks\n"
            )
            f.write(
                "5. **[Entity-Relationship Diagram](05_er_diagram.md)** - Visual database structure\n"
            )
            f.write(
                "6. **[NBA Glossary](06_nba_glossary.md)** - Basketball terminology reference\n\n"
            )

            f.write("## Data Files\n\n")
            f.write("- `data/table_inventory.csv` - Table metadata\n")
            f.write("- `data/column_statistics.csv` - Column-level statistics\n")
            f.write("- `data/relationship_matrix.csv` - Tested relationships\n")
            f.write("- `data/quality_issues.csv` - Data quality issues\n\n")

            f.write("## SQL Queries\n\n")
            f.write("- `sql_queries/schema_queries.sql` - Schema inspection queries\n")
            f.write(
                "- `sql_queries/profiling_queries.sql` - Statistical profiling queries\n"
            )
            f.write("- `sql_queries/quality_checks.sql` - Data quality check queries\n")
            f.write(
                "- `sql_queries/relationship_queries.sql` - Relationship testing queries\n\n"
            )

            f.write("## Quick Start\n\n")
            f.write("```bash\n")
            f.write("# Install dependencies\n")
            f.write("pip install -r requirements.txt\n\n")
            f.write("# Run analysis\n")
            f.write("cd nba_database_documentation/scripts\n")
            f.write("python analyze_database.py --phase all\n")
            f.write("```\n")

        print(f"  Saved README to: {doc_path}")

    def generate_erd(self):
        """Generate MermaidJS Entity-Relationship Diagram"""
        doc_path = self.output_dir / "05_er_diagram.md"

        with open(doc_path, "w") as f:
            f.write("# NBA Database - Entity-Relationship Diagram\n\n")
            f.write(f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")

            f.write("## Core Tables ERD\n\n")
            f.write("```mermaid\nerDiagram\n")

            # Core tables
            core_tables = [
                "team",
                "games",
                "common_player_info",
                "team_game_stats",
                "player_game_stats",
            ]

            for table_name in core_tables:
                if table_name in self.tables_cache["table_name"].values:
                    cols = self.columns_cache[
                        self.columns_cache["table_name"] == table_name
                    ].head(10)

                    f.write(f"    {table_name} {{\n")
                    for _, col in cols.iterrows():
                        f.write(f"        {col['data_type']} {col['column_name']}\n")
                    f.write("    }\n")

            # Relationships
            f.write("    team ||--o{ team_game_stats : has\n")
            f.write("    games ||--o{ team_game_stats : contains\n")
            f.write("    games ||--o{ player_game_stats : contains\n")
            f.write("    common_player_info ||--o{ player_game_stats : plays\n")

            f.write("```\n\n")

            f.write("## Notes\n\n")
            f.write(
                "- This diagram shows core tables and their primary relationships\n"
            )
            f.write(
                "- Full database contains 75+ tables across raw, silver, and gold layers\n"
            )
            f.write(
                "- See [Semantic Analysis](03_semantic_analysis.md) for complete relationship details\n"
            )

        print(f"  Saved ERD to: {doc_path}")

    def generate_sql_library(self):
        """Generate reusable SQL query library"""

        # Schema queries
        schema_sql = self.sql_dir / "schema_queries.sql"
        with open(schema_sql, "w") as f:
            f.write("-- NBA Database Schema Queries\n")
            f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("-- List all tables and views\n")
            f.write("SELECT table_name, table_type\n")
            f.write("FROM information_schema.tables\n")
            f.write("WHERE table_schema = 'main'\n")
            f.write("ORDER BY table_type, table_name;\n\n")

            f.write("-- Get schema for a specific table\n")
            f.write("SELECT column_name, data_type, is_nullable, column_default\n")
            f.write("FROM information_schema.columns\n")
            f.write("WHERE table_name = 'team_game_stats'\n")  # Example
            f.write("ORDER BY ordinal_position;\n\n")

            f.write("-- Get all constraints\n")
            f.write("SELECT * FROM duckdb_constraints()\n")
            f.write("WHERE schema_name = 'main';\n\n")

            f.write("-- Get all indexes\n")
            f.write("SELECT * FROM duckdb_indexes()\n")
            f.write("WHERE schema_name = 'main';\n")

        # Profiling queries
        profiling_sql = self.sql_dir / "profiling_queries.sql"
        with open(profiling_sql, "w") as f:
            f.write("-- NBA Database Profiling Queries\n")
            f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("-- Quick profile with SUMMARIZE\n")
            f.write("SUMMARIZE team_game_stats;\n\n")

            f.write("-- Detailed column statistics\n")
            f.write("SELECT \n")
            f.write("    COUNT(*) as total_rows,\n")
            f.write("    COUNT(pts) as non_null_count,\n")
            f.write("    COUNT(DISTINCT pts) as distinct_count,\n")
            f.write("    MIN(pts) as min_value,\n")
            f.write("    MAX(pts) as max_value,\n")
            f.write("    AVG(pts) as mean_value,\n")
            f.write("    MEDIAN(pts) as median_value,\n")
            f.write("    STDDEV(pts) as std_dev\n")
            f.write("FROM team_game_stats;\n\n")

            f.write("-- Top 20 most common values\n")
            f.write("SELECT team_id, COUNT(*) as frequency\n")
            f.write("FROM team_game_stats\n")
            f.write("GROUP BY team_id\n")
            f.write("ORDER BY frequency DESC\n")
            f.write("LIMIT 20;\n")

        # Quality checks
        quality_sql = self.sql_dir / "quality_checks.sql"
        with open(quality_sql, "w") as f:
            f.write("-- NBA Database Quality Check Queries\n")
            f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("-- Find duplicate rows\n")
            f.write("SELECT *, COUNT(*) as dup_count\n")
            f.write("FROM team\n")
            f.write("GROUP BY ALL\n")
            f.write("HAVING COUNT(*) > 1;\n\n")

            f.write("-- Check for negative statistics\n")
            f.write("SELECT *\n")
            f.write("FROM team_game_stats\n")
            f.write("WHERE pts < 0 OR reb < 0 OR ast < 0;\n\n")

            f.write("-- Check FG made vs attempted\n")
            f.write("SELECT game_id, team_id, fgm, fga\n")
            f.write("FROM team_game_stats\n")
            f.write("WHERE fgm > fga;\n")

        # Relationship queries
        relationship_sql = self.sql_dir / "relationship_queries.sql"
        with open(relationship_sql, "w") as f:
            f.write("-- NBA Database Relationship Queries\n")
            f.write(f"-- Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

            f.write("-- Test FK relationship integrity\n")
            f.write("SELECT COUNT(*) as orphan_count\n")
            f.write("FROM team_game_stats\n")
            f.write("WHERE team_id IS NOT NULL\n")
            f.write("    AND team_id NOT IN (SELECT id FROM team);\n\n")

            f.write("-- Join teams with their game stats\n")
            f.write("SELECT t.full_name, tgs.*\n")
            f.write("FROM team t\n")
            f.write("JOIN team_game_stats tgs ON t.id = tgs.team_id\n")
            f.write("LIMIT 100;\n")

        print(f"  Saved SQL queries to: {self.sql_dir}")

    # ============================================================================
    # MAIN ORCHESTRATION
    # ============================================================================

    def run_all_phases(self):
        """Execute complete analysis"""
        print("\n" + "=" * 80)
        print("NBA DATABASE COMPREHENSIVE ANALYSIS")
        print("=" * 80)

        self.run_phase_1()
        self.run_phase_2()
        self.run_phase_3()
        self.run_phase_4()
        self.run_phase_5()

        print("\n" + "=" * 80)
        print("ANALYSIS COMPLETE!")
        print("=" * 80)
        print(f"\nDocumentation: {self.output_dir}")
        print(f"Data exports: {self.data_dir}")
        print(f"SQL queries: {self.sql_dir}")


def main():
    parser = argparse.ArgumentParser(description="Analyze NBA DuckDB database")
    parser.add_argument(
        "--phase",
        choices=["1", "2", "3", "4", "5", "all"],
        default="all",
        help="Which phase to run (default: all)",
    )

    args = parser.parse_args()

    analyzer = NBADatabaseAnalyzer()

    if args.phase == "all":
        analyzer.run_all_phases()
    elif args.phase == "1":
        analyzer.run_phase_1()
    elif args.phase == "2":
        analyzer.run_phase_2()
    elif args.phase == "3":
        analyzer.run_phase_3()
    elif args.phase == "4":
        analyzer.run_phase_4()
    elif args.phase == "5":
        analyzer.run_phase_5()


if __name__ == "__main__":
    main()
