import nltk
from collections import Counter
import re
from typing import List

# Download required NLTK data on first run
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)

from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

class TextSummarizer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
    
    def clean_text(self, text: str) -> str:
        """Remove special characters and extra whitespace"""
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def extract_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        return sent_tokenize(text)
    
    def score_sentences(self, sentences: List[str]) -> dict:
        """Score sentences based on word frequency"""
        # Tokenize all words
        words = []
        for sentence in sentences:
            words.extend([
                word.lower() for word in word_tokenize(sentence)
                if word.isalnum() and word.lower() not in self.stop_words
            ])
        
        # Calculate word frequencies
        word_freq = Counter(words)
        max_freq = max(word_freq.values()) if word_freq else 1
        
        # Normalize frequencies
        for word in word_freq:
            word_freq[word] = word_freq[word] / max_freq
        
        # Score sentences
        sentence_scores = {}
        for i, sentence in enumerate(sentences):
            score = 0
            words_in_sentence = [
                word.lower() for word in word_tokenize(sentence)
                if word.isalnum()
            ]
            for word in words_in_sentence:
                if word in word_freq:
                    score += word_freq[word]
            
            # Average score per word in sentence
            if words_in_sentence:
                sentence_scores[i] = score / len(words_in_sentence)
        
        return sentence_scores
    
    def summarize(self, text: str, max_sentences: int = 5) -> dict:
        """Generate extractive summary"""
        cleaned = self.clean_text(text)
        sentences = self.extract_sentences(cleaned)
        
        if len(sentences) <= max_sentences:
            return {
                'summary': cleaned,
                'original_length': len(text),
                'summary_length': len(cleaned),
                'sentences_count': len(sentences),
                'truncated': False
            }
        
        # Score and rank sentences
        scores = self.score_sentences(sentences)
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Select top sentences and maintain original order
        top_indices = sorted([idx for idx, _ in ranked[:max_sentences]])
        summary_sentences = [sentences[i] for i in top_indices]
        summary = ' '.join(summary_sentences)
        
        return {
            'summary': summary,
            'original_length': len(text),
            'summary_length': len(summary),
            'sentences_count': len(summary_sentences),
            'truncated': len(sentences) > max_sentences
        }

# Global instance
summarizer = TextSummarizer()
