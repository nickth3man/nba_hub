import duckdb
import os
import glob

db_path = 'data/nba.duckdb'
data_dir = 'data'

print(f"Connecting to {db_path}...")
con = duckdb.connect(db_path)

csv_files = glob.glob(os.path.join(data_dir, '*.csv'))

for csv_file in csv_files:
    filename = os.path.basename(csv_file)
    # Create table name: kaggle_ + filename without extension, lowercase
    table_name = f"kaggle_{filename.replace('.csv', '').lower()}"
    
    print(f"Loading {filename} into table '{table_name}'...")
    
    try:
        # Use CREATE OR REPLACE TABLE to overwrite if exists
        con.execute(f"""
            CREATE OR REPLACE TABLE {table_name} AS 
            SELECT * FROM read_csv_auto('{csv_file}', ignore_errors=True)
        """)
        
        count = con.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"✅ Loaded {count} rows into {table_name}")
        
    except Exception as e:
        print(f"❌ Error loading {filename}: {e}")

print("\nIngestion complete.")
print("\nVerifying tables:")
tables = con.execute("SHOW TABLES").fetchall()
for t in tables:
    if t[0].startswith('kaggle_'):
        print(f"  - {t[0]}")

con.close()
