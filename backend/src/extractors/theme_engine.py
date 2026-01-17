from typing import List, Dict, Any
from collections import Counter
import re

class ThemeIdentificationEngine:
    """
    Goes beyond text parsing to identify meaningful themes.
    """

    def identify_themes(self, content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Identify and rank themes from content using frequency analysis.
        """
        text = " ".join([p.get("content", "").lower() for p in content])
        
        stop_words = {
            "the", "and", "a", "to", "of", "in", "is", "for", "on", "with", "my", "at", "it", "this", "that", "are", "was", "be", "as",
            "about", "from", "have", "would", "will", "just", "like", "more", "wanted", "share", "something", "thanks", "please",
            "what", "when", "where", "who", "which", "why", "how", "can", "could", "should", "your", "their", "our", "been", "has",
            "there", "here", "really", "very", "much", "also", "some", "other", "into", "over", "after", "before", "out", "only",
            "want", "need", "good", "great", "best", "better", "know", "think", "make", "take", "time", "work", "people", "years"
        }
        
        words = re.findall(r'\w+', text)
        filtered_words = [w for w in words if w not in stop_words and len(w) > 3]
        
        word_counts = Counter(filtered_words)
        common = word_counts.most_common(5)
        
        total_words = sum(word_counts.values()) or 1
        frequency_breakdown = {word: count/total_words for word, count in common}
        
        primary = common[0][0] if common else "technology"
        secondary = [w for w, c in common[1:]]
        
        return {
            "primary": primary,
            "secondary": secondary,
            "frequency_breakdown": frequency_breakdown
        }

    def generate_theme_insights(self, themes: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate human-readable insights from themes.
        """
        primary = themes.get("primary", "technology")
        frequency = themes.get("frequency_breakdown", {}).get(primary, 0)
        
        return [
            {
                "insight": f"Posts about {primary} with {(frequency*100):.1f}% frequency.",
                "confidence": 0.85,
                "evidence": ["frequency_analysis"]
            }
        ]
