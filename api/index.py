from flask import Flask, request, jsonify
from supabase import create_client
from flask_cors import CORS  # Important for Vercel
import os

app = Flask(__name__)
CORS(app) # This tells the browser "It's okay to send data here"

# Your Supabase Credentials
url = "https://qfglcgvcutotlsaexljq.supabase.co"
key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InFmZ2xjZ3ZjdXRvdGxzYWV4bGpxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzU0ODk3ODMsImV4cCI6MjA5MTA2NTc4M30.WR0rlO5iPwKzBGC4xR2iMv_1ix0VBDpv7r90yNrwp7o"
supabase = create_client(url, key)

@app.route('/api/reserve', methods=['POST'])
def reserve():
    try:
        data = request.json
        # Insert into Supabase table
        response = supabase.table("reservations").insert({
            "name": data['name'],
            "date": data['date'],
            "time": data['time'],
            # Change this line in your api/index.py
            "guests": int(data.get('guests', 1))
        }).execute()
        
        return jsonify({"status": "success", "message": "Reservation confirmed!"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# DO NOT write 'app = Flask(__name__)' again here.
# Vercel just needs to find the 'app' object.
app = app
