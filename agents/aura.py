from crewai import Agent
from textwrap import dedent
from config import MODELS, AGENT_CONFIG
import json
import re

class AuraAgent:
    def __init__(self):
        self.agent = Agent(
            role=AGENT_CONFIG['aura']['role'],
            goal=AGENT_CONFIG['aura']['goal'],
            backstory=AGENT_CONFIG['aura']['backstory'],
            verbose=True,
            allow_delegation=False,
            llm=self._get_llm(),
        )

    def _get_llm(self):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model_name=MODELS['audio_agent'], temperature=0.7)

    def design_soundscape(self, context: str, mood: str) -> dict:
        prompt = dedent(f"""
        **Context:** {context}
        **Mood:** {mood}
        
        **Your Task:**
        Design a complete soundscape including:
        - Ambient sounds and background audio
        - Key sound effects and when they should trigger
        - Music recommendations (genre, tempo, instrumentation)
        - Audio mixing guidelines (volume levels, panning)
        - Implementation considerations
        
        Format your response as JSON with the following structure:
        {{
          "soundscape_description": "Overall description of the audio experience",
          "ambient_sounds": ["list", "of", "ambient", "sounds"],
          "sound_effects": [
            {{
              "name": "SFX name",
              "description": "What it represents",
              "trigger": "When it should play"
            }}
          ],
          "music": {{
            "genre": "Music genre",
            "tempo": "BPM range",
            "instruments": ["list", "of", "instruments"],
            "mood": "Emotional quality"
          }},
          "mixing_guidelines": {{
            "ambient_volume": "relative level",
            "sfx_volume": "relative level",
            "music_volume": "relative level"
          }}
        }}
        """)
        
        print(f"[Aura] Designing soundscape for: {context}")
        response = self.agent.execute_task(task=prompt)
        
        try:
            json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            else:
                return json.loads(response)
        except json.JSONDecodeError:
            print(f"[Aura] Error: Could not parse JSON response. Raw output: {response}")
            return {"error": "Failed to parse soundscape design"}

    def compose_music_brief(self, requirements: str) -> dict:
        prompt = dedent(f"""
        **Requirements:** {requirements}
        
        **Your Task:**
        Create a detailed music composition brief including:
        - Musical style and genre
        - Tempo and time signature
        - Key and harmonic structure
        - Instrumentation and arrangement
        - Emotional arc and dynamics
        - Reference tracks if applicable
        
        Format your response as JSON with the following structure:
        {{
          "composition_brief": "Overall description of the music",
          "style": "Musical style",
          "tempo": "BPM range",
          "time_signature": "e.g., 4/4",
          "key": "Primary key",
          "instrumentation": ["list", "of", "instruments"],
          "structure": {{
            "intro": "Description",
            "verse": "Description",
            "chorus": "Description",
            "bridge": "Description",
            "outro": "Description"
          }},
          "emotional_arc": "How the emotion changes throughout"
        }}
        """)
        
        print(f"[Aura] Creating music brief for: {requirements}")
        response = self.agent.execute_task(task=prompt)
        
        try:
            json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            else:
                return json.loads(response)
        except json.JSONDecodeError:
            print(f"[Aura] Error: Could not parse JSON response. Raw output: {response}")
            return {"error": "Failed to parse music brief"}
