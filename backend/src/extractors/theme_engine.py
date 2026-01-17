from typing import List, Dict, Any
from collections import Counter
import re
import json

class ThemeIdentificationEngine:
    """
    Goes beyond text parsing to identify meaningful themes.
    """

    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    def identify_themes(self, content: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Identify and rank themes from content using frequency analysis or LLM.
        """
        # Handle None in content
        safe_content = []
        for p in content:
            if p and isinstance(p, dict) and p.get("content"):
                safe_content.append(p.get("content", ""))
        
        text = " ".join([c.lower() for c in safe_content])
        
        if self.llm_client and text.strip():
            try:
                return self._identify_themes_llm(safe_content)
            except Exception as e:
                print(f"LLM Theme extraction failed: {e}. Falling back to frequency analysis.")

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

    def _identify_themes_llm(self, posts: List[str]) -> Dict[str, Any]:
        """
        Use LLM to identify themes from posts.
        """
        # Truncate posts if too long
        posts_text = "\n---\n".join(posts[:20]) # Limit to 20 posts
        
        prompt = f"""
        Analyze the following social media posts to identify the key professional themes and topics this person discusses.
        
        POSTS:
        {posts_text}
        
        Identify:
        1. The Primary Theme (the single most dominant topic)
        2. Secondary Themes (2-4 other important topics)
        3. A rough frequency/importance score for each (0.0 to 1.0)
        
        Return JSON in this format:
        {{
            "primary": "Theme Name",
            "secondary": ["Theme 2", "Theme 3", "Theme 4"],
            "frequency_breakdown": {{
                "Theme Name": 0.8,
                "Theme 2": 0.5,
                "Theme 3": 0.3
            }}
        }}
        """
        
        message = self.llm_client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=500,
            messages=[{"role": "user", "content": prompt}]
        )
        
        response_text = message.content[0].text
        
        # Parse JSON
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0]
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0]
            
        return json.loads(response_text)

    def generate_theme_insights(self, themes: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Generate human-readable insights from themes.
        """
        primary = themes.get("primary", "technology")
        frequency = themes.get("frequency_breakdown", {}).get(primary, 0)
        
        return [
            {
                "insight": f"Primary focus on {primary} (approx. {int(frequency*100)}% relevance).",
                "confidence": 0.85,
                "evidence": ["content_analysis"]
            }
        ]
