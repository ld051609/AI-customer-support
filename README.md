# RAG Chatbot with Next.js Frontend and Flask Backend

## Overview

This project is a Retrieval-Augmented Generation (RAG) chatbot that leverages external knowledge from the [Wikipedia 20220301.simple](https://huggingface.co/datasets/wikipedia) dataset. The project is built with a Next.js frontend and a Flask backend. The backend uses Pinecone for storing and retrieving vector embeddings, enabling the chatbot to provide accurate and contextually relevant responses.

## Features

- **Frontend**: 
  - Built with Next.js for efficient server-side rendering.
  - User-friendly interface for interacting with the chatbot.
  - API integration with the Flask backend for processing user inputs.

- **Backend**:
  - Flask-based backend handling API requests and responses.
  - Integration with Pinecone to store and retrieve vector embeddings.
  - Utilizes the `wikipedia` dataset (`20220301.simple`) for external knowledge retrieval.

## Getting Started

### Prerequisites

- Node.js (>= 16.x)
- Python (>= 3.8)
- pip (Python package installer)
- Pinecone API key
- OpenAI API key

### Setting up the backend
1. **Create and activate virtual environment**
2. **Install the required Python packages**
```bash 
    pip install -r requirements.txt
```
3. **Run the backend**
```bash 
    python3 app.py
```

### Setting up the frontend
1. **Install the required Node.js packages**
```bash 
    npm install 
    # or
    yarn install
```
2. **Run the Next.js development server**
```bash 
    npm run dev 
    # or
    yarn dev
```