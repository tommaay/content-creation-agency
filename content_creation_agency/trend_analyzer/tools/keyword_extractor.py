from agency_swarm.tools import BaseTool
from pydantic import Field
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from collections import Counter
import string

# Download required NLTK data
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')

class KeywordExtractor(BaseTool):
    """
    A tool to extract keywords from text using NLTK.
    """
    text: str = Field(
        ..., description="The text to extract keywords from."
    )
    num_keywords: int = Field(
        10, description="Number of keywords to extract."
    )

    def run(self):
        """Extract keywords from the provided text."""
        try:
            # Tokenize and lowercase the text
            tokens = word_tokenize(self.text.lower())
            
            # Remove punctuation and stopwords
            stop_words = set(stopwords.words('english'))
            tokens = [word for word in tokens 
                     if word not in string.punctuation 
                     and word not in stop_words
                     and len(word) > 2]
            
            # Get part-of-speech tags
            pos_tags = pos_tag(tokens)
            
            # Keep only nouns and adjectives
            important_words = [word for word, pos in pos_tags 
                             if pos.startswith(('NN', 'JJ'))]
            
            # Count frequencies
            word_freq = Counter(important_words)
            
            # Get top keywords
            keywords = word_freq.most_common(self.num_keywords)
            
            return {
                "keywords": keywords,
                "total_words_analyzed": len(tokens)
            }
        except Exception as e:
            return f"Error extracting keywords: {str(e)}"

if __name__ == "__main__":
    sample_text = """
    Artificial Intelligence and Machine Learning continue to transform various industries.
    Deep learning models are becoming more sophisticated, while natural language processing
    makes significant strides in understanding human communication.
    """
    tool = KeywordExtractor(text=sample_text)
    print(tool.run()) 