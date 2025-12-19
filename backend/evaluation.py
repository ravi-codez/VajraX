import json
import time
from sentence_transformers import SentenceTransformer, util

from rag.qa import answer_question
from rag.vectorstore import get_vectorstore


# -----------------------------
# Configuration
# -----------------------------
GROUND_TRUTH_FILE = "evaluation/ground_truth.json"
SIMILARITY_THRESHOLD = 0.75
FAITHFULNESS_THRESHOLD = 0.6
TOP_K = 3


# -----------------------------
# Load models
# -----------------------------
embedder = SentenceTransformer("all-MiniLM-L6-v2")


# -----------------------------
# Metric Functions
# -----------------------------
def context_recall(retrieved_docs, ground_truth):
    for doc in retrieved_docs:
        if ground_truth.lower() in doc.page_content.lower():
            return 1
    return 0


def semantic_similarity(predicted, ground_truth):
    emb1 = embedder.encode(predicted, convert_to_tensor=True)
    emb2 = embedder.encode(ground_truth, convert_to_tensor=True)
    return util.cos_sim(emb1, emb2).item()


def faithfulness_score(answer, context):
    emb1 = embedder.encode(answer, convert_to_tensor=True)
    emb2 = embedder.encode(context, convert_to_tensor=True)
    return util.cos_sim(emb1, emb2).item()


# -----------------------------
# Evaluation Loop
# -----------------------------
def evaluate():
    with open(GROUND_TRUTH_FILE, "r") as f:
        dataset = json.load(f)

    vectorstore = get_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": TOP_K})

    recall_scores = []
    similarity_scores = []
    faithfulness_scores = []
    latencies = []

    for sample in dataset:
        question = sample["question"]
        ground_truth = sample["ground_truth"]

        # Retrieve context
        retrieved_docs = retriever.get_relevant_documents(question)
        context_text = "\n".join(doc.page_content for doc in retrieved_docs)

        recall_scores.append(
            context_recall(retrieved_docs, ground_truth)
        )

        # Generate answer
        start = time.time()
        answer = answer_question(question, history=[])
        latencies.append(time.time() - start)

        # Compute metrics
        similarity_scores.append(
            semantic_similarity(answer, ground_truth)
        )

        faithfulness_scores.append(
            faithfulness_score(answer, context_text)
        )

    # Aggregate metrics
    context_recall_avg = sum(recall_scores) / len(recall_scores)
    answer_similarity_avg = sum(similarity_scores) / len(similarity_scores)
    faithfulness_avg = sum(faithfulness_scores) / len(faithfulness_scores)

    hallucinations = sum(
        1 for s in faithfulness_scores if s < FAITHFULNESS_THRESHOLD
    )
    hallucination_rate = hallucinations / len(faithfulness_scores)

    avg_latency = sum(latencies) / len(latencies)

    # Print results
    print("\n📊 RAG Evaluation Results\n")
    print(f"Context Recall        : {context_recall_avg:.2f}")
    print(f"Answer Similarity     : {answer_similarity_avg:.2f}")
    print(f"Faithfulness Score    : {faithfulness_avg:.2f}")
    print(f"Hallucination Rate    : {hallucination_rate:.2%}")
    print(f"Average Latency (sec) : {avg_latency:.2f}")


if __name__ == "__main__":
    evaluate()
