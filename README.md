# AI Requirements RAG - QA Test Scenario Analyzer

A Python-based project that uses Retrieval-Augmented Generation (RAG) to help QA engineers analyze software requirements and generate structured test scenarios with AI.

## Features

- Semantic search for relevant software requirements.
- AI-generated positive, negative, and edge-case test scenarios.
- Requirement-to-test traceability.
- Gherkin scenarios using Given, When, and Then.
- Identification of ambiguous requirements and missing information.
- Source references for retrieved requirements.
- Human review of AI-generated test cases.

## Technology Stack

- Python
- OpenAI API
- ChromaDB
- Embeddings and semantic search
- Retrieval-Augmented Generation (RAG)
- Pytest

## Project Structure

```text
data/
  documents/
    authentication_requirements.md
  vector_store/
src/
  answer_generator.py
  chunker.py
  config.py
  document_loader.py
  embeddings.py
  qa_analyzer.py
  rag_pipeline.py
  retriever.py
  test_rag_unknown.py
  vector_store.py
.env.example
requirements.txt
README.md
```

## Prerequisites

- Python 3.12 or a compatible version.
- An OpenAI API key with access to the configured model.
- Git.

## Installation

Clone the repository:

```bash
git clone https://github.com/bailona/ai-requirements-rag.git
cd ai-requirements-rag
```

Create a virtual environment in Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```powershell
python -m pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root, using `.env.example` as a reference.

Add your API key:

```dotenv
OPENAI_API_KEY=your_openai_api_key_here
```

**Security:** Never commit your real API key or publish it in your repository.

## Run the QA Analyzer

From the project root, execute:

```powershell
python -m src.qa_analyzer
```

The current example analyzes password reset requirements and generates a structured QA report.

## Expected Analysis

The report may include:

- Requirement traceability IDs.
- Test case descriptions and pre