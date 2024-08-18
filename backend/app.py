from flask import Flask, request, jsonify
from flask_cors import CORS
from process import retrieve_from_pinecone, generate_response
app = Flask(__name__)
CORS(app)

# Main chatbot function
def chatbot(message):
    # Retrieve similar messages
    matches = retrieve_from_pinecone(message)
    
    if matches:
        # If a close match is found, return the stored metadata
        closest_match = matches[0]
        return f"Title: {closest_match['metadata']['title']}, URL: {closest_match['metadata']['url']}"
    else:
        # If no close match is found, generate a new response and return it
        response = generate_response(message)
        return response

@app.route('/', methods=['POST'])
def get_message():
    message = request.json['message']
    if not message:
        print("Please provide a message")
        return jsonify({"response": "Please provide a message"})
    response = chatbot(message)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
