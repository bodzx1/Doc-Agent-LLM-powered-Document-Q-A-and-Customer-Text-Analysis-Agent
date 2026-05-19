import warnings
from dotenv import load_dotenv
load_dotenv()
import docagent.tools as tools

def test_calculator_tool():
    print("--- Running Tool Tests ---")
    
    # Test case 1: Standard math
    res1 = tools.calculator("2 + 2 * 5")
    print(f"Test 1 (2 + 2 * 5): {res1} (Expected: 12)")
    
    # Test case 2: Complex math
    res2 = tools.calculator("sin(30) + 2**3")
    print(f"Test 2 (sin(30) + 2**3): {res2}")
    
    # Test case 3: Edge case / Error handling
    try:
        res3 = tools.calculator("2 / 0")
        print(f"Test 3 (2 / 0): {res3}")
    except Exception as e:
        print(f"Test 3 (2 / 0): Handled exception successfully -> {e}")
def test_web_search_tool():
    print("--- Running Web Search Tool Test ---")
    
    # Test case: Basic search query
    query = "What is the capital of France?"
    res = tools.web_search(query)
    print(f"Web Search Result for '{query}':\n{res}")
def test_retrieve_docs_tool():
    print("--- Running Retrieve Docs Tool Test ---")
    warnings.filterwarnings("ignore")
    
    # Test case: Basic document retrieval query
    query = "What are the main themes in the documents?"
    res = tools.retrieve_docs.invoke(query)
    print(f"Retrieve Docs Result for '{query}':\n")
    print(res)
def test_extract_themes_tool():
    print("--- Running Extract Themes Tool Test ---")
    
    # Test case: Basic theme extraction query
    text = "I love the product but the customer service could be better. The interface is intuitive and easy to use."
    res = tools.extract_themes.invoke(text)
    print(f"Extract Themes Result for provided customer feedback:\n{text}\nResult:\n{res}")
def test_analyze_sentiment_tool():
    print("--- Running Analyze Sentiment Tool Test ---")
    
    # Test case: Basic sentiment analysis query
    text = "I love the product but the customer service could be better. The interface is intuitive and easy to use."
    res = tools.analyze_sentiment.invoke(text)
    print(f"Analyze Sentiment Result for provided customer feedback:\n{text}\nResult:\n{res}")
if __name__ == "__main__":
    #test_calculator_tool()
    # test_web_search_tool()
    #test_retrieve_docs_tool()
    test_extract_themes_tool()
    test_analyze_sentiment_tool()
    
