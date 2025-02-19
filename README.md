# Meme Generator Application

This project provides you with a fully functional application to create custom memes by combining images with quotes. You can either generate a meme using random selections or specify your own inputs (image, quote, and author) to create a personalized meme. The project is designed with two main interfaces in mind: a command-line interface (CLI) for quick meme generation and a web-based interface built using Flask for an interactive experience.

---

## Project Structure

The project is organized into a serie of directories and files, each serving a specific purpose. Below is an outline of the project’s structure along with a brief description of each component:

```
.
├── main.py          # Entry point for the command-line interface, allowing meme creation via terminal commands.
├── app.py           # Flask web application that provides a graphical interface for meme generation.
├── MemeEngine       # Contains the logic responsible for generating memes.
│   └── MemeGenerator.py  
├── QuoteEngine      # Manages the extraction and parsing of quotes from various text files.
│   └── TextIngestor.py   
├── templates        # HTML templates used by the Flask web application.
│   ├── meme.html         
│   ├── mbase.html        
│   └── meme_form.html    
└── static           # Directory for storing the generated memes as static files.
```

Each component of the project works together seamlessly, enabling both command-line and web interactions for generating memes.

---

## Prerequisites

Before running the application, ensure that your development environment meets the following requirements:

- **Python 3.7 or higher:** The project relies on modern Python features available from version 3.7 onward.
- **Required Python Packages:** The application depends on several third-party libraries. If a `requirements.txt` file is available, you can install all necessary packages with:
  ```bash
  pip install -r requirements.txt
  ```
These dependencies ensure that the application runs smoothly and that image processing, web serving, and network requests are properly handled.

---

## Command-Line Interface (CLI)

The command-line interface, powered by the `main.py` script, allows users to generate memes directly from the terminal. This approach is ideal for quick meme creation without launching a web server.

### How to Run the CLI

To generate a meme using the CLI, execute the following command in your terminal:
```bash
python main.py --path <image_path> --body <quote_text> --author <author_name>
```

### Command-Line Arguments

- **`--path` (optional):**  
  Specifies the file path of the image to be used for meme generation. If you do not provide a path, the application will automatically select a random image from the available collection.

- **`--body` (optional):**  
  The text of the quote that you want to overlay on the image. If this argument is omitted, the application will randomly choose a quote from its database.

- **`--author` (optional):**  
  The name of the person credited with the quote. **Note:** If you provide a quote via `--body`, you must also supply the `--author` argument so that the meme displays complete information.

### Example Usage

Here’s an example command that demonstrates how to generate a meme with a specific image and custom quote:
```bash
python main.py --body "Life is better with dogs" --author "Anonymous"
```

This command tells the application to create a meme using the specified image and quote details.

---

## Flask Web Application

For those who prefer a graphical user interface, the Flask web application offers an intuitive way to generate memes through your web browser.

### Starting the Web Application

1. **Launch the Flask Server:**  
   Run the following command to start the web server:
   ```bash
   python app.py
   ```
   This will initialize the Flask server and set up the necessary endpoints for the web interface.

2. **Access the Web Interface:**  
   Open your preferred web browser and navigate to:
   ```bash
   http://127.0.0.1:5000
   ```
   This URL will bring up the homepage where you can start generating memes.

### Available Web Routes

#### Homepage

- **Purpose:**  
  The homepage automatically generates a meme using a random image and quote. This is a great way to quickly see what the application can do without having to provide any input.
  
- **Functionality:**  
  You can generate additional random memes by clicking the **`Random`** button, which triggers the backend to select new random components.

####  Meme Creation Form (Creator)

- **Purpose:**  
  This route provides a form for users who wish to create custom memes by specifying their own inputs.

- **Form Fields:**  
  - **Image URL:** Provide the direct URL of an image (.jpg) to be used.
  - **Quote Text:** Enter the text of the quote that will appear on the meme.
  - **Author Name:** Enter the name of the person credited with the quote.

- **Submission:**  
  After filling in the form, click the **`Create Meme!`** button. The application will process your inputs, generate the meme accordingly, and then display the result.

### Detailed Workflow Example

1. **Navigate to the Homepage:**  
   Open your web browser and visit `http://127.0.0.1:5000`.

2. **Generate a Random Meme:**  
   On the homepage, click the **`Random`** button to view a randomly generated meme.

3. **Access the Meme Creator:**  
   Click on the **`Creator`** link (or button) to go to the custom meme creation form.

4. **Fill Out the Form:**  
   Enter the URL of your chosen image, along with the quote text and the author’s name.

5. **Submit and View Your Meme:**  
   Click the **`Create Meme!`** button to generate your meme. The new meme will be displayed, and it is also saved in the `static` directory.

