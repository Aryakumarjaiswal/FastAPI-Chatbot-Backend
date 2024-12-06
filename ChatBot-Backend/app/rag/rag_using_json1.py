import pandas as pd
import numpy as np
import google.generativeai as genai


def rag_using_json(message: str, top_n=5):
    # Load the pre-computed embeddings and the passage text
    df = pd.read_feather("data/maitri_data/maitri_data_with_embeddings.feather")

    query_embedding = genai.embed_content(
        model="models/text-embedding-004", content=message
    )["embedding"]

    # Compute the dot product between the query embedding and the pre-computed embeddings
    dot_products = np.dot(np.stack(df["Embeddings"]), query_embedding)

    top_indices = np.argsort(dot_products)[-top_n:][::-1]

    rag_passages = df.iloc[top_indices]["Text"].tolist()

    escaped_passages = [
        passage.replace("'", "").replace('"', "").replace("\n", " ")
        for passage in rag_passages
    ]

    joined_passages = "\n\n".join(
        f"PASSAGE {i+1}: {passage}" for i, passage in enumerate(escaped_passages)
    )

    prompt = f"""
            CONTEXT:{joined_passages}

            QUESTION: {message}
        """

    return prompt
