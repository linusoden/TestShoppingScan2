import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from PIL import Image
import json

app = Flask(__name__)

# Configure Gemini API (You'll get this key from Google AI Studio)
genai.configure(api_key="YOUR_GEMINI_API_KEY")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
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
    
    # Clean up the response to ensure it's valid JSON
    json_text = response.text.replace('```json', '').replace('```', '').strip()
    data = json.loads(json_text)
    
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)