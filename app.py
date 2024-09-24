from flask import Flask, request, Response, jsonify, stream_with_context
from chatbot import chatbot_response
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

def generate_event(user_input):
    for token in chatbot_response(user_input, stream_to_terminal=True):
        data = json.dumps({"message": token})
        yield f"data: {data}\n\n"
    yield "event: end\ndata: {}\n\n"


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No message provided"}), 400
    
    return Response(stream_with_context(generate_event(user_input)), 
                    content_type='text/event-stream')

if __name__ == '__main__':
    app.run(debug=True)
