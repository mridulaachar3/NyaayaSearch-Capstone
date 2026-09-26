# NyaayaSearch

NyaayaSearch is an AI-powered Indian legal search and assistance platform. It combines hybrid statutory retrieval (BM25 keyword search + fine-tuned dense embeddings with sentence-transformers) and cross-encoder reranking over Indian legal acts (including the Bharatiya Nyaya Sanhita, Bharatiya Nagarik Suraksha Sanhita, Indian Contract Act, Motor Vehicles Act, Information Technology Act, etc.), paired with a Groq-powered LLM reasoning layer providing plain-language explanations in English, Hindi, and Kannada.

---

## 1. Setup

### Prerequisites
- Python 3.10+ (tested on Python 3.11/3.14)
- Node.js 18+ and npm
- Groq API Key

### Python Virtual Environment & Dependencies
Create and activate a virtual environment, then install the pinned dependencies:

```bash
# Create virtual environment
python -m venv .venv

# Activate environment
# On Windows (PowerShell):
.venv\Scripts\Activate.ps1
# On Linux / macOS:
source .venv/bin/activate

# Install pinned dependencies
pip install -r requirements.txt
```

### Environment Configuration
Create a `.env` file at the repository root and add your Groq API key:

```env
GROQ_API_KEY=gsk_your_groq_api_key_here
```

---

## 2. Running the Application

### Backend (FastAPI + Uvicorn)
From the repository root with the virtual environment activated:

```bash
uvicorn main:app --app-dir scripts --reload --port 8000
```

*(Alternatively, navigate to `scripts/` and run `uvicorn main:app --reload --port 8000`)*

- API Server: `http://127.0.0.1:8000`
- Interactive Swagger Documentation: `http://127.0.0.1:8000/docs`
- Health check & Corpus Statistics: `http://127.0.0.1:8000/stats`

### Frontend (React + Vite)
In a separate terminal:

```bash
cd frontend
npm install
npm run dev
```

- Web UI: `http://localhost:5173`

---

## 3. Reproducing Evaluations

### Multilingual Reranker Evaluation
Evaluates the retrieval pipeline (Current Production Hybrid BM25+Embeddings vs. Cross-Encoder Reranker) across English, Hindi, and Kannada benchmarks with McNemar tests, bootstrap confidence intervals, and Holm-Bonferroni corrections:

```bash
python scripts/eval_reranker.py --strict-clean --languages en,hi,kn
```

### Relevance Classifier with Reranker Features
Evaluates the 5-fold `GroupKFold` relevance classifier with leakage-free decision threshold tuning (combining BM25, semantic cosine similarity, and cross-encoder scores):

```bash
python scripts/classifier_with_reranker.py
```

### Google Colab GPU Scripts
For fine-tuning and cross-validation on GPU hardware (e.g. Google Colab with T4/V100/A100):
- `scripts/finetune_crossencoder_cv.py`: 5-fold cross-validation fine-tuning of cross-encoders on GPU.
- `scripts/stack_finetuned_rf.py`: Stacked fine-tuned cross-encoder + Random Forest training across 5 folds.

Both scripts include Colab setup steps and run standalone when the required data files (`classifier_training_data_with_reranker.csv`, `Legal_Knowledge_Base_combined.xlsx`, `training_pairs.jsonl`) are present.

---

## 4. Note on Pinned Versions

The retrieval scores, embedding generation, cross-encoder inference, and evaluation benchmarks strictly depend on the versions pinned in `requirements.txt` (specifically `torch==2.14.0`, `transformers==5.17.0`, `sentence-transformers==6.1.0`, `scikit-learn==1.9.1`, `numpy==2.5.3`, and `scipy==1.18.1`). Upgrading or changing these packages may produce minor floating-point differences in embedding similarity scores or ranking order.
