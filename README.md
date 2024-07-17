# Blog Generation and Question Answering Project
## Overview:
This project focuses on automating the generation of blog posts and enabling question-answering capabilities based on the generated content. The system utilizes advanced AI models and technologies to create, store, and interact with blog data efficiently.

## Screenshots

### <img src="preview\BG_homepage.png" width="1000"/>

### <img src="preview\BG_generateblog1.png" width="1000"/>

### <img src="preview\BG_generateblog2.png" width="1000"/>

### <img src="preview\BG_quarydata.png" width="1000"/>

## Technologies Used:
LlamaIndex: For indexing and searching blog content.
Gemini-Pro: An advanced model for text generation and question answering.
ChromaDB: A vector database used for storing and retrieving vector data.
Streamlit: A front-end framework to create an interactive user interface.

## Features:
Blog Generation: Automatically generate blog posts using the Gemini-Pro model.
Question Answering: Ask questions based on the generated blogs and receive accurate answers.
Vector Storage: Efficient storage and retrieval of blog content using ChromaDB.
Interactive UI: User-friendly interface for interacting with the system via Streamlit.

## Installation:
Prerequisites
Python 3.8 or higher
Virtual environment tools (e.g., venv or virtualenv)
Steps
Clone the Repository

```bash
git clone https://github.com/jagdish31502/blog_generation.git
cd blog-generation-qa
Create and Activate Virtual Environment
```

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Install Dependencies
```
```bash
pip install -r requirements.txt
Set Up Environment Variables
```

Create a .env file in the root directory and add necessary environment variables:
BACKGROUND_IMAGE = 'background-image'
EMBED_MODEL = 'all-mpnet-base-v2'
GEMINI_PRO_API_KEY=your_gemini_pro_api_key

## Usage:
1. Run the Streamlit App

    ```bash
    streamlit run app.py
    ```

2. Generate Blog Content

   - Navigate to the Streamlit app in your browser.
   - Use the provided interface to generate new blog posts using the Gemini-Pro model.
    
3. Ask Questions

   - Input questions in the question-answering section.
   - Receive answers based on the generated blog content.