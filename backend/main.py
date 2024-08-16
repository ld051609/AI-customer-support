import os
from pinecone import Pinecone, ServerlessSpec
import openai

OPENAI_API_KEY = "sk-6gwmkoC0OWp2eD7euiu0cQJfGOh5vTIkW-JPk2JhEtT3BlbkFJcX0q7rT0jjOpCTm-9tNqR3BAAf6Phjw6cqrqjiiKQA"
PINECONE_API_KEY ="c099b577-4a22-4b51-81e4-618d2e924a79"

# Initialize Pinecone
pc = Pinecone(
    api_key=PINECONE_API_KEY
)

# Set up Pinecone index
index_name = 'chatbot-ai-index'
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
print(index.describe_index_stats())

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Generate embeddings
def generate_embeddings(text):
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response['data'][0]['embedding']

# Create chatbot response using OpenAI
def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Store embeddings and response in Pinecone
def store_in_pinecone(message, response):
    embedding = generate_embeddings(message)
    index.upsert(vectors=[(message, embedding, {"response": response})])
    return embedding

# Retrieve response from Pinecone based on a query
def retrieve_from_pinecone(message, top_k=1):
    embedding = generate_embeddings(message)
    results = index.query(queries=[embedding], top_k=top_k)
    return results["matches"]

# Main chatbot function
def chatbot(message):
    # Retrieve similar messages
    matches = retrieve_from_pinecone(message)
    
    if matches:
        # If a close match is found, return the stored response
        closest_match = matches[0]
        stored_response = closest_match["metadata"]["response"]
        return f"Similar question: {closest_match['id']}\nStored response: {stored_response}"
    else:
        # If no close match is found, generate a new response
        response = generate_response(message)
        store_in_pinecone(message, response)
        return response
