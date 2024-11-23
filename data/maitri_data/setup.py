# Run this file each time the data is updated.

import pandas as pd
import google.generativeai as genai
import os

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

genai.configure(api_key=api_key)

# Load JSON data
data = pd.read_json("data/maitri_data.json")

df = pd.DataFrame(data)
df.columns = ["Title", "Text"]


# Get the embeddings of each text and add to an embeddings column in the dataframe
def embed_fn(title, text):
    return genai.embed_content(model="models/text-embedding-004", content=text)[
        "embedding"
    ]


df["Embeddings"] = df.apply(lambda row: embed_fn(row["Title"], row["Text"]), axis=1)

# Save the dataframe to a feather file
df.to_feather("data/data_with_embeddings.feather")

print("Data Embedded and Saved to data/data_with_embeddings.feather")
