from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import os
import platform
import socket
from datetime import datetime

app = FastAPI(
    title="API Système & Build",
    description="Une API légère exposant des infos de build, de monitoring et de santé.",
    version=os.getenv("VERSION", "v1.0.0")
)

@app.get("/", response_class=HTMLResponse)
def root():
    return """
    <html>
        <head>
            <title>Mon API</title>
            <style>
                body { font-family: sans-serif; padding: 2rem; background: #f4f4f4; }
                h1 { color: #333; }
                ul { line-height: 1.6; }
                a { color: #007BFF; text-decoration: none; }
                a:hover { text-decoration: underline; }
                footer { margin-top: 2rem; font-size: 0.9rem; color: #666; }
            </style>
        </head>
        <body>
            <h1>Bienvenue sur mon API 🎉</h1>
            <p>Voici les endpoints disponibles :</p>
            <ul>
                <li><a href="/info">/info</a> – Informations sur le build et le système</li>
                <li><a href="/healthz">/healthz</a> – Statut de santé</li>
                <li><a href="/metrics">/metrics</a> – Statistiques système</li>
                <li><a href="/docs">/docs</a> – Documentation interactive Swagger</li>
            </ul>
            <p>Status : <strong>En ligne ✅</strong></p>
            <footer>
                &copy; 2025 – Mon API FastAPI
            </footer>
        </body>
    </html>
    """

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
    return {
        "status": "ok",
        "uptime": datetime.utcnow().isoformat(),
        "services": {
            "database": "ok",
            "cache": "ok"
        }
    }

@app.get("/metrics")
def metrics():
    try:
        total_mem = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") // (1024 ** 2)
        avail_mem = os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_AVPHYS_PAGES") // (1024 ** 2)
        cpu_load = os.getloadavg()
    except (AttributeError, ValueError, OSError):
        total_mem = avail_mem = 0
        cpu_load = [0.0, 0.0, 0.0]

    return {
        "cpu_load": {
            "1m": cpu_load[0],
            "5m": cpu_load[1],
            "15m": cpu_load[2]
        },
        "memory": {
            "total_MB": total_mem,
            "available_MB": avail_mem
        },
        "hostname": socket.gethostname()
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
