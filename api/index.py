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
        # Get data safely
        data = request.get_json(force=True) 
        
        # Log it to the Vercel console so we can see it
        print(f"Received data: {data}")

        # Insert into Supabase
        # We use .get() to avoid crashing if a field is missing
        response = supabase.table("reservations").insert({
            "name": data.get('name', 'Unknown'),
            "date": data.get('date', ''),
            "time": data.get('time', ''),
            "guests": int(data.get('guests') or 1)
        }).execute()
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        print(f"ERROR: {str(e)}") # This will show up in your red logs!
        return jsonify({"status": "error", "message": str(e)}), 500