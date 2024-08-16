from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
import os
from datasets import load_dataset
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Set up Pinecone index
index_name = 'ai-customer-support'
if index_name in pc.list_indexes().names():
    pc.delete_index(index_name)
if index_name not in pc.list_indexes().names():
    # Create a new index if it does not exist
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="dotproduct",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )
# Connect to index
index = pc.Index(index_name)

# Set OpenAI API key
client = OpenAI(api_key=OPENAI_API_KEY)

# Generate embeddings
def generate_embeddings(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    response = client.embeddings.create(input=[text], model=model)
    embedding = response.data[0].embedding
    return embedding

# Store embeddings in Pinecone
def store_in_pinecone(id, title, url, text):
    embedding = generate_embeddings(text)
    index.upsert(
        vectors=[
            {
                "id": id,
                "values": embedding,
                "metadata": {
                    "title": title,
                    "url": url
                }
            }
        ]
    )

# Load the dataset
dataset = load_dataset('wikipedia', '20220301.simple')

# Store each article in Pinecone
for article in dataset['train']:
    store_in_pinecone(article['id'], article['title'], article['url'], article['text'])

print("Data stored in Pinecone successfully")

# Create chatbot response using OpenAI
def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    res = response.choices[0].message.content
    return res

# Retrieve response from Pinecone based on a query
def retrieve_from_pinecone(message):
    embedding = generate_embeddings(message)
    results = index.query(
        vector=embedding,
        top_k=3,
        include_metadata=True
    )
    print(results)
    return results['matches']


