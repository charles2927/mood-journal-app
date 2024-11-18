from flask import Flask, render_template, request
from textblob import TextBlob
import json

app = Flask(__name__)

def save_entry(entry, sentiment):
    try:
        with open('journal_entries.json', 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = []

    data.append({'entry': entry, 'sentiment': sentiment})

    with open('journal_entries.json', 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/', methods=['GET', 'POST'])
def home():
    entries = []
    try:
        with open('journal_entries.json', 'r') as file:
            entries = json.load(file)
    except FileNotFoundError:
        entries = []

    sentiment = ""
    if request.method == 'POST':
        user_entry = request.form['entry']
        blob = TextBlob(user_entry)
        sentiment_score = blob.sentiment.polarity

        if sentiment_score > 0:
            sentiment = "Positive 😊"
        elif sentiment_score < 0:
            sentiment = "Negative 😟"
        else:
            sentiment = "Neutral 😐"

        save_entry(user_entry, sentiment)

        return render_template('index.html', entries=entries, last_entry=user_entry, sentiment=sentiment)

    return render_template('index.html', entries=entries)

if __name__ == '__main__':
    app.run(debug=True)

from waitress import serve

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=5000)
