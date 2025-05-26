import os
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
# Update these imports
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
import chromadb

def extract_text_from_pdf(pdf_path):
    """Extract text from a PDF file"""
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    """Split text into overlapping chunks"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
    )
    chunks = text_splitter.split_text(text)
    return chunks

def create_embeddings_and_store(chunks, db_directory="./chroma_db"):
    """Create embeddings and store in Chroma DB"""
    # Initialize the embedding model (using a smaller model for local use)
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",  # Smaller, faster model good for local use
        model_kwargs={'device': 'cpu'}
    )
    
    # Create and persist the vector database
    vectordb = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        persist_directory=db_directory
    )
    
    print(f"Vector database created with {len(chunks)} chunks")
    return vectordb

def main():
    # Set path to your PDF
    pdf_path = "math_pro_guide.pdf"  # Replace with your PDF file path
    
    # Process the PDF
    print(f"Extracting text from {pdf_path}...")
    text = extract_text_from_pdf(pdf_path)
    print(f"Extracted {len(text)} characters")
    
    # Chunk the text
    print("Chunking text...")
    chunks = chunk_text(text)
    print(f"Created {len(chunks)} chunks")
    
    # Create embeddings and store in Chroma
    print("Generating embeddings and storing in Chroma...")
    vectordb = create_embeddings_and_store(chunks)
    print("Processing complete!")

if __name__ == "__main__":
    main()