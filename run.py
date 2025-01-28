import nltk
from app import create_app

def setup_nltk():
    """Download required NLTK resources"""
    try:
        nltk.download('punkt')
        nltk.download('punkt_tab')
        print("NLTK resources downloaded successfully")
    except Exception as e:
        print(f"Error downloading NLTK resources: {e}")
        raise

# Initialize NLTK resources
setup_nltk()

# Create Flask app
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)