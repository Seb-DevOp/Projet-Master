from fastapi import FastAPI
import os
from datetime import datetime

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "env": os.getenv("ENV", "dev"),
        "version": os.getenv("VERSION", "v0.0.1"),
        "commit": os.getenv("COMMIT", "unknown"),
        "build_time": os.getenv("BUILD_TIME", datetime.utcnow().isoformat()),
        "status": "ok"
    }
