import pandas as pd
import numpy as np
import google.generativeai as genai
import os


def rag_using_json(message: str, top_n=5):
    # Load the pre-computed embeddings
    df = pd.read_feather(
        "data/property_dummy_data/property_data_with_embeddings.feather"
    )

    # Configure Gemini API
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)

    # Embed the query
    query_embedding = genai.embed_content(
        model="models/text-embedding-004", content=message
    )["embedding"]

    # Compute similarity
    df["similarity"] = df["embeddings"].apply(lambda x: np.dot(x, query_embedding))

    # Get top passages
    top_passages = df.nlargest(top_n, "similarity")["full_text"].tolist()

    # Prepare prompt
    joined_passages = "\n\n".join(
        f"PASSAGE {i+1}: {passage}" for i, passage in enumerate(top_passages)
    )

    prompt = f"""
    CONTEXT:{joined_passages}

    QUESTION: {message}

    Please provide a detailed answer based on the context above. If the context does not contain sufficient information to answer the question, please say so.
    """

    return prompt
