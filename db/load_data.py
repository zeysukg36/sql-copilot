# db/load_data.py
import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_NAME = os.getenv("POSTGRES_DB")
DB_PORT = os.getenv("POSTGRES_PORT", "5433")

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@localhost:{DB_PORT}/{DB_NAME}")

df = pd.read_csv("../data/WA_Fn-UseC_-Telco-Customer-Churn.csv")

# Churn projesinden bildiğimiz TotalCharges düzeltmesi
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)

df.to_sql("customers", engine, if_exists="replace", index=False)
print(f"✅ {len(df)} satır 'customers' tablosuna yüklendi.")