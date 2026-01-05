from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from storage import get_all

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
def dashboard():
    hotels = get_all()

    html = """
    <html>
    <head>
        <title>Hotel Price Tracker</title>
        <style>
            body { font-family: Arial; padding: 30px; }
            h1 { margin-bottom: 10px; }
            .hotel { margin-bottom: 15px; }
            .price { font-weight: bold; }
            .chat { color: #666; font-size: 12px; }
        </style>
    </head>
    <body>
        <h1>🏨 Tracked Hotels</h1>
    """

    if not hotels:
        html += "<p>No hotels tracked yet.</p>"
    else:
        for h in hotels:
            html += f"""
            <div class="hotel">
                <div class="price">${h['last_price']}</div>
                <a href="{h['url']}" target="_blank">{h['url']}</a>
                <div class="chat">Chat ID: {h['chat_id']}</div>
            </div>
            <hr/>
            """

    html += "</body></html>"
    return html
