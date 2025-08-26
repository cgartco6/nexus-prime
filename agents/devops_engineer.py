from crewai import Agent
from textwrap import dedent
from config import MODELS, AGENT_CONFIG
import json
import re

class DevOpsEngineerAgent:
    def __init__(self):
        self.agent = Agent(
            role="DevOps Engineer & Infrastructure Specialist",
            goal="Design and implement scalable infrastructure and deployment pipelines.",
            backstory=dedent("""
                You are an experienced DevOps engineer with expertise in cloud infrastructure, CI/CD pipelines,
                and containerization. You've built scalable systems for high-traffic applications and optimized
                deployment processes for reliability and efficiency.
            """),
            verbose=True,
            allow_delegation=False,
            llm=self._get_llm(),
        )

    def _get_llm(self):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model_name=MODELS['architect'], temperature=0.1)

    def design_infrastructure(self, requirements: str, cloud_provider: str = "AWS") -> dict:
        prompt = dedent(f"""
        **Requirements:**
        {requirements}
        
        **Cloud Provider:** {cloud_provider}
        
        **Your Task:**
        Design a scalable infrastructure including:
        - Architecture diagram components
        - Services and their purposes
        - Scaling strategies
        - Security measures
        - Cost optimization considerations
        
        Format your response as JSON with the following structure:
        {{
          "architecture": "High-level architecture description",
          "services": [
            {{
              "name": "Service name",
              "purpose": "What it does",
              "specs": "Configuration details"
            }}
          ],
          "scaling_strategy": "How the system scales",
          "security_measures": ["list", "of", "security", "measures"],
          "cost_optimization": ["list", "of", "cost", "optimization", "strategies"]
        }}
        """)
        
        print(f"[DevOpsEngineer] Designing infrastructure for: {requirements}")
        response = self.agent.execute_task(task=prompt)
        
        try:
            json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            else:
                return json.loads(response)
        except json.JSONDecodeError:
            print(f"[DevOpsEngineer] Error: Could not parse JSON response. Raw output: {response}")
            return {"error": "Failed to parse infrastructure design"}
