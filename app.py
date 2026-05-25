import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image
import json
 
app = Flask(__name__)
 
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash-exp")
 
@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
 
    try:
        file = request.files['file']
        img = Image.open(file)
 
        prompt = """
        Look at this handwritten shopping list. 
        1. Extract all items.
        2. Categorize them by grocery store sections (e.g., Produce, Dairy, Meat, Pantry, etc.).
        3. Return ONLY a JSON object in this format: 
        {"Categories": [{"name": "Produce", "items": ["Apples", "Bananas"]}, {"name": "Dairy", "items": ["Milk"]}]}
        """
 
        response = model.generate_content([prompt, img])
        json_text = response.text.replace('```json', '').replace('```', '').strip()
        data = json.loads(json_text)
        return jsonify(data)
 
    except Exception as e:
        return jsonify({"error": str(e)}), 500
 
if __name__ == '__main__':
    app.run(debug=True)
 
