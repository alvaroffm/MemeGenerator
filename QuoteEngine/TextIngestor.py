import abc
import csv
import os
import pprint
import re
import subprocess
import tempfile
import docx
import pandas as pd


class IngestorInterface(abc.ABC):
    """
    Abstract base class for defining file ingestor behavior. Different file formats 
    (CSV, DOCX, TXT, PDF) will inherit from this class and implement the `parse` method.
    """
    allowed_extensions = []

    @classmethod
    def can_ingest(cls, path: str) -> bool:
        """
        Determines if the file type can be ingested based on the file extension.
  
        Args:
            path (str): The path to the file to check.

        Returns:
            bool: True if the file extension is allowed for ingestion, otherwise False.
        """
        print(cls.input_extension(path))
        return cls.input_extension(path) in cls.allowed_extensions

    @classmethod
    @abc.abstractmethod
    def parse(cls, path: str):
        """
        Abstract method to parse the content of the file.

        Args:
            path (str): The path to the file to parse.

        Returns:
            list: A list of `QuoteModel` objects extracted from the file.
        """
        pass

    @classmethod
    def input_extension(cls, path: str) -> str:
        """
        Extracts the file extension from a given file path.

        Args:
            path (str): The file path.

        Returns:
            str: The file extension.
        """
        return path.split('.')[-1]

    @classmethod
    def clean_data(cls, text: str) -> str:
        """
        Cleans the text by removing unwanted characters, such as special symbols, 
        non-printable characters, and common punctuation marks.

        Args:
            text (str): The text to be cleaned.

        Returns:
            str: The cleaned version of the input text.
        """
        unwanted_chars = r'[()\"#<>{}`+=~|.!?/@;,¿«»¨>>ï]'

        cleaned_text = re.sub(unwanted_chars, "", text)
        cleaned_text = ''.join(
            char for char in cleaned_text if char.isprintable()
        )

        return cleaned_text.strip()


class IngestorDOCX(IngestorInterface):
    """
    Ingestor for processing DOCX files, extracting quotes and authors.
    """
    allowed_extensions = ['docx']

    @classmethod
    def parse(cls, path: str):

        if not cls.can_ingest(path):
            raise ValueError(f"File not supported - {path}")

        doc = docx.Document(path)
        quotes = []

        for paragraph in doc.paragraphs:
            if paragraph.text:
                parts = paragraph.text.split("-")
                if len(parts) == 2:
                    quote_text = cls.clean_data(parts[0])
                    author_text = cls.clean_data(parts[1])
                    quotes.append(QuoteModel(quote=quote_text, author=author_text))

        return quotes


class IngestorCSV(IngestorInterface):
    """
    Ingestor for processing CSV files, extracting quotes and authors.
    """
    allowed_extensions = ['csv']

    @classmethod
    def parse(cls, path: str):
        if not cls.can_ingest(path):
            raise ValueError(f"File not supported - {path}")

        df = pd.read_csv(path).apply(
            lambda x: QuoteModel(quote=x.body, author=x.author), axis=1
        ).to_list()
        return df


#
# class IngestorPDF(IngestorInterface):
#     """
#     Ingestor for processing PDF files, extracting quotes and authors.
#     """
#     allowed_extensions = ['pdf']
#
#     @classmethod
#     def parse(cls, path: str):
#
#         output = []
#         if not cls.can_ingest(path):
#             raise Exception(f"File not supported - {path}")
#
#         temp_file = tempfile.NamedTemporaryFile(suffix="_pdf.txt")
#         temp_file_name = temp_file.name
#
#         try:
#             subprocess.run(['pdftotext', path, temp_file_name], check=True)
#             output = IngestorTXT.parse(temp_file_name)
#         except Exception as e:
#             print("'pdftotext' subprocess didn't work")
#             raise
#
#         return output
class IngestorPDF(IngestorInterface):
    """
       Handles PDF files to extract quotes and authors using Xpdf.
       """
    allowed_extensions = ['pdf']

    @classmethod
    def parse(cls, source: str):

        if not cls.can_ingest(source):
            raise ValueError(f"File not processed: {source}")

        extracted_quotes = []

        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.abspath(os.path.join(current_dir, '..'))
            pdftotext_path = os.path.join(project_root, r"xpdf-tools-win-4.05", "bin64", "pdftotext.exe")

            result = subprocess.run([pdftotext_path, "-layout", source, "-"], capture_output=True, text=True, check=True)
            text = result.stdout

            for line in text.split("\n"):
                elements = line.strip().split("-")
                try:
                    quote = cls.clean_data(elements[0])
                    author = cls.clean_data(elements[1])
                    quote_pdf = QuoteModel(quote=quote, author=author)
                    extracted_quotes.append(quote_pdf)

                except Exception as e:
                    continue

            return extracted_quotes

        except Exception as error:
            raise ValueError(f"Error occurred while processing PDF: {error}")


class IngestorTXT(IngestorInterface):
    """
    Ingestor for processing plain text (TXT) files, extracting quotes and authors.
    """
    allowed_extensions = ['txt']

    @classmethod
    def parse(cls, path: str):

        if not cls.can_ingest(path):
            raise ValueError(f"File not supported - {path}")

        lines = open(path, 'r').readlines()

        quote_models = []

        for line in lines:
            if cls.clean_data(line):
                parts = line.split("-")
                if len(parts) > 1:
                    quote = cls.clean_data(parts[0])
                    author = cls.clean_data(parts[1])
                    quote_models.append(QuoteModel(quote=quote, author=author))

        return quote_models


class Ingestor(IngestorInterface):
    """
    A class to select the appropriate ingestor based on the file extension.
    """

    @classmethod
    def parse(cls, path: str):

        extension = cls.input_extension(path)

        if extension == 'csv':
            ingestor = IngestorCSV
        elif extension == 'docx':
            ingestor = IngestorDOCX
        elif extension == 'txt':
            ingestor = IngestorTXT
        elif extension == 'pdf':
            ingestor = IngestorPDF
        else:
            raise Exception('No suitable ingestor found')

        print(f'Selected {ingestor}')
        return ingestor.parse(path)


class QuoteModel:
    """
    A model representing a quote and its author.
    """

    def __init__(self, quote: str, author: str):
        """
        Initializes a new `QuoteModel` object with the quote and author.

        Args:
            quote (str): The text of the quote.
            author (str): The author of the quote.
        """
        self.quote = quote
        self.author = author

    def __repr__(self):
        """
        String representation of the `QuoteModel` object.

        Returns:
            str: A formatted string showing the quote and author.
        """
        return f'Quote Object: "{self.quote}" - {self.author}'


if __name__ == '__main__':
    import os

    file_path = 'DogQuotesPDF.pdf'
    print(f"File exists: {os.path.exists(file_path)}")
    print(f"Full path: {file_path}")

    files = [
        'DogQuotesCSV.csv',
        'DogQuotesDOCX.docx',
        'DogQuotesTXT.txt',
        'DogQuotesPDF.pdf'
    ]
    current_dir = os.path.dirname(os.path.abspath(__file__))

    project_root = os.path.abspath(os.path.join(current_dir, '..'))

    data_directory = os.path.join(project_root, '_data', 'DogQuotes')

    ingestor = Ingestor()

    for file in files:
        file_path = os.path.join(data_directory, file)
        pprint.pprint(ingestor.parse(file_path))
