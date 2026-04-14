from flask import Flask, request, jsonify
from flask_cors import CORS
import whois
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app) # This allows your Chrome extension to talk to this server

@app.route('/check_link', methods=['GET', 'POST'])
def check():
    # Use .get('domain') or .get('url') depending on your extension's code
    domain = request.args.get('domain') or request.args.get('url')
    
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date
        
        # Corrected indentation and logic
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        
        # --- TEST MODE: FORCING DANGER ALERT ---
        is_malicious = (datetime.now() - creation_date) < timedelta(hours=24)

        # ---------------------------------------

        return jsonify({"is_malicious": is_malicious})

    except Exception as e:
        # If WHOIS lookup fails, we still return a response
        return jsonify({"is_malicious": True, "error": str(e)})

if __name__ == '__main__':
    # Running on port 5000 as required by your extension
   import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
