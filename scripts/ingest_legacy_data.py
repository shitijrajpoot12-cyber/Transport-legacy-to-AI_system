from pathlib import Path
import pandas as pd
import urllib
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

# __file__ is 'scripts/ingest_legacy_data.py'
script_dir = Path(__file__).resolve().parent # points to project_root/scripts
project_root = script_dir.parent             # climbs up to project root

# Load the environmental configuration
load_dotenv(project_root / ".env")

data_path = project_root / "data" / "raw" / "dynamic_supply_chain_logistics_dataset.csv"

# Fallback values default cleanly to your running Docker container configurations
db_host = os.getenv("SQL_SERVER_HOST", "127.0.0.1")
db_port = os.getenv("SQL_SERVER_PORT", "1433")
db_user = os.getenv("SQL_ADMIN_USER", "sa")
db_password = os.getenv("SQL_ADMIN_PASSWORD", "FdeEnterprisePass123")

# 1. Load the raw dataset
print(f"Loading CSV from {data_path}...")
if not data_path.exists():
    raise FileNotFoundError(f"Could not locate the source dataset at: {data_path}")
    
df = pd.read_csv(data_path)

# 2. Map clean columns to a messy 2000s legacy enterprise schema
legacy_mapping = {
    'timestamp': 'TS_UTC',
    'vehicle_gps_latitude': 'V_LAT',
    'vehicle_gps_longitude': 'V_LON',
    'iot_temperature': 'IOT_TEMP_VAL_C',
    'cargo_condition_status': 'CGO_COND_CD',
    'risk_classification': 'RISK_CLS_TXT',
    'delay_probability': 'DELAY_PROB_DEC',
    'port_congestion_level': 'PRT_CNG_LVL',
    'route_risk_level': 'RT_RSK_IDX'
}

# Keep only the columns we mapped for this demo and rename them
df_legacy = df[list(legacy_mapping.keys())].rename(columns=legacy_mapping)

# Add a fake ingestion flag to make it look like an automated legacy system
df_legacy['SYS_INGEST_FLAG'] = 'Y'

# 3. Connect to Docker MSSQL Server
print("Connecting to legacy MSSQL Database...")
connection_string = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={db_host},{db_port};"
    f"DATABASE=master;"
    f"UID={db_user};"
    f"PWD={db_password};"
    f"Encrypt=no;"                  # ODBC Driver 18 defaults to yes; explicitly tracking it keeps connections predictable  # Explicitly bypass local self-signed certificate constraints inside Docker
)

params = urllib.parse.quote_plus(connection_string)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")

# 4. Ingest data into the messy table name
table_name = 'TBL_SC_FLEET_HIST_RAW'
print(f"Ingesting into {table_name}. This may take a minute...")

try:
    df_legacy.to_sql(table_name, engine, if_exists='replace', index=False, schema='dbo')
    print("✅ Legacy data ingestion complete!")
except Exception as e:
    print(f"❌ Ingestion failed with error:\n{e}")
