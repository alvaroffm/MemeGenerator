import os
import random
import tempfile
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw
from PIL.ImageFont import FreeTypeFont


class MemeGenerator:
    """
    A class to generate memes by adding quotes and author text to an image.

    Attributes:
        output_dir (str or bool): Directory path where the meme will be saved.
                                   Defaults to False, meaning it saves in the current working directory.
        font_path (str): Path to the font file used for text.
        font_quote (FreeTypeFont): Font used for the quote.
        font_author (FreeTypeFont): Font used for the author name.
        image (Image): The image object that will have text added to it.
        quote (str): The quote text to be added.
        author (str): The author of the quote to be added.

    Methods:
        load_and_resize_image(img_path: str, width: int):
            Loads the image from the given path and resizes it to the specified width.
        
        prepare_fonts(quote: str, author: str):
            Prepares the fonts based on the provided quote and author text.
        
        make_meme(img_path: str, text: str, author: str, width=500) -> str:
            Generates a meme by adding the quote and author text to the image and saves it.
    """

    def __init__(self, output_dir='./output'):
        """
        Initializes the MemeGenerator instance.

        Args:
            output_dir (str, optional): Directory path for saving the generated meme. Defaults to False.
        """
        self.output_dir = output_dir
        self.image = None
        self.quote = ''
        self.author = ''
        self.font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'FiraSans-Medium.ttf')
        self.font_quote = None
        self.font_author = None

    def load_and_resize_image(self, img_path: str, width: int = 500):
        """
        Load image from the path and resize it to the specified width, maintaining aspect ratio.

        Args:
            img_path (str): Path to the image file.
            width (int): The width to which the image should be resized (default 500).
        """
        try:
            self.image = Image.open(img_path)

            if width > 500 or width < 1:
                width = 500

            original_width, original_height = self.image.size
            aspect_ratio = original_height / original_width
            new_height = int(width * aspect_ratio)

            self.image = self.image.resize((width, new_height), Image.Resampling.LANCZOS)

        except FileNotFoundError:
            print(f"Error: The image file at {img_path} was not found.")
            raise
        except OSError as e:
            print(f"Error: Failed to open or process the image. {e}")
            raise

    def prepare_fonts(self, quote: str, author: str):
        """
        Prepares the fonts based on the quote and author text.

        Args:
            quote (str): The quote text.
            author (str): The author of the quote.
        """

        self.quote = quote
        self.author = author
        self.font_size = 30
        try:
            self.font_quote = FreeTypeFont(self.font_path, self.font_size)
            self.font_author = FreeTypeFont(self.font_path, int(self.font_size * 0.8))
        except Exception as e:
            print(f"Error: Could not load the font at {self.font_path}. {e}")
            raise

    def make_meme(self, img_path: str, text: str, author: str, width=500) -> str:
        """
        Generate a meme by adding the quote and author text to the image.

        Args:
            img_path (str): Path to the image file.
            text (str): The quote text to be added to the image.
            author (str): The author of the quote.
            width (int, optional): The width of the resized image. Defaults to 500.

        Returns:
            str: The file path of the generated meme.
        """
        try:
            self.load_and_resize_image(img_path, width)
            self.prepare_fonts(text, author)

            drawing = ImageDraw.Draw(self.image)

            # I use this block to avoid clipping when adding the text to the image
            img_width, img_height = self.image.size
            text_width, _ = drawing.textbbox((0, 0), text, font=self.font_quote)[2:]
            author_width, _ = drawing.textbbox((0, 0), f"- {author}", font=self.font_author)[2:]

            margin = 10
            max_text_width = max(text_width, author_width)

            max_x = max(margin, img_width - max_text_width)
            max_y = max(margin + self.font_size, img_height - 2 * self.font_size)

            if max_x > margin:
                x = random.randint(margin, max_x)
            else:
                x = margin

            if max_y > margin + self.font_size:
                y = random.randint(margin + self.font_size, max_y)
            else:
                y = margin + self.font_size
            drawing.text((x, y), text, font=self.font_quote, anchor='lb', fill=(250, 240, 255))
            # I use a random color for the Author's name.
            drawing.text((x, y + 5), f"- {author}", font=self.font_author, anchor='lt',
                         fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

            output_folder = Path(self.output_dir)

            output_folder.mkdir(parents=True, exist_ok=True)
            output_path_complete = tempfile.NamedTemporaryFile(dir=output_folder.name, prefix='meme_',
                                                               suffix='.jpg').name
            self.image.save(output_path_complete)

            return str(output_folder) + "/" + str(Path(output_path_complete).name)

        except Exception as e:
            print(f"Error: {e}")
            raise


if __name__ == '__main__':

    meme_generator = MemeGenerator()
    print(meme_generator.make_meme(r'_data/photos/dog/xander_4.jpg', text='Example Quote', author='Author Text'))
    print('Completed')
