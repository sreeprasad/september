import asyncio
import sys
import os

# Ensure we can import from src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.visual.pdf_generator import PDFGenerator

def verify_pdf_generation():
    print("--- Testing PDF Generation ---")
    
    mock_data = {
        "person": {
            "name": "Jane Doe",
            "role": "Chief Technology Officer",
            "company": "TechCorp",
            "professional_identity": "AI Strategy Leader",
            "photo_url": "" 
        },
        "themes": {
            "frequency_breakdown": {
                "AI Strategy": 0.45,
                "Cloud Infrastructure": 0.30,
                "Digital Transformation": 0.25
            }
        },
        "talking_points": [
            {"point": "Discuss AI Governance", "context": "Relevant to recent posts"},
            {"point": "Cloud Migration Challenges", "context": "Aligns with company news"},
            {"point": "Team Scaling", "context": "Based on job postings"}
        ],
        "company_context": {
            "name": "TechCorp",
            "recent_developments": ["Series B Funding Announced", "New Product Launch"]
        },
        "sentiment": {
            "communication_style": "Direct and strategic"
        }
    }
    
    try:
        generator = PDFGenerator()
        pdf_bytes = generator.generate(mock_data)
        
        output_path = "test_briefing.pdf"
        with open(output_path, "wb") as f:
            f.write(pdf_bytes)
            
        print(f"SUCCESS: PDF generated at {output_path} ({len(pdf_bytes)} bytes)")
        
        # Verify file exists and has content
        if os.path.exists(output_path) and os.path.getsize(output_path) > 0:
            print("Verification: File exists and is not empty.")
        else:
            print("FAILURE: File not created or empty.")
            
    except Exception as e:
        print(f"FAILURE: PDF generation error: {e}")

if __name__ == "__main__":
    verify_pdf_generation()
