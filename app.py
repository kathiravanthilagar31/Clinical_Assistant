import os
from flask import Flask, request, jsonify, render_template
from src.helper import init_rag_engine

# --- FLASK APPLICATION SETUP ---
app = Flask(__name__, template_folder='templates')
query_engine = init_rag_engine()

# --- ROUTES ---
@app.route('/')
def home():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat_endpoint():
    """Handles chat queries via an API endpoint."""
    if not query_engine:
        return jsonify({"error": "Chatbot not initialized correctly."}), 500

    data = request.get_json()
    user_query = data.get('query')
    if not user_query:
        return jsonify({"error": "No query provided."}), 400


    # Use .chat() for the ChatEngine
    response = query_engine.chat(user_query) 
    return jsonify({"response": str(response)})

if __name__ == '__main__':
    app.run(debug=False, host="0.0.0.0", port=8080)