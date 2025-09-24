from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
import re

class TerminalParserUI:
    def __init__(self):
        self.console = Console()
        
    def clean_text(self, text):
        """Clean and normalize the parsed text"""
        if isinstance(text, list):
            text = "\n".join(text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()
    
    def detect_sections(self, text):
        """Identify sections based on headers"""
        sections = []
        current_section = []
        header_level = 0
        
        for line in text.split('\n'):
            if line.startswith('## '):
                if current_section:
                    sections.append(('\n'.join(current_section), header_level))
                current_section = [line[3:]]
                header_level = 2
            elif line.startswith('# '):
                if current_section:
                    sections.append(('\n'.join(current_section), header_level))
                current_section = [line[2:]]
                header_level = 1
            else:
                current_section.append(line)
        
        if current_section:
            sections.append(('\n'.join(current_section), header_level))
            
        return sections
    
    def display(self, parsed_data):
        """Display parsed content with rich formatting"""
        clean_text = self.clean_text(parsed_data)
        sections = self.detect_sections(clean_text)
        
        if not sections:
            self.console.print(Markdown(clean_text))
            return
            
        for content, level in sections:
            if level == 1:
                self.console.print(Panel.fit(
                    Markdown(content),
                    border_style="bright_blue",
                    title_align="left"
                ))
            elif level == 2:
                self.console.print(Panel.fit(
                    Markdown(content),
                    border_style="bright_green", 
                    title_align="left"
                ))
            else:
                self.console.print(Markdown(content))
            self.console.print()