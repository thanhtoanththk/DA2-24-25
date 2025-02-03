from flask import Flask, request, jsonify
from model_utils import T5TextCorrector
from transformers import MT5Tokenizer, MT5ForConditionalGeneration

# Initialize Flask app
app = Flask(__name__)
corrector = T5TextCorrector()

@app.route('/correct', methods=['POST'])
def correct_text():
    # Get input text from the request
    input_data = request.form.get('incorrect_text')
    correct_texts = corrector.correct_text(input_data)
    # Return the corrected text as a JSON response
    return jsonify({"corrected_text": correct_texts})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
