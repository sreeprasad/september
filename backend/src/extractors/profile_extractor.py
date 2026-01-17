import agentql
from typing import List, Dict, Any
from collections import Counter
import re

class SemanticProfileExtractor:
    """
    Uses semantic analysis to extract and structure profile data.
    """

    def __init__(self):
        pass

    async def extract_profile_themes(self, raw_posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract themes from posts using simple keyword frequency analysis.
        """
        # Combine all post content safely
        safe_content = []
        for p in raw_posts:
            if p and isinstance(p, dict) and p.get("content"):
                safe_content.append(p.get("content", ""))
                
        text = " ".join([c.lower() for c in safe_content])
        
        # Simple stop words (expand as needed)
        stop_words = {
            "the", "and", "a", "to", "of", "in", "is", "for", "on", "with", "my", "at", "it", "this", "that", "are", "was", "be", "as",
            "about", "from", "have", "would", "will", "just", "like", "more", "wanted", "share", "something", "thanks", "please",
            "what", "when", "where", "who", "which", "why", "how", "can", "could", "should", "your", "their", "our", "been", "has",
            "there", "here", "really", "very", "much", "also", "some", "other", "into", "over", "after", "before", "out", "only",
            "want", "need", "good", "great", "best", "better", "know", "think", "make", "take", "time", "work", "people", "years"
        }
        
        # Tokenize and filter
        words = re.findall(r'\w+', text)
        filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
        
        # Count frequency
        word_counts = Counter(filtered_words)
        common = word_counts.most_common(5)
        
        total_words = sum(word_counts.values()) or 1
        frequency_breakdown = {word: count/total_words for word, count in common}
        
        primary_theme = common[0][0] if common else "general technology"
        
        return {
            "primary_theme": primary_theme,
            "theme_frequency": frequency_breakdown,
            "professional_identity": f"Professional focused on {primary_theme}"
        }

    async def extract_sentiment_patterns(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Extract sentiment patterns (simplified).
        """
        # Combine all post content safely
        safe_content = []
        for p in posts:
            if p and isinstance(p, dict) and p.get("content"):
                safe_content.append(p.get("content", ""))
                
        text = " ".join([c.lower() for c in safe_content])
        
        # Basic keyword matching for sentiment
        positive_words = {"excited", "happy", "great", "love", "amazing", "proud", "grateful", "best", "good"}
        concerns_words = {"challenge", "problem", "issue", "debt", "complex", "hard", "difficult", "struggle"}
        
        pos_count = sum(1 for w in text.split() if w in positive_words)
        neg_count = sum(1 for w in text.split() if w in concerns_words)
        
        sentiment = "positive" if pos_count >= neg_count else "concerned"
        
        return {
            "overall_sentiment": sentiment,
            "passion_topics": ["technology", "growth"], 
            "concerns": ["complexity"] if neg_count > 0 else [],
            "communication_style": "professional"
        }
