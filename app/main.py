from fastapi import FastAPI
import os
import platform
import socket
from datetime import datetime

app = FastAPI()

@app.get("/")
def root():
    return {
        "message": "Bienvenue sur mon API !",
        "available_endpoints": ["/", "/info", "/healthz", "/metrics"]
    }

@app.get("/info")
def info():
    return {
        "environment": os.getenv("ENV", "dev"),
        "version": os.getenv("VERSION", "v0.0.1"),
        "commit": os.getenv("COMMIT", "unknown"),
        "build_time": os.getenv("BUILD_TIME", datetime.utcnow().isoformat()),
        "hostname": socket.gethostname(),
        "python_version": platform.python_version(),
        "system": platform.system(),
        "release": platform.release()
    }

@app.get("/healthz")
def health_check():
    # Simuler un check simple
    return {
        "status": "ok",
        "uptime": datetime.utcnow().isoformat(),
        "services": {
            "database": "ok",  # à adapter plus tard si tu veux checker une vraie BDD
            "cache": "ok"
        }
    }

@app.get("/metrics")
def metrics():
    return {
        "cpu_load": os.getloadavg(),  # (1min, 5min, 15min)
        "memory": {
            "total": os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") // (1024 ** 2),
            "available": os.sysconf("SC_AVPHYS_PAGES") * os.sysconf("SC_PAGE_SIZE") // (1024 ** 2)
        },
        "container_hostname": socket.gethostname()
    }
