from fastapi.responses import HTMLResponse

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
            </style>
        </head>
        <body>
            <h1>Bienvenue sur mon API 🎉</h1>
            <p>Voici les endpoints disponibles :</p>
            <ul>
                <li><a href="/info">/info</a> – Informations sur le build et le système</li>
                <li><a href="/healthz">/healthz</a> – Statut de santé</li>
                <li><a href="/metrics">/metrics</a> – Statistiques système</li>
            </ul>
            <p>Status : <strong>En ligne ✅</strong></p>
        </body>
    </html>
    """
