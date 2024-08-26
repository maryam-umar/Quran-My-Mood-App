import sqlite3
import random
import requests
from bs4 import BeautifulSoup

def get_verse_and_translation(url):
    """Fetches the verse in Arabic and its English translation from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the Arabic verse text
        verse_elements = soup.find_all('span', class_='GlyphWord_styledWord__OfEEG')

        if not verse_elements:
            raise ValueError("Could not find the Arabic verse text")

        arabic_text = ''.join([element.get_text(strip=True) for element in verse_elements])

        if not arabic_text:
            raise ValueError("Found the Arabic verse container, but it appears to be empty")

        # Find the translation text
        translation_container = soup.find('div', class_='TranslationText_text__4atf8 TranslationText_ltr__146rZ')

        if translation_container is None:
            raise ValueError("Could not find the translation container")

        translation_text = translation_container.get_text(strip=True)

        if not translation_text:
            raise ValueError("Found the translation container, but it appears to be empty")

        return arabic_text, translation_text

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred during the request: {err}")
    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")

    return None, None

def save_to_sql(arabic_text, translation_text, mood, db_name='verses.db'):
    """Saves the Arabic verse, its translation, and mood to an SQLite database."""
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS verses (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    arabic TEXT,
                    translation TEXT,
                    mood TEXT
                )
            ''')
            cursor.execute('INSERT INTO verses (arabic, translation, mood) VALUES (?, ?, ?)',
                           (arabic_text, translation_text, mood))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def main():
    verses_data = {
        "Anxiety": [
            "https://quran.com/2/286",
            "https://quran.com/3/139",
            "https://quran.com/13/28",
            "https://quran.com/3/189",
            "https://quran.com/2/62",
            "https://quran.com/2/186",
            "https://quran.com/2/214",
            "https://quran.com/65/3",
            "https://quran.com/3/122",
            "https://quran.com/15/56",
            "https://quran.com/7/54",
            "https://quran.com/7/188",
            "https://quran.com/6/2",
            "https://quran.com/6/160",
            "https://quran.com/5/39",
            "https://quran.com/5/40",
            "https://quran.com/5/56",
            "https://quran.com/5/120",
            "https://quran.com/17/66",
            "https://quran.com/19/21",
            "https://quran.com/29/60",
            "https://quran.com/11/6",
            "https://quran.com/11/56",
            "https://quran.com/68/32",
            "https://quran.com/76/22",
            "https://quran.com/76/24",
            "https://quran.com/5/35",
            "https://quran.com/5/40",
            "https://quran.com/15/23",
            "https://quran.com/15/49",
            
        ],
        "Fear": [
            "https://quran.com/2/82",
            "https://quran.com/2/107",
            "https://quran.com/2/112",
            "https://quran.com/2/115",
            "https://quran.com/2/117",
            "https://quran.com/2/277",
            "https://quran.com/20/46",
            "https://quran.com/72/22",
            "https://quran.com/20/68",
            "https://quran.com/44/51",
            "https://quran.com/6/17",
            "https://quran.com/6/102",
            "https://quran.com/5/69",
            "https://quran.com/4/132",
            "https://quran.com/25/59",
            "https://quran.com/17/65",
            "https://quran.com/30/54",
            "https://quran.com/31/22",
            "https://quran.com/55/33",
            "https://quran.com/53/38",
            "https://quran.com/29/19",
            "https://quran.com/35/2",
            "https://quran.com/35/17",
            "https://quran.com/35/41",
            "https://quran.com/39/52",
            "https://quran.com/39/53",
            "https://quran.com/39/61",
            "https://quran.com/47/7",
            "https://quran.com/28/68",
            "https://quran.com/13/15",
        ],
        "Sadness": [
            "https://quran.com/39/10",
            "https://quran.com/12/86",
            "https://quran.com/40/60",
            "https://quran.com/93/3",
            "https://quran.com/13/28",
            "https://quran.com/94/6",
            "https://quran.com/3/146",
            "https://quran.com/3/139",
            "https://quran.com/64/11",
            "https://quran.com/70/5",
            "https://quran.com/4/28",
            "https://quran.com/4/147",
            "https://quran.com/25/58",
            "https://quran.com/30/33",
            "https://quran.com/55/34",
            "https://quran.com/55/60",
            "https://quran.com/53/43",
            "https://quran.com/3/139",
            "https://quran.com/3/142",
            "https://quran.com/3/150",
            "https://quran.com/3/160",
            "https://quran.com/29/2",
            "https://quran.com/35/18",
            "https://quran.com/47/2",
            "https://quran.com/47/35",
            "https://quran.com/28/24",
            "https://quran.com/13/24",
            "https://quran.com/11/47",
            "https://quran.com/11/75",
            "https://quran.com/11/115",
            "https://quran.com/66/8",
        ],
        "Anger": [
            "https://quran.com/3/134",
            "https://quran.com/42/43",
            "https://quran.com/11/115",
            "https://quran.com/76/24",
            "https://quran.com/74/11",
            "https://quran.com/10/11",
            "https://quran.com/41/34",
            "https://quran.com/21/87",
            "https://quran.com/7/55",
            "https://quran.com/6/34",
            "https://quran.com/6/147",
            "https://quran.com/5/105",
            "https://quran.com/4/45",
            "https://quran.com/4/148",
            "https://quran.com/17/37",
            "https://quran.com/17/96",
            "https://quran.com/19/47",
            "https://quran.com/2/263",
            "https://quran.com/29/52",
            "https://quran.com/35/6",
            "https://quran.com/37/174,"
            "https://quran.com/38/17",
            "https://quran.com/38/55",
            "https://quran.com/39/30",
            "https://quran.com/39/70",
            "https://quran.com/40/14",
            "https://quran.com/40/60",
            "https://quran.com/50/39",
            "https://quran.com/28/55",
        ],
        "Joy": [
            "https://quran.com/14/7",
            "https://quran.com/110/3",
            "https://quran.com/99/7",
            "https://quran.com/98/7",
            "https://quran.com/73/2",
            "https://quran.com/71/28",
            "https://quran.com/2/152",
            "https://quran.com/7/205",
            "https://quran.com/9/38",
            "https://quran.com/2/155",
            "https://quran.com/7/3",
            "https://quran.com/7/10",
            "https://quran.com/7/27",
            "https://quran.com/7/200",
            "https://quran.com/7/204",
            "https://quran.com/7/205",
            "https://quran.com/6/72",
            "https://quran.com/6/127",
            "https://quran.com/5/9",
            "https://quran.com/5/35",
            "https://quran.com/29/7",
            "https://quran.com/29/45",
            "https://quran.com/36/58",
            "https://quran.com/39/73",
            "https://quran.com/11/108",
            "https://quran.com/15/48",
            "https://quran.com/15/56",
            "https://quran.com/89/28",
            "https://quran.com/93/5",
            "https://quran.com/93/8",
        ],
        "Reassurance": [
            "https://quran.com/95/4",
            "https://quran.com/71/13",
            "https://quran.com/19/67",
            "https://quran.com/18/37",
            "https://quran.com/50/6",
            "https://quran.com/3/14",
            "https://quran.com/3/195",
            "https://quran.com/57/20",
            "https://quran.com/21/103",
            "https://quran.com/2/28",
            "https://quran.com/7/42",
            "https://quran.com/7/153",
            "https://quran.com/6/13",
            "https://quran.com/6/116",
            "https://quran.com/6/125",
            "https://quran.com/4/40",
            "https://quran.com/4/69",
            "https://quran.com/14/23",
            "https://quran.com/17/20",
            "https://quran.com/17/70",
            "https://quran.com/29/62",
            "https://quran.com/29/64",
            "https://quran.com/40/19",
            "https://quran.com/40/39",
            "https://quran.com/40/51",
            "https://quran.com/40/55",
            "https://quran.com/50/29",
            "https://quran.com/28/60",
            "https://quran.com/28/84",
            "https://quran.com/76/11",
        ],
    }       
    for mood, urls in verses_data.items():
        for url in urls:
            try:
                arabic_text, translation_text = get_verse_and_translation(url)                
                if arabic_text and translation_text: 
                    save_to_sql(arabic_text, translation_text, mood)
                    print(f"Verse from {url} with mood '{mood}' has been successfully saved to the database.")
                else:
                    print(f"Skipping {url} as no valid text was found.")

            except Exception as e:
                print(f"An error occurred while processing {url}: {e}")

if __name__ == "__main__":
    main()