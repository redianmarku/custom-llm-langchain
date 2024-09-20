# Custom LLM Chatbot with LangChain

This project is a conversational chatbot built using OpenAI's language models, LangChain, ChromaDB for vector storage, and Flask for serving the chatbot as an API. It allows the user to embed documents into a vector database and retrieve relevant information during the chatbot conversation.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Embedding Data to ChromaDB](#embedding-data-to-chromadb)
- [Running the Flask Server](#running-the-flask-server)
- [Testing the API](#testing-the-api)
- [Environment Variables](#environment-variables)
- [Technologies Used](#technologies-used)

## Features

- **Custom conversational AI**: Uses OpenAI's GPT-4 models with LangChain's conversational memory and retrieval capabilities.
- **ChromaDB**: Stores and retrieves vector embeddings for document-based context.
- **Flask API**: Provides a backend server that responds to user input via a `/chat` endpoint.

## Prerequisites

Before running the project, ensure that you have:

1. **Python 3.7+**
2. **API Key** for OpenAI models. You can get it from [OpenAI's Developer Platform](https://platform.openai.com/).

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/redianmarku/custom-llm-langchain.git
   cd custom-llm-langchain
   ```

2. **Install dependencies**:

   It's recommended to create a virtual environment before installing the requirements.

   ```bash
   python3 -m venv env
   source env/bin/activate  # For Linux/macOS
   env\Scripts\activate  # For Windows
   ```

   Then, install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your OpenAI API key**:

   You need to set an environment variable for your API key. You can do this by adding the following to your shell profile or using a `.env` file:

   **Linux/macOS**:

   ```bash
   export OPENAI_API_KEY="your_openai_api_key_here"
   ```

   **Windows**:

   ```bash
   set OPENAI_API_KEY="your_openai_api_key_here"
   ```

## Embedding Data to ChromaDB

To use the chatbot with document retrieval, you need to embed documents into the vector database (ChromaDB):

1. **Run the `chroma-embedding.py` script**:

   ```bash
   python chroma-embedding.py
   ```

2. **Add a document**:

   When prompted, enter the path to the text file you want to add to the Chroma database. The script will split the document into chunks and store the embeddings in the vector database.

3. **Exit the script**:

   You can type `'q'` to quit the script once you're done embedding documents.

## Running the Flask Server

To start the Flask server, follow these steps:

1. **Run the `app.py` file**:

   ```bash
   python app.py
   ```

2. The Flask server will run on `http://127.0.0.1:5000/` in development mode.

## Testing the API

You can test the API using Postman or any HTTP client of your choice. Here's how:

1. **Endpoint**:

   ```
   POST http://127.0.0.1:5000/chat
   ```

2. **Request Body**:

   Send a `POST` request with a JSON body containing a `message` field. Example:

   ```json
   {
     "message": "What is the weather today?"
   }
   ```

3. **Response**:

   The API will respond with a JSON object containing the chatbot's response:

   ```json
   {
     "response": "I am an AI chatbot. I can't check the weather right now."
   }
   ```

## Environment Variables

Make sure to set the following environment variable for the API to work properly:

- `OPENAI_API_KEY`: Your OpenAI API key for accessing the GPT models.

## Technologies Used

- **Python**: Programming language for the backend.
- **Flask**: Lightweight WSGI web application framework for serving the API.
- **LangChain**: Framework for building applications with large language models.
- **ChromaDB**: Vector database for storing and retrieving embeddings.
- **OpenAI API**: For generating language model outputs.
