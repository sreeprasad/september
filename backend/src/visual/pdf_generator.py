from fpdf import FPDF
import io
from .freepik_service import FreepikService

class PDFGenerator:
    """
    Generate PDF using FPDF2 (Pure Python).
    """

    def generate(self, briefing_data: dict) -> bytes:
        """
        Generate PDF bytes from briefing data.
        """
        pdf = FPDF(orientation="P", unit="mm", format="Letter")
        pdf.add_page()
        
        # Colors
        primary_color = (79, 70, 229) # #4F46E5
        
        # Header
        pdf.set_fill_color(*primary_color)
        pdf.rect(0, 0, 216, 40, 'F')
        
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 24)
        pdf.set_y(15)
        pdf.cell(0, 10, "MEETING BRIEFING", align="C", new_x="LMARGIN", new_y="NEXT")
        
        person_name = briefing_data.get("person", {}).get("name", "Unknown")
        pdf.set_font("Helvetica", "", 14)
        pdf.cell(0, 10, person_name, align="C", new_x="LMARGIN", new_y="NEXT")
        
        # Reset colors
        pdf.set_text_color(0, 0, 0)
        pdf.set_y(50)
        
        # Profile Section
        person = briefing_data.get("person", {})
        pdf.set_font("Helvetica", "B", 16)
        pdf.cell(0, 10, person.get("name", ""), new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("Helvetica", "", 12)
        role_company = f"{person.get('role', '')} at {person.get('company', '')}"
        pdf.cell(0, 8, role_company, new_x="LMARGIN", new_y="NEXT")
        
        pdf.set_font("Helvetica", "I", 11)
        pdf.set_text_color(100, 100, 100)
        pdf.cell(0, 8, person.get("professional_identity", ""), new_x="LMARGIN", new_y="NEXT")
        
        pdf.ln(10)
        
        # Themes Section
        pdf.set_text_color(79, 70, 229)
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "WHAT THEY CARE ABOUT", border="B", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)
        
        themes = briefing_data.get("themes", {}).get("frequency_breakdown", {})
        
        # Add Freepik Icon for top theme (Freepik Integration)
        if themes:
            try:
                top_theme = list(themes.keys())[0]
                freepik = FreepikService()
                # Generate icon for the top theme
                icon_b64 = freepik.generate_image(f"icon representing {top_theme}, minimalist vector style, blue and white")
                
                if icon_b64:
                    import base64
                    img_data = base64.b64decode(icon_b64)
                    # Position icon to the right of the header
                    current_y = pdf.get_y()
                    # Using io.BytesIO(img_data)
                    pdf.image(io.BytesIO(img_data), x=150, y=current_y - 20, w=30)
            except Exception as e:
                print(f"Failed to add Freepik icon: {e}")

        if themes:
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(0, 0, 0)
            
            for theme, percentage in themes.items():
                pdf.cell(60, 8, theme)
                
                # Draw bar
                bar_width = percentage * 100 # Scale to max 100mm
                x = pdf.get_x()
                y = pdf.get_y()
                pdf.set_fill_color(*primary_color)
                pdf.rect(x, y+2, bar_width, 4, 'F')
                
                pdf.set_x(x + 110)
                pdf.cell(20, 8, f"{int(percentage * 100)}%", new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.set_font("Helvetica", "I", 11)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 8, "No theme data available.", new_x="LMARGIN", new_y="NEXT")

        pdf.ln(10)

        # Talking Points Section
        pdf.set_text_color(79, 70, 229)
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 10, "TALKING POINTS", border="B", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(5)
        
        talking_points = briefing_data.get("talking_points", [])
        if talking_points:
            for point in talking_points:
                pdf.set_text_color(0, 0, 0)
                pdf.set_font("Helvetica", "B", 11)
                
                # Bullet point
                current_y = pdf.get_y()
                pdf.set_x(10)
                pdf.cell(5, 8, "-")
                
                # Text content
                pdf.set_x(15)
                point_text = point.get("point", "")
                pdf.multi_cell(0, 8, point_text)
                
                context = point.get("context", "")
                if context:
                    pdf.set_x(15)
                    pdf.set_font("Helvetica", "", 10)
                    pdf.set_text_color(80, 80, 80)
                    pdf.multi_cell(0, 6, context)
                
                pdf.ln(2)
        else:
            pdf.set_font("Helvetica", "I", 11)
            pdf.set_text_color(100, 100, 100)
            pdf.cell(0, 8, "No talking points generated.", new_x="LMARGIN", new_y="NEXT")

        pdf.ln(10)
        
        # Quick Facts / Footer
        pdf.set_y(-30)
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(150, 150, 150)
        generated_at = briefing_data.get("generated_at", "Just now")
        pdf.cell(0, 10, f"Generated by Brief Me | {generated_at}", align="C")

        return bytes(pdf.output())
