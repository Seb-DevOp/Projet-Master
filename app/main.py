from fastapi import FastAPI
import os
from datetime import datetime
import uvicorn

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

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # prends PORT de l'env ou 8080 par défaut
    uvicorn.run(app, host="0.0.0.0", port=port)
