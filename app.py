import random
import os
import requests
from flask import Flask, render_template, abort, request
import tempfile
from MemeEngine.MemeGenerator import MemeGenerator
from QuoteEngine.TextIngestor import Ingestor

app = Flask(__name__)

meme = MemeGenerator('./static')


def setup():
    """Load all resources."""
    quote_files = [
        './_data/DogQuotes/DogQuotesTXT.txt',
        './_data/DogQuotes/DogQuotesDOCX.docx',
        './_data/DogQuotes/DogQuotesCSV.csv',
        './_data/DogQuotes/DogQuotesPDF.pdf',

    ]
    quotes = []
    images_path = "./_data/photos/dog/"

    for f in quote_files:
        parsed_quotes = Ingestor.parse(f)
        quotes.extend(parsed_quotes)

    imgs = []

    for f in os.listdir(images_path):
        if f.endswith(".jpg"):
            imgs.append(f"{images_path}/{f}")

    return quotes, imgs


quotes, imgs = setup()
print(imgs)


@app.route('/')
def meme_rand():
    """Generate a random meme."""
    img = random.choice(imgs)
    quote = random.choice(quotes)
    path = meme.make_meme(img, quote.quote, quote.author)
    return render_template('meme.html', path=path)


@app.route('/create', methods=['GET'])
def meme_form():
    """User input for meme information."""
    return render_template('meme_form.html')


@app.route('/create', methods=['POST'])
def meme_post():
    """Create a user defined meme."""

    image_url = request.form.get('image_url')
    quote = request.form.get('body')
    author = request.form.get('author')

    if not image_url or not quote or not author:
        return "Missing info.", 400

    response = requests.get(image_url)
    if response.status_code != 200:
        return "Error getting the image", 400

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    temp_file.write(response.content)
    print(temp_file.name)

    path = meme.make_meme(temp_file.name, quote, author)
    temp_file.close()
    os.remove(temp_file.name)

    return render_template('meme.html', path=path)


if __name__ == "__main__":
    app.run()
