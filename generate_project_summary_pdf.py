from fpdf import FPDF

# Read the summary text
with open('project_summary.txt', 'r', encoding='utf-8') as f:
    summary = f.read()

diagram = '''
+-------------------+       +-------------------+       +----------------------+
|   AI Agent (UI)   | <---> |    Frontend UI    | <---> |     REST API         |
| (Chatbot/Assistant|       | (React/Vue/HTML)  |       |  (FastAPI/Flask)     |
+-------------------+       +-------------------+       +----------------------+
         |                         |                               |
         | 1. User interacts       |                               |
         |    with AI agent/chat   |                               |
         |------------------------>|                               |
         | 2. Guided search, help  |                               |
         |    recommendations      |                               |
         |------------------------>|                               |
         | 3. Submit search query  |                               |
         |------------------------>|                               |
         |                        4. Auth check, route to provider |
         |                        5. Fetch & unify results         |
         |<------------------------|                               |
         | 6. Show results         |                               |
+-------------------+       +-------------------+       +----------------------+
| User Management   |       | Role-based Access |       | Unified Output Format|
+-------------------+       +-------------------+       +----------------------+
'''

import os

class PDF(FPDF):
    def header(self):
        # Add logo if available
        if os.path.exists('logo.png'):
            self.image('logo.png', 10, 8, 33)
            self.set_xy(10, 25)
        self.set_font('Arial', 'B', 14)
        self.cell(0, 10, 'Web Search App: Project Summary', ln=1, align='C')
        self.ln(5)

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 8, title, ln=1)
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Arial', '', 11)
        self.multi_cell(0, 7, body)
        self.ln(2)

    def diagram(self, diagram_text):
        self.set_font('Courier', '', 8)
        self.multi_cell(0, 5, diagram_text)
        self.ln(2)

    def diagram_image(self, path):
        self.image(path, x=30, w=150)
        self.ln(10)

pdf = PDF()
pdf.add_page()

# Split the summary into sections for better formatting
sections = summary.split('\n\n')
for section in sections:
    if section.strip().startswith('+-------------------+'):
        pdf.chapter_title('Architecture Diagram')
        # Try to add diagram image if it exists
        if os.path.exists('architecture_diagram.png'):
            pdf.diagram_image('architecture_diagram.png')
        else:
            pdf.diagram(diagram)
    elif section.strip().startswith('| Layer'):
        pdf.chapter_title('Summary Table')
        pdf.chapter_body(section)
    else:
        pdf.chapter_body(section)

pdf.output('project_summary.pdf')
print('PDF generated as project_summary.pdf')
