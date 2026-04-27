from flask import Flask, render_template_string
import requests
import time

app = Flask(__name__)

# L'API qu'on va surveiller (Prix du Bitcoin)
API_URL = "https://api.coindesk.com/v1/bpi/currentprice.json"

@app.route('/')
def monitor_api():
    start_time = time.time()
    status = "🔴 DOWN"
    latency = 0
    api_data = {}

    try:
        # On teste l'API
        response = requests.get(API_URL, timeout=5)
        latency = round((time.time() - start_time) * 1000, 2) # Temps en millisecondes
        
        if response.status_code == 200:
            status = "🟢 UP (Fonctionnelle)"
            api_data = response.json()
        else:
            status = f"🟠 Erreur {response.status_code}"
    except Exception as e:
        status = f"🔴 Erreur : {str(e)}"

    # Page HTML simple pour afficher les résultats
    html = f"""
    <html>
        <head><title>Monitoring API</title></head>
        <body style="font-family: Arial; text-align: center; padding-top: 50px;">
            <h1>🛠️ Tableau de bord de Surveillance</h1>
            <hr>
            <h2>API Surveillée : Coindesk Bitcoin</h2>
            <p style="font-size: 20px;">Statut : <b>{status}</b></p>
            <p style="font-size: 20px;">Temps de réponse : <b>{latency} ms</b></p>
            <hr>
            <p>Dernière vérification en direct</p>
        </body>
    </html>
    """
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)
