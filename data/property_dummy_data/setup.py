import pandas as pd
import json
import google.generativeai as genai
import os
import numpy as np

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

genai.configure(api_key=api_key)

# Load JSON data
with open("data/property_dummy_data/property_data.json", "r") as file:
    data = json.load(file)


# Extract property information
def extract_property_info(property_data):
    return {
        "property_id": property_data.get("property_id", ""),
        "name": property_data.get("name", ""),
        "description": property_data.get("description", ""),
        "location": f"{property_data.get('location', {}).get('address', '')}, {property_data.get('location', {}).get('city', '')}, {property_data.get('location', {}).get('state', '')}",
        "bedrooms": property_data.get("details", {}).get("bedrooms", 0),
        "bathrooms": property_data.get("details", {}).get("bathrooms", 0),
        "max_guests": property_data.get("details", {}).get("max_guests", 0),
        "amenities": ", ".join(property_data.get("amenities", [])),
        "base_rate": property_data.get("pricing", {}).get("base_rate", 0),
        "check_in": property_data.get("policies", {}).get("check_in", ""),
        "check_out": property_data.get("policies", {}).get("check_out", ""),
        "full_text": f"""
Property: {property_data.get('name', '')}
Description: {property_data.get('description', '')}
Location: {property_data.get('location', {}).get('address', '')} in {property_data.get('location', {}).get('city', '')}, {property_data.get('location', {}).get('state', '')}
Bedrooms: {property_data.get('details', {}).get('bedrooms', 0)}
Bathrooms: {property_data.get('details', {}).get('bathrooms', 0)}
Max Guests: {property_data.get('details', {}).get('max_guests', 0)}
Amenities: {", ".join(property_data.get("amenities", []))}
Base Rate: ${property_data.get('pricing', {}).get('base_rate', 0)}
Check-in: {property_data.get('policies', {}).get('check_in', '')}
Check-out: {property_data.get('policies', {}).get('check_out', '')}
        """,
    }


# Create DataFrame
df = pd.DataFrame([extract_property_info(prop) for prop in data.get("properties", [])])


# Embedding function
def embed_fn(text):
    return genai.embed_content(model="models/text-embedding-004", content=text)[
        "embedding"
    ]


# Add embeddings column
df["embeddings"] = df["full_text"].apply(embed_fn)

# Save to feather file
df.to_feather("data/property_dummy_data/property_data_with_embeddings.feather")

print(
    "Data Embedded and Saved to data/property_dummy_data/property_data_with_embeddings.feather"
)
