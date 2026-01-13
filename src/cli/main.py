import subprocess
import sys

import click

from src.core.config import DB_PATH
from src.core.database import get_db_connection


@click.group()
def cli():
    """NBA Data Hub CLI - Manage your basketball data lakehouse."""
    pass


@cli.command()
def init():
    """Initialize the database schema and load core dimensions."""
    click.echo("Initializing database...")
    subprocess.run([sys.executable, "src/etl/load/init_dimensions.py"], check=True)
    subprocess.run(
        [sys.executable, "src/etl/load/init_referees_coaches.py"], check=True
    )
    subprocess.run([sys.executable, "src/etl/load/init_awards_table.py"], check=True)
    click.echo("Database initialized.")


@cli.command()
@click.option("--date", help="Date in YYYYMMDD format to scrape.")
def scrape(date):
    """Scrape game metadata for a specific date."""
    if not date:
        click.echo("Please provide a date with --date YYYYMMDD")
        return
    click.echo(f"Scraping data for {date}...")
    subprocess.run(
        [
            sys.executable,
            "src/scraping/sites/basketball_reference_games.py",
            "--date",
            date,
        ],
        check=True,
    )


@cli.command()
def migrate():
    """Run database migrations to unified schema."""
    click.echo("Running migrations...")
    subprocess.run(
        [sys.executable, "src/etl/transform/migrate_unified_schema.py"], check=True
    )
    subprocess.run(
        [sys.executable, "src/etl/transform/migrate_depth_data.py"], check=True
    )
    click.echo("Migrations complete.")


@cli.command()
def status():
    """Show database status and row counts."""
    con = get_db_connection()
    tables = con.execute("SHOW TABLES").fetchall()
    click.echo(f"Database: {DB_PATH}")
    click.echo(f"Tables found: {len(tables)}")
    for (table,) in tables:
        try:
            count = con.execute(f'SELECT count(*) FROM "{table}"').fetchone()[0]
            click.echo(f"  - {table}: {count} rows")
        except Exception as e:
            click.echo(f"  - {table}: Error ({e})")
    con.close()


if __name__ == "__main__":
    cli()
