import os, logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import boto3
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(title="D1FY Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/healthz")
def healthz():
    out = {"database": "skipped", "storage": None}
    try:
        bucket = os.getenv("BUCKET_NAME")
        if not bucket:
            out["storage"] = "skipped"
        else:
            s3 = boto3.client(
                "s3",
                aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
                aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
                region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
            )
            s3.head_bucket(Bucket=bucket)
            out["storage"] = "ok"
    except Exception as e:
        logging.exception("S3 fail")
        out["storage"] = f"error: {e}"

    ok = out["storage"] in ("ok", "skipped")
    return {"status": "ok" if ok else "error", "details": out}
