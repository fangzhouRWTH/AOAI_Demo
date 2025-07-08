from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from openai import AzureOpenAI

load_dotenv()

app = Flask(__name__)

# openai.api_type = "azure"
# openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
# openai.api_key = os.getenv("AZURE_OPENAI_KEY")
# openai.api_version = os.getenv("AZURE_OPENAI_API_VERSION")
# deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT")

deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")

client = AzureOpenAI(
    api_version = os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_KEY")
)


from flask import render_template

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "you are helpful"},
                {"role": "user", "content": user_input}
            ],
            max_completion_tokens=100000,
            model=deployment
        )
        reply = response.choices[0].message.content
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)