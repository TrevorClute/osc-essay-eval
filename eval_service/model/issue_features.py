import language_tool_python

# 1. INITIALIZE THE TOOL
# We do this outside the function so we don't reload it 1,000 times.
# Note: On the first run, this might take a few seconds to download the Java tool.
tool = language_tool_python.LanguageTool('en-US', config={"cacheDir": "/tmp/lt_cache"})

def get_manual_features(text):
    """
    Analyzes an essay and returns a list of two numbers:
    1. Word Count (Length)
    2. Grammar Error Rate (Quality)
    """
    
    # A. Calculate Word Count
    # We split by spaces to count words.
    words = text.split()
    word_count = len(words)

    # B. Calculate Grammar Errors
    # tool.check returns a list of all matches (errors) found.
    matches = tool.check(text)
    error_count = len(matches)

    # C. Calculate Error Rate
    # (Errors per 100 words). 
    # If the essay is empty, we set error rate to a high number (100).
    if word_count > 0:
        error_rate = (error_count / word_count) * 100
    else:
        error_rate = 100.0

    # Return as a list of numbers [Float, Float]
    return [float(word_count), float(error_rate)]

# --- TEST BLOCK ---
# This only runs if you run "python issue_features.py" directly.
# It helps you verify that the grammar checker is actually working.
if __name__ == "__main__":
    test_essay = "I want to go to the unversity because its good."
    
    print(f"\nTesting with: '{test_essay}'")
    features = get_manual_features(test_essay)
    
    print(f"Word Count: {features[0]}")
    print(f"Error Rate: {features[1]:.2f}%") 
    # Expected: 'unversity' (spelling) and 'its' (grammar) should trigger errors.
