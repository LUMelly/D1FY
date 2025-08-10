import os, psycopg2, boto3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="D1FY Backend")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/healthz")
def healthz():
    details = {"database":"skipped","storage":"skipped"}
    # DB check (we'll set DATABASE_URL later)
    try:
        db_url = os.getenv("DATABASE_URL")
        if db_url:
            conn = psycopg2.connect(db_url, connect_timeout=5, sslmode="require")
            with conn.cursor() as cur: cur.execute("SELECT 1;"); cur.fetchone()
            conn.close(); details["database"]="ok"
    except Exception as e: details["database"]=f"error: {e}"
    # S3 check (we'll set BUCKET envs later)
    try:
        bucket = os.getenv("BUCKET_NAME")
        if bucket:
            s3 = boto3.client("s3",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_DEFAULT_REGION","us-east-1"))
            s3.head_bucket(Bucket=bucket); details["storage"]="ok"
    except Exception as e: details["storage"]=f"error: {e}"
    ok = (details["database"] in ("ok","skipped")) and (details["storage"] in ("ok","skipped"))
    return {"status":"ok" if ok else "error","details":details}
