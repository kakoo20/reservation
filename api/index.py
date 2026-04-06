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
        # Use silent=True so it doesn't crash if the body is weird
        data = request.get_json(silent=True)
        
        if not data:
            return jsonify({"status": "error", "message": "No JSON data received"}), 400

        # Log exactly what we received to the Vercel console
        print(f"DEBUG: Data received: {data}")

        response = supabase.table("reservations").insert({
            "name": data.get('name'),
            "date": data.get('date'),
            "time": data.get('time'),
            "guests": int(data.get('guests') or 1)
        }).execute()
        
        return jsonify({"status": "success", "message": "Booked!"}), 200

    except Exception as e:
        # This writes the REAL error to your Vercel logs
        print(f"CRITICAL ERROR: {str(e)}") 
        return jsonify({"status": "error", "message": f"Server Error: {str(e)}"}), 500