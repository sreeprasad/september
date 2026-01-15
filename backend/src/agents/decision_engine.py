from typing import List, Dict, Any
from ..schemas.navigator_output import Post

class NavigatorDecisionEngine:
    """
    The intelligence layer that makes Navigator stand out.
    Instead of scraping everything, we DECIDE what matters.
    """

    def prioritize_data_points(self, raw_posts: List[Dict[str, Any]], meeting_context: str) -> List[Dict[str, Any]]:
        """
        From many data points, surface the most relevant ones.
        
        Criteria:
        1. Relevance to first meeting context (keywords)
        2. Engagement (likes/comments)
        3. Recency vs significance
        """
        scored_posts = []
        
        # Simple heuristic keywords based on context
        keywords = []
        if "partnership" in meeting_context.lower():
            keywords = ["collaboration", "partner", "growth", "strategy"]
        elif "technical" in meeting_context.lower():
            keywords = ["architecture", "scale", "performance", "ai", "engineering"]
        else:
            keywords = ["vision", "culture", "team", "future"]

        for post in raw_posts:
            score = 0.5  # Base score
            
            # Engagement score (normalized)
            engagement = post.get("engagement", {"likes": 0, "comments": 0})
            total_engagement = engagement.get("likes", 0) + engagement.get("comments", 0) * 2
            if total_engagement > 100:
                score += 0.2
            elif total_engagement > 500:
                score += 0.4
                
            # Keyword matching
            content = post.get("content", "").lower()
            matches = [k for k in keywords if k in content]
            if matches:
                score += 0.3 * len(matches)
                
            # Cap score
            score = min(0.99, score)
            
            # Generate reason
            reason = self._generate_reason(post, matches, total_engagement)
            
            post_with_score = post.copy()
            post_with_score["priority_score"] = score
            post_with_score["priority_reason"] = reason
            scored_posts.append(post_with_score)

        # Sort by score descending and take top 5
        scored_posts.sort(key=lambda x: x["priority_score"], reverse=True)
        return scored_posts[:5]

    def _generate_reason(self, post: Dict, matches: List[str], engagement: int) -> str:
        reasons = []
        if matches:
            reasons.append(f"Aligns with meeting context ({', '.join(matches)})")
        if engagement > 100:
            reasons.append("High community engagement")
        
        if not reasons:
            return "General professional update"
            
        return " & ".join(reasons)

    def generate_reasoning(self, decisions: List[Dict]) -> List[str]:
        """
        Generate explanations for why each data point was selected.
        """
        return [f"Selected post from {d.get('date')} due to {d.get('priority_reason')}" for d in decisions]
