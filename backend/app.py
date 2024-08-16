from flask import Flask, request, jsonify
from flask_cors import CORS
from process import chatbot
app = Flask(__name__)
CORS(app)

@app.route('/', methods=['POST'])
def chatbot():
    message = request.json['message']
    if not message:
        print("Please provide a message")
        return jsonify({"response": "Please provide a message"})
    response = chatbot(message)
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
