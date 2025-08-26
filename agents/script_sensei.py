from crewai import Agent
from textwrap import dedent
from config import MODELS, AGENT_CONFIG
import json
import re

class ScriptSenseiAgent:
    def __init__(self):
        self.agent = Agent(
            role=AGENT_CONFIG['script_sensei']['role'],
            goal=AGENT_CONFIG['script_sensei']['goal'],
            backstory=AGENT_CONFIG['script_sensei']['backstory'],
            verbose=True,
            allow_delegation=False,
            llm=self._get_llm(),
        )

    def _get_llm(self):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model_name=MODELS['content_agent'], temperature=0.8)

    def create_content(self, topic: str, format: str, tone: str = "professional") -> str:
        prompt = dedent(f"""
        **Topic:** {topic}
        **Format:** {format}
        **Tone:** {tone}
        
        **Your Task:**
        Create engaging and well-structured content based on the above parameters.
        - Ensure it's appropriate for the specified format
        - Maintain a consistent tone throughout
        - Make it informative and engaging
        - Follow best practices for the format
        
        Provide the complete content in your response.
        """)
        
        print(f"[ScriptSensei] Creating {format} content about: {topic}")
        return self.agent.execute_task(task=prompt)

    def develop_story(self, premise: str, genre: str, length: str = "short") -> dict:
        prompt = dedent(f"""
        **Premise:** {premise}
        **Genre:** {genre}
        **Length:** {length}
        
        **Your Task:**
        Develop a complete story structure including:
        - Main characters with descriptions and motivations
        - Plot outline with beginning, middle, and end
        - Key scenes or events
        - Themes and messages
        - Setting and world-building elements
        
        Format your response as JSON with the following structure:
        {{
          "title": "Story title",
          "premise": "Story premise",
          "genre": "Story genre",
          "characters": [
            {{
              "name": "Character name",
              "role": "Protagonist/Antagonist/Supporting",
              "description": "Physical and personality description",
              "motivation": "What drives this character"
            }}
          ],
          "plot": {{
            "beginning": "Setup and inciting incident",
            "middle": "Development and conflicts",
            "end": "Climax and resolution"
          }},
          "key_scenes": [
            "Description of key scene 1",
            "Description of key scene 2"
          ],
          "themes": ["list", "of", "themes"]
        }}
        """)
        
        print(f"[ScriptSensei] Developing {genre} story: {premise}")
        response = self.agent.execute_task(task=prompt)
        
        try:
            json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            else:
                return json.loads(response)
        except json.JSONDecodeError:
            print(f"[ScriptSensei] Error: Could not parse JSON response. Raw output: {response}")
            return {"error": "Failed to parse story development"}

    def generate_dialogue(self, characters: list, context: str) -> str:
        characters_str = "\n".join([f"- {char}" for char in characters])
        
        prompt = dedent(f"""
        **Characters:**
        {characters_str}
        
        **Context:**
        {context}
        
        **Your Task:**
        Write natural and engaging dialogue for these characters in this context.
        - Give each character a distinct voice
        - Ensure the dialogue moves the scene forward
        - Include appropriate emotional tones
        - Format it as a script with character names and dialogue
        
        Provide the complete dialogue in your response.
        """)
        
        print(f"[ScriptSensei] Generating dialogue for {len(characters)} characters")
        return self.agent.execute_task(task=prompt)
