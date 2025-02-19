import os
from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Load OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return "Chatbot API is running!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    if not OPENAI_API_KEY:
        return jsonify({"error": "API key not configured"}), 500

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": user_message}],
            api_key=OPENAI_API_KEY
        )
        return jsonify({"response": response["choices"][0]["message"]["content"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Explicitly set the correct port for Render
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Ensure port is detected correctly
    app.run(host='0.0.0.0', port=port, debug=True)
