from flask import Flask, render_template, request
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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        mood = request.form.get('mood', '').capitalize()
        if not mood:
            return render_template('index.html', error="Please select a mood.")
        
        verse = get_random_verse_by_mood(mood)
        if verse:
            return render_template('result.html', mood=mood, arabic=verse[0], translation=verse[1])
        else:
            return render_template('index.index.html', error=f"No verses found for mood: {mood}")
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)  
