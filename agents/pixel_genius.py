from crewai import Agent
from textwrap import dedent
from config import MODELS, AGENT_CONFIG
import json
import re
import os

class PixelGeniusAgent:
    def __init__(self):
        self.agent = Agent(
            role=AGENT_CONFIG['pixel_genius']['role'],
            goal=AGENT_CONFIG['pixel_genius']['goal'],
            backstory=AGENT_CONFIG['pixel_genius']['backstory'],
            verbose=True,
            allow_delegation=False,
            llm=self._get_llm(),
        )

    def _get_llm(self):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model_name=MODELS['design_agent'], temperature=0.7)

    def design_ui(self, requirements: str, platform: str = "web") -> dict:
        prompt = dedent(f"""
        **Design Requirements:**
        {requirements}
        
        **Platform:** {platform}
        
        **Your Task:**
        Create a comprehensive UI design specification including:
        - Color palette with hex codes
        - Typography system (fonts, sizes, weights)
        - Layout and component structure
        - Key screens or views with descriptions
        - UI components and their states
        - Responsive design considerations if applicable
        
        Format your response as JSON with the following structure:
        {{
          "design_system": {{
            "color_palette": {{
              "primary": "#hexcode",
              "secondary": "#hexcode",
              "accent": "#hexcode",
              "background": "#hexcode",
              "text": "#hexcode"
            }},
            "typography": {{
              "font_family": "font name",
              "font_sizes": {{
                "h1": "size",
                "h2": "size",
                "body": "size"
              }}
            }}
          }},
          "screens": [
            {{
              "name": "Screen name",
              "purpose": "Description of purpose",
              "components": ["list", "of", "components"]
            }}
          ],
          "components": [
            {{
              "name": "Component name",
              "description": "Component purpose",
              "states": ["default", "hover", "active", "disabled"]
            }}
          ]
        }}
        """)
        
        print(f"[PixelGenius] Designing UI for: {requirements}")
        response = self.agent.execute_task(task=prompt)
        
        try:
            json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            else:
                return json.loads(response)
        except json.JSONDecodeError:
            print(f"[PixelGenius] Error: Could not parse JSON response. Raw output: {response}")
            return {"error": "Failed to parse UI design"}

    def generate_css(self, design_spec: dict) -> str:
        prompt = dedent(f"""
        **Design Specification:**
        {json.dumps(design_spec, indent=2)}
        
        **Your Task:**
        Generate complete CSS code that implements this design specification.
        - Use modern CSS features (Flexbox, Grid, CSS Variables)
        - Make it responsive for different screen sizes
        - Include comments for clarity
        - Ensure it follows best practices
        
        Provide the CSS code in a single code block.
        """)
        
        print(f"[PixelGenius] Generating CSS from design spec")
        response = self.agent.execute_task(task=prompt)
        
        css_code = self._extract_code_blocks(response)
        
        if css_code:
            return list(css_code.values())[0]
        else:
            return response

    def _extract_code_blocks(self, text: str) -> dict:
        code_blocks = {}
        pattern = r"```(?:\w+)?\s*\n([\s\S]*?)```"
        matches = re.findall(pattern, text)
        
        for i, match in enumerate(matches):
            code_blocks[f"code_block_{i}"] = match.strip()
            
        return code_blocks
