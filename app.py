from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import requests
import sqlite3
import random

app = Flask(__name__)

CORS(app)

# Your database file
Database = 'verses.db'

def get_random_verse_by_mood(mood, db_name=Database):
    """Fetch a random verse for a given mood from the database."""
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT arabic, translation FROM verses WHERE mood = ?", (mood,))
            rows = cursor.fetchall()
            if not rows:
                return None
            return random.choice(rows)
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results')
def results():
    mood = request.args.get('mood', '').capitalize()
    if not mood:
        return render_template('result.html', error="No mood specified")
    
    # Fetch verse from PythonAnywhere API
    api_url = f"https://amaluomar.pythonanywhere.com/api/verse?mood={mood}"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if 'error' in data:
            return render_template('result.html', error=data['error'])
        else:
            return render_template('result.html', mood=mood, arabic=data['arabic'], translation=data['translation'])
    else:
        return render_template('result.html', error="Failed to fetch data from the API.")

@app.route('/api/verse', methods=['GET'])
def get_verse():
    """API endpoint to get a random verse based on mood."""
    mood = request.args.get('mood', '').capitalize()
    if not mood:
        return jsonify({"error": "Please provide a mood parameter."}), 400
    verse = get_random_verse_by_mood(mood)
    if verse:
        return jsonify({
            "mood": mood,
            "arabic": verse[0],
            "translation": verse[1]
        })
    else:
        return jsonify({"error": f"No verses found for mood: {mood}"}), 404

if __name__ == '__main__':
    app.run(debug=False)
