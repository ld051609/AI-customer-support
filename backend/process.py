from openai import OpenAI
from langchain_community.embeddings import OpenAIEmbeddings
import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
load_dotenv()
import tiktoken  

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Initialize Pinecone (use correct import if using newer version)
pc = Pinecone(api_key=os.environ.get("PINECONE_API_KEY"))
index_name = 'ai-customer-support-chatbot-2'

if index_name in pc.list_indexes().names():
    pc.delete_index(index_name)

if index_name not in pc.list_indexes():
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="dotproduct",
        spec=ServerlessSpec(
            cloud='aws',
            region='us-east-1'
        )
    )

# Connect to Pinecone index
index = pc.Index(index_name)


# Function to count tokens using tiktoken
def count_tokens(text):
    encoder = tiktoken.get_encoding("cl100k_base")
    tokens = encoder.encode(text)
    return len(tokens)

# Function to split text into chunks based on token count
def split_into_chunks(text, max_tokens):
    encoder = tiktoken.get_encoding("cl100k_base")
    tokens = encoder.encode(text)
    chunks = [tokens[i:i + max_tokens] for i in range(0, len(tokens), max_tokens)]
    return [encoder.decode(chunk) for chunk in chunks]

# Function to generate embeddings
def generate_embeddings(text, model="text-embedding-ada-002"):
    max_tokens = 8192
    chunks = split_into_chunks(text, max_tokens)
    
    embeddings = []
    for chunk in chunks:
        response = client.embeddings.create(
            input=[chunk],
            model=model
        )
        # Access the embedding from the response object
        embedding = response.data[0].embedding
        embeddings.append(embedding)
    
    return embeddings


# Function to create chatbot response using OpenAI
def generate_response(prompt):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

# Function to retrieve response from Pinecone based on a query
def retrieve_from_pinecone(message):
    embedding = generate_embeddings(message)
    results = index.query(
        vector=embedding,
        top_k=3,
        include_metadata=True
    )
    return results['matches']
