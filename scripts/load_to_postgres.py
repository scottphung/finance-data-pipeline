import pandas as pd
from sqlalchemy import create_engine

# ------------------------
# DATABASE CONNECTION
# ------------------------
engine = create_engine(
    "postgresql+psycopg2://postgres:1234@localhost:5432/finance_db"
)

# ------------------------
# LOAD DATA
# ------------------------
df = pd.read_csv("data/stock_features.csv")

# ------------------------
# INSERT INTO POSTGRES
# ------------------------
df.to_sql(
    "stock_prices",
    engine,
    if_exists="replace",
    index=False
)

print("✅ Data loaded into PostgreSQL")