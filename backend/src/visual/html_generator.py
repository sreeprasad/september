from jinja2 import Environment, FileSystemLoader
import os
from datetime import datetime

class HTMLGenerator:
    """
    Generate HTML from Jinja2 template.
    """

    def __init__(self, template_dir="backend/templates"):
        # Adjust path if running from different context
        if not os.path.exists(template_dir):
             # Try absolute path based on file location
             current_dir = os.path.dirname(os.path.abspath(__file__))
             # Navigate up to backend/templates
             template_dir = os.path.join(current_dir, "../../../templates")
        
        self.env = Environment(loader=FileSystemLoader(template_dir))

    def generate(self, briefing_data: dict) -> str:
        """
        Render the HTML template with briefing data.
        """
        template = self.env.get_template("briefing.html")
        
        # Add timestamp if missing
        if "generated_at" not in briefing_data:
            briefing_data["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
        return template.render(**briefing_data)
