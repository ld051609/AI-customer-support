from process import chatbot, store_in_pinecone
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
load_dotenv()

# Create a Pinecone index
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

# Test data
test_messages = [
    {"message": "Hello, how can I help you?", "response": "I'm here to assist you with your queries."},
    {"message": "What are the opening hours?", "response": "We are open from 9 AM to 5 PM, Monday to Friday."},
    {"message": "Where is your store located?", "response": "We are located at 123 Main Street, Springfield."}
]

# Store test data
for test in test_messages:
    store_in_pinecone(test["message"], test["response"])

# Test retrieval
for test in test_messages:
    retrieved_response = chatbot(test["message"])
    print(f"Input Message: {test['message']}")
    print(f"Expected Response: {test['response']}")
    print(f"Retrieved Response: {retrieved_response}")
    print()
    
# Print index stats to verify data
print(index.describe_index_stats())