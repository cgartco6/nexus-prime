from crewai import Agent
from textwrap import dedent
from config import MODELS, AGENT_CONFIG
import json
import re

class BlockchainDeveloperAgent:
    def __init__(self):
        self.agent = Agent(
            role="Blockchain Developer & Smart Contract Expert",
            goal="Develop secure smart contracts and blockchain solutions.",
            backstory=dedent("""
                You are an experienced blockchain developer with expertise in multiple blockchain platforms.
                You've developed secure smart contracts for DeFi projects, NFTs, and enterprise blockchain solutions.
                You're proficient with Solidity, Rust, and blockchain security best practices.
            """),
            verbose=True,
            allow_delegation=False,
            llm=self._get_llm(),
        )

    def _get_llm(self):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model_name=MODELS['architect'], temperature=0.1)

    def design_smart_contract(self, requirements: str, platform: str = "Ethereum") -> dict:
        prompt = dedent(f"""
        **Requirements:**
        {requirements}
        
        **Platform:** {platform}
        
        **Your Task:**
        Design a secure smart contract including:
        - Contract architecture and components
        - Functions and their purposes
        - Security considerations and potential vulnerabilities
        - Gas optimization strategies
        - Testing approach
        
        Format your response as JSON with the following structure:
        {{
          "contract_name": "Descriptive name",
          "platform": "Blockchain platform",
          "functions": [
            {{
              "name": "Function name",
              "purpose": "What it does",
              "parameters": ["list", "of", "parameters"],
              "returns": "What it returns"
            }}
          ],
          "security_considerations": ["list", "of", "security", "measures"],
          "potential_vulnerabilities": ["list", "of", "potential", "issues"],
          "testing_approach": "How to test the contract"
        }}
        """)
        
        print(f"[BlockchainDeveloper] Designing smart contract for: {requirements}")
        response = self.agent.execute_task(task=prompt)
        
        try:
            json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            else:
                return json.loads(response)
        except json.JSONDecodeError:
            print(f"[BlockchainDeveloper] Error: Could not parse JSON response. Raw output: {response}")
            return {"error": "Failed to parse smart contract design"}
