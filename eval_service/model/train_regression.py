import pandas as pd
import numpy as np
import joblib
from sentence_transformers import SentenceTransformer
from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix

from issue_features import get_manual_features

def train():
    embedder = SentenceTransformer('all-mpnet-base-v2')

    data_path = '../data/essays.csv'
    df = pd.read_csv(data_path)

    combined_text = [
        f"Question: {row['prompt_text']} \n Answer: {row['essay_text']}" 
        for _, row in df.iterrows()
    ]
    X_bert = embedder.encode(combined_text)

    X_manual = np.array([get_manual_features(text) for text in df['essay_text']])

    # COMBINE THEM
    # Stack the 768 BERT numbers + 2 Manual numbers side-by-side
    X_combined = np.hstack((X_bert, X_manual))
    
    # PREPARE TARGETS
    # Ensure scores are integers (0, 1, 2, 3)
    y = df['score'].astype(int).values

    # 4. TRAIN / TEST SPLIT
    # 80% for training, 20% for testing
    X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)

    # 5. TRAINING
    print("Training the Classifier...")
    # Class_weight='balanced' is crucial: it prevents the model from ignoring 
    # rare scores (like 0s) if your dataset is mostly 3s.
    clf = make_pipeline(StandardScaler(), SVC(kernel='linear', class_weight='balanced'))
    clf.fit(X_train, y_train)

    # 6. EVALUATION
    print("\n--- Training Complete. Evaluating... ---")
    preds = clf.predict(X_test)
    
    # Print the detailed report
    print(classification_report(y_test, preds, digits=3))
    
    # Quick sanity check on the first few test items
    print("\nSample Predictions:")
    for i in range(min(5, len(preds))):
        print(f"True Score: {y_test[i]} | Predicted: {preds[i]}")

    # 7. SAVE THE BRAIN
    output_file = 'classifier.pkl'
    joblib.dump(clf, output_file)
    print(f"\nSUCCESS: Model saved to '{output_file}'")

if __name__ == "__main__":
    train()
