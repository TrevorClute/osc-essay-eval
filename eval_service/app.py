from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from pathlib import Path
import joblib
import numpy as np
from sentence_transformers import SentenceTransformer
from model.issue_features import get_manual_features  # Import your grammar helper
from mangum import Mangum

# env_path = Path(__file__).resolve().parent / '.env'
# load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
INTERNAL_API_KEY = os.getenv('FLASK_API_KEY')

def validate_request(func):
    def wrapper(*args, **kwargs):
        incoming_key = request.headers.get('X-Internal-Secret')
        if incoming_key != INTERNAL_API_KEY:
            return jsonify({"error": "Unauthorized System Access"}), 401
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


MODEL_PATH = 'model/classifier.pkl' 
TRANSFORMER_NAME = 'all-mpnet-base-v2'  

PROMPT_MAP = {
    1: "Why would you be a good candidate for the program?",
    2: "How might you benefit from participation in the program?",
    3: "Give an example of your work on a group project. Describe your role, any successes, and how you handled any frustrations.",
    4: "Please look at the past student projects in the archives on this website and detail which ones are of interest to you and why."
}

clf = joblib.load(MODEL_PATH)
embedder = SentenceTransformer(TRANSFORMER_NAME)

@app.route('/evaluate', methods=['POST'])
@validate_request
def analyze_essay():
    data = request.json

    essay_text = data.get('essay_text', '')
    prompt_id = data.get('prompt_id', 1)

    prompt_text = PROMPT_MAP.get(prompt_id, "")

    fusion_string = f"Question: {prompt_text} \n Answer: {essay_text}"

    features_bert = embedder.encode([fusion_string])

    stats = get_manual_features(essay_text)
    features_manual = np.array([stats])

    features_final = np.hstack((features_bert, features_manual))

    prediction = clf.predict(features_final)[0]

    return jsonify({
        "score": int(prediction),  # Convert numpy int to python int
        "grammar_error_rate": stats[1],
        "word_count": stats[0]
    })


if __name__ == '__main__':
    app.run(port=5001, debug=True)
