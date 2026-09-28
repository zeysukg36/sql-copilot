import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

admin_url = os.getenv("ADMIN_DATABASE_URL")
if not admin_url:
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    name = os.getenv("POSTGRES_DB")
    port = os.getenv("POSTGRES_PORT", "5433")
    admin_url = f"postgresql+psycopg2://{user}:{password}@localhost:{port}/{name}"

engine = create_engine(admin_url)

df = pd.read_csv("../data/WA_Fn-UseC_-Telco-Customer-Churn.csv")
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)

df.to_sql("customers", engine, if_exists="replace", index=False)
print(f"✅ {len(df)} satır 'customers' tablosuna yüklendi.")