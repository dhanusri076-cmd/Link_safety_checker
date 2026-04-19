from flask import Flask, request, jsonify
from flask_cors import CORS
import whois
from datetime import datetime, timedelta
import os

app = Flask(__name__)
CORS(app) # This allows your Chrome extension to talk to this server

# --- ADD THIS NEW SECTION TO FIX THE "NOT FOUND" ERROR ---
@app.route('/')
def home():
    return jsonify({
        "status": "online",
        "message": "Link Safety Checker API is running. Use /check_link for analysis."
    })
# ---------------------------------------------------------

@app.route('/check_link', methods=['GET', 'POST'])
def check():
    domain = request.args.get('domain') or request.args.get('url')
    
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        # TEST MODE: FORCING DANGER ALERT if domain is less than 24 hours old
        is_malicious = (datetime.now() - creation_date) < timedelta(hours=24)
        
        return jsonify({"is_malicious": is_malicious})

    except Exception as e:
        return jsonify({"is_malicious": True, "error": str(e)})

if __name__ == '__main__':
    # --- IMPORTANT: UNCOMMENT THESE LINES FOR RENDER ---
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
