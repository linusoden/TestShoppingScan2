import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types
from PIL import Image
import io
import json
 
app = Flask(__name__)
 
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
 
    try:
        file = request.files['file']
        image_bytes = file.read()
 
        prompt = """
        Look at this handwritten shopping list. 
        1. Extract all items.
        2. Categorize them by grocery store sections (e.g., Produce, Dairy, Meat, Pantry, etc.).
        3. Return ONLY a JSON object in this format: 
        {"Categories": [{"name": "Produce", "items": ["Apples", "Bananas"]}, {"name": "Dairy", "items": ["Milk"]}]}
        """
 
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                types.Part.from_bytes(data=image_bytes, mime_type=file.mimetype),
                prompt
            ]
        )
 
        json_text = response.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(json_text)
        return jsonify(data)
 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
if __name__ == '__main__':
    app.run(debug=True)
 
