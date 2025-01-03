# LLM Learnings

## RAG Architecture

Goal
- Load some PDF file and talk with that

Steps
- Load the pdf from a path
- split this words
- create embeddings
- save in vectorstore database
- retrieval

Install
- cp .env.example .env
- docker build -t langchain-app .
- docker compose up -d
