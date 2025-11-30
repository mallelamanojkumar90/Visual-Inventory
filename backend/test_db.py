import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("DATABASE_URL")
# Mask password for printing
safe_url = url.replace(url.split(":")[2].split("@")[0], "****") if url and ":" in url and "@" in url else url
print(f"Testing connection to: {safe_url}")

try:
    engine = create_engine(url)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print(f"Connection successful! Result: {result.fetchone()}")
except Exception as e:
    print(f"Connection failed: {e}")
    import traceback
    traceback.print_exc()
