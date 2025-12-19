# Mini RAG-Powered Assistant

This project implements a Retrieval-Augmented Generation (RAG) based assistant
that answers user queries using a custom document corpus. The system integrates
document retrieval with large language models to provide grounded and context-aware responses.


## Problem Statement

Traditional LLMs generate responses without awareness of private or custom documents.
The goal of this project is to design a RAG-based system that retrieves relevant
information from a document corpus and uses it to generate accurate answers.


## High-Level Architecture

User → Frontend (Node.js)
     → Backend API (FastAPI)
     → RAG Pipeline
     → Vector Database (Chroma)
     → LLM (OpenAI)
     → Response to User


### RAG-Based Design Choice

A Retrieval-Augmented Generation approach was selected to reduce hallucinations
and ensure responses are grounded in the provided document corpus.

### Document Ingestion

Documents are uploaded via the frontend and processed once.
Text is extracted, cleaned, and prepared for chunking.


### Chunking Strategy

Recursive Character Chunking with overlap was used to preserve semantic meaning
while maintaining manageable chunk sizes for embedding generation.


### Embedding Strategy

Dense vector embeddings are generated using an OpenAI embedding model.
These embeddings capture semantic meaning rather than exact keyword matches.


### Vector Database

A persistent vector store (Chroma) is used to store embeddings and metadata.
Persistence avoids recomputation and improves performance for repeated queries.

### Retrieval Strategy

Cosine similarity is used to compare query embeddings with document embeddings.
Max Marginal Relevance (MMR) is applied to ensure diversity in retrieved chunks.


### Prompt Engineering

The final prompt includes:
- Retrieved document context
- Previous conversation history
- Current user query

This enables multi-turn, context-aware responses.


### Conversation Memory

Conversation history is maintained on the frontend and explicitly sent to the backend
with each query, allowing the LLM to handle follow-up questions coherently.


## Query Handling Flow

1. User submits a question via frontend
2. Backend embeds the query
3. Relevant document chunks are retrieved
4. Context + history are passed to LLM
5. Final answer is generated and returned


## Cloud Deployment Strategy

- Frontend deployed using Azure Static Web Apps
- Backend deployed using Azure App Service
- Environment variables used for API key management
- HTTPS and CORS enabled for secure communication

## Technology Stack

- Frontend: React (Node.js)
- Backend: FastAPI (Python)
- Vector Database: Chroma
- Embeddings & LLM: OpenAI
- Cloud Platform: Microsoft Azure


## Design Decisions and Trade-offs

- Chroma was chosen for simplicity and local persistence.
- REST APIs were preferred over direct LLM calls for security.
- POST requests were used due to large payload sizes and non-idempotent operations.
