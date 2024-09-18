import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import TextLoader

# Get the API key from the environment variable
openai_api_key =  ""


if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Initialize embedding function
embeddings = OpenAIEmbeddings(api_key=openai_api_key)

# Initialize Chroma DB
vector_db = Chroma(
    embedding_function=embeddings,
    collection_name="my_collection",
    persist_directory="./my_chroma_db"
)

def add_document_to_chroma(file_path):
    # Load the document
    loader = TextLoader(file_path)
    documents = loader.load()

    # Split the document into chunks
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)

    # Add documents to Chroma DB
    vector_db.add_documents(texts)
    # The changes are automatically persisted
    print(f"Added {len(texts)} text chunks from {file_path} to Chroma DB")

def main():
    while True:
        file_path = input("Enter the path to the text file you want to add (or 'q' to quit): ")
        if file_path.lower() == 'q':
            break
        if os.path.exists(file_path):
            add_document_to_chroma(file_path)
        else:
            print("File not found. Please enter a valid file path.")

if __name__ == "__main__":
    main()