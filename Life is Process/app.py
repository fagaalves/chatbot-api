from flask import Flask, request, jsonify
import os
import openai

app = Flask(__name__)

# Load OpenAI API Key from Environment Variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Chatbot API is running!"

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Send message to OpenAI ChatGPT
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are a helpful relationship coach."},
                      {"role": "user", "content": user_message}]
        )

        bot_reply = response["choices"][0]["message"]["content"]

        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Set Port to 10000 (Render Requirement)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)
