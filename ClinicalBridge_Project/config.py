import os
from dotenv import load_dotenv

# Load environment variables from a .env file if it exists
load_dotenv()

# --- API Keys ---
# Google Gemini API key is required for LLM and Embeddings
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "your-google-api-key-here")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "your-openrouter-key")

# --- Model Selection ---
# We use models optimized for reasoning and structured JSON output
LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "google/gemini-2.5-flash")
EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "models/gemini-embedding-001")

# --- Agent Temperature Parameters ---
# Strictly controlled temperatures to prevent hallucinations and maintain clinical objectivity
TRIAGE_AGENT_TEMP = 0.0
EHR_AGENT_TEMP = 0.0
ANAMNESIS_AGENT_TEMP = 0.1  # Slight flexibility to interpret colloquial patient terms
SYNTHESIS_AGENT_TEMP = 0.0

# --- Vector Store Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VECTOR_STORE_PATH = os.path.join(BASE_DIR, "data", "vector_store")
