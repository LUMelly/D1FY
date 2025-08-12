from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import boto3
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create FastAPI app
app = FastAPI(title="D1FY Backend")

# CORS setup (allow all for now — can tighten later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "D1FY API is up"}

@app.get("/health")
def health():
    """
    Health check endpoint for API and S3 bucket.
    """
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
        logging.exception("S3 check failed")
        out["storage"] = "error"
    return out

@app.get("/healthz")
def healthz():
    """
    Lightweight probe: returns OK plus details.
    """
    return {"status": "ok", "details": health()}
