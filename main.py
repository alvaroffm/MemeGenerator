import os
import random
from QuoteEngine.TextIngestor import Ingestor, QuoteModel
from MemeEngine.MemeGenerator import MemeGenerator

def generate_meme(path=None, body=None, author=None):
    """ Generate a meme given a path and a quote """
    img = None
    quote = None

    if path is None:
        images = "./_data/photos/dog/"
        imgs = []
        for root, _, files in os.walk(images):
            imgs = [os.path.join(root, name) for name in files]

        if not imgs:
            raise FileNotFoundError("No images found in the directory.")

        img = random.choice(imgs)

    else:
        img = random.choice(path)

    if body is None:
        quote_files = ['./_data/DogQuotes/DogQuotesTXT.txt',
                       './_data/DogQuotes/DogQuotesDOCX.docx',
                       './_data/DogQuotes/DogQuotesCSV.csv']
        quotes = []
        for f in quote_files:
            quotes.extend(Ingestor.parse(f))

        if not quotes:
            raise Exception("No quotes found in the specified sources.")

        quote = random.choice(quotes)
    else:
        if author is None:
            raise Exception("Author name is required if a quote is provided.")
        
        quote = QuoteModel(body, author)

    meme = MemeGenerator('./tmp')
    path = meme.make_meme(img, quote.quote, quote.author)
    return path

def implement_arguments():
    import argparse

    parser = argparse.ArgumentParser(description='Generate a meme from an image and a quote.')
    parser.add_argument('--path', type=str, help='Path to the image file', default=None)
    parser.add_argument('--body', type=str, help='Quote text', default=None)
    parser.add_argument('--author', type=str, help='Author name', default=None)

    return parser

if __name__ == "__main__":
    
    parser = implement_arguments()
    args = parser.parse_args()
    print(generate_meme(args.path, args.body, args.author))

