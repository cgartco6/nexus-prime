from crewai import Agent
from textwrap import dedent
from config import MODELS, AGENT_CONFIG
import re
import json

class LogicSphereAgent:
    def __init__(self):
        self.agent = Agent(
            role=AGENT_CONFIG['logic_sphere']['role'],
            goal=AGENT_CONFIG['logic_sphere']['goal'],
            backstory=AGENT_CONFIG['logic_sphere']['backstory'],
            verbose=True,
            allow_delegation=False,
            llm=self._get_llm(),
        )

    def _get_llm(self):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model_name=MODELS['logic_agent'], temperature=0.1)

    def design_algorithm(self, problem_description: str, constraints: str = "") -> dict:
        prompt = dedent(f"""
        **Problem Description:**
        {problem_description}

        **Constraints:**
        {constraints if constraints else "None specified"}

        **Your Task:**
        Design the most efficient algorithm to solve this problem.
        - Analyze time and space complexity
        - Consider edge cases and error handling
        - Provide pseudocode with clear explanations
        - Suggest appropriate data structures
        - If applicable, recommend parallelization strategies

        Format your response as JSON with the following structure:
        {{
          "algorithm_name": "Descriptive name",
          "approach": "High-level description of the approach",
          "time_complexity": "O() notation",
          "space_complexity": "O() notation",
          "pseudocode": "Step-by-step pseudocode",
          "data_structures": ["list", "of", "recommended", "structures"],
          "edge_cases": ["list", "of", "edge", "cases", "to", "consider"]
        }}
        """)
        
        print(f"[LogicSphere] Designing algorithm for: {problem_description}")
        response = self.agent.execute_task(task=prompt)
        
        try:
            json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            else:
                return json.loads(response)
        except json.JSONDecodeError:
            print(f"[LogicSphere] Error: Could not parse JSON response. Raw output: {response}")
            return {"error": "Failed to parse algorithm design"}

    def design_architecture(self, requirements: str, scale: str = "small") -> dict:
        prompt = dedent(f"""
        **System Requirements:**
        {requirements}

        **Scale:** {scale}

        **Your Task:**
        Design a robust system architecture to meet these requirements.
        - Recommend appropriate technologies and frameworks
        - Design database schema if needed
        - Plan API structure and endpoints
        - Consider security, scalability, and maintainability
        - Suggest cloud services if applicable (AWS, Azure, GCP)

        Format your response as JSON with the following structure:
        {{
          "architecture_type": "e.g., Microservices, Monolith, Serverless",
          "technology_stack": {{
            "backend": ["list", "of", "technologies"],
            "frontend": ["list", "of", "technologies"],
            "database": "database technology",
            "caching": "caching solution if needed"
          }},
          "cloud_services": ["list", "of", "cloud", "services"],
          "key_components": ["list", "of", "system", "components"],
          "api_endpoints": ["list", "of", "API", "endpoints"],
          "security_considerations": ["list", "of", "security", "measures"]
        }}
        """)
        
        print(f"[LogicSphere] Designing architecture for: {requirements}")
        response = self.agent.execute_task(task=prompt)
        
        try:
            json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            else:
                return json.loads(response)
        except json.JSONDecodeError:
            print(f"[LogicSphere] Error: Could not parse JSON response. Raw output: {response}")
            return {"error": "Failed to parse architecture design"}

    def optimize_solution(self, existing_solution: str, problem: str) -> str:
        prompt = dedent(f"""
        **Problem:**
        {problem}

        **Existing Solution:**
        {existing_solution}

        **Your Task:**
        Analyze this solution and suggest optimizations.
        - Identify bottlenecks and inefficiencies
        - Suggest improvements for performance
        - Recommend better algorithms or data structures
        - Consider memory usage and computational complexity

        Provide detailed suggestions in markdown format.
        """)
        
        print(f"[LogicSphere] Optimizing solution for: {problem}")
        return self.agent.execute_task(task=prompt)
