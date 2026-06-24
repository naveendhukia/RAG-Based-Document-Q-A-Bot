import os
import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client()

def text_response(content):
    response = client.models.generate_content(
        model = "gemini-2.5-flash",
        contents = content
    )
    return response.text

def embedding_response(chunks):
    response = client.models.generate_content(
        model = "text-embedding-004",
        contents = chunks
    )
    return response.values

def add_to_chromadb(collection, embedding, pdf_path,chunk_id ):
    collection.add(
        embeddings = [embedding],
        source_data = [{"source":pdf_path,
                        "chunk_id":chunk_id}]
    )
    return collection


