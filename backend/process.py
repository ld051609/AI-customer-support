from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize Pinecone
pc = Pinecone(api_key=PINECONE_API_KEY)

# Set up Pinecone index
index_name = 'ai-customer-support'
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
client = OpenAI(
    api_key=OPENAI_API_KEY,
)

# Generate embeddings
def generate_embeddings(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    response = client.embeddings.create(input = [text], model=model)
    embedding = response.data[0].embedding
    return embedding


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

# Store embeddings and response in Pinecone
def store_in_pinecone(message, response):
    embedding = generate_embeddings(message)

    index.upsert(
        vectors=[
            {
                "id": message,
                "values": embedding,
                "metadata": {
                    "response": response
                }
            }
        ]
    )

# Retrieve response from Pinecone based on a query
def retrieve_from_pinecone(message):
    embedding = generate_embeddings(message)
    results = index.query(
        vector=embedding,
        top_k=1,
        include_metadata=True
    )
    print(results)
    return results['matches']


# Main chatbot function
def chatbot(message):
    # Retrieve similar messages
    matches = retrieve_from_pinecone(message)
    
    if matches:
        # If a close match is found, return the stored response
        closest_match = matches[0]
        stored_response = closest_match['metadata']['response']
        return stored_response
    else:
        # If no close match is found, generate a new response
        response = generate_response(message)
        store_in_pinecone(message, response)
        return response
    



