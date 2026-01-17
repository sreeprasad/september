from typing import List, Dict, Any

class ResponseCoach:
    """
    Generate suggested responses and coaching tips using LLM.
    """
    def __init__(self, llm_client=None):
        self.llm_client = llm_client

    async def generate_response_strategies(
        self,
        questions: List[Dict[str, Any]],
        profile_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        For each likely question, generate response strategies.
        """
        if not self.llm_client:
             # Fallback
             return [
                 {
                     "question": q["question"],
                     "response_framework": "Listen -> Acknowledge -> Solve",
                     "emphasize": ["Value"],
                     "avoid": ["Jargon"],
                     "pivot_options": ["Let's focus on results."],
                     "follow_up_prepared": ["Does that make sense?"]
                 } for q in questions
             ]

        strategies = []
        
        name = profile_data.get('name', 'They')
        role = profile_data.get('role', 'Professional')

        for question_obj in questions:
            question_text = question_obj.get("question", "")
            
            prompt = f"""
            You are an executive negotiation coach. 
            The person asking the question is {name}, a {role}.
            
            The question is: "{question_text}"
            
            Generate a response strategy.
            Return valid JSON:
            {{
                "question": "{question_text}",
                "response_framework": "Name of framework (e.g. STAR, PPP)",
                "emphasize": ["Key point 1", "Key point 2"],
                "avoid": ["Pitfall 1", "Pitfall 2"],
                "pivot_options": ["Pivot phrase 1", "Pivot phrase 2"],
                "follow_up_prepared": ["Follow up 1", "Follow up 2"]
            }}
            """
            
            try:
                message = self.llm_client.messages.create(
                    model="claude-sonnet-4-5",
                    max_tokens=800,
                    messages=[{"role": "user", "content": prompt}]
                )
                response_text = message.content[0].text
                import json
                if "```json" in response_text:
                    response_text = response_text.split("```json")[1].split("```")[0]
                elif "```" in response_text:
                     response_text = response_text.split("```")[1].split("```")[0]
                strategies.append(json.loads(response_text))
            except Exception as e:
                print(f"Error generating strategy: {e}")
                strategies.append({
                    "question": question_text,
                    "response_framework": "Direct Answer",
                    "emphasize": ["Clarity"],
                    "avoid": ["Ambiguity"],
                    "pivot_options": [],
                    "follow_up_prepared": []
                })

        return strategies

