import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Current Groq production model
MODEL_NAME = "openai/gpt-oss-120b"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

CHROMA_PATH = "data/processed/chroma_db"

COLLECTION_NAME = "medical_knowledge"

TOP_K = 5