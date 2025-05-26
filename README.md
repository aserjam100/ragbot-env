Prerequisites

Python 3.8+
Node.js 16+
Ollama installed and running

Setup Instructions
1. Clone the Repository
bashgit clone <your-repo-url>
cd <repo-name>
2. Set Up Python Environment
bash# Create virtual environment
python -m venv ragbot-env

# Activate virtual environment
# On macOS/Linux:
source ragbot-env/bin/activate
# On Windows:
ragbot-env\Scripts\activate

# Install Python dependencies
pip install pypdf langchain chromadb sentence-transformers fastapi uvicorn requests langchain-community
3. Set Up Ollama
bash# Pull the Gemma 3 12B model
ollama pull gemma3:12b

# Ensure Ollama is running (usually starts automatically)
# You can check by visiting: http://localhost:11434
4. Process Your PDF Document
The repository includes a sample PDF (math_pro_guide.pdf). To process it or use your own PDF:
bash# Make sure you're in the project root and virtual environment is activated
python process_pdf.py
This will:

Extract text from the PDF
Create text chunks
Generate embeddings
Store everything in the chroma_db folder

5. Set Up React Frontend
bash# Navigate to frontend directory
cd rag-frontend

# Install dependencies
npm install

# Return to project root
cd ..
Running the Application
You need to run three components simultaneously:
Terminal 1: Start the Backend API
bash# Make sure virtual environment is activated
source ragbot-env/bin/activate  # or ragbot-env\Scripts\activate on Windows

# Start the FastAPI backend
uvicorn app:app --reload
The backend will be available at: http://localhost:8000
Terminal 2: Start the React Frontend
bash# Navigate to frontend directory
cd rag-frontend

# Start the development server
npm run dev
The frontend will be available at: http://localhost:5173
Terminal 3: Ensure Ollama is Running
bash# Check if Ollama is running
curl http://localhost:11434/api/tags

# If not running, start it:
ollama serve
Using the Application

Open your browser and go to http://localhost:5173
You'll see a simple chat interface
Ask questions about the content in your PDF document
The chatbot will retrieve relevant information from the PDF and generate answers using the Gemma 3 12B model
