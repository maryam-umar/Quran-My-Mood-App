from flask import Flask, jsonify, request
import sqlite3
import random

app = Flask(__name__)

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

