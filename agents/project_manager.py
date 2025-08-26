from crewai import Agent
from textwrap import dedent
from config import MODELS, AGENT_CONFIG
import os

class ProjectManagerAgent:
    def __init__(self):
        self.agent = Agent(
            role=AGENT_CONFIG['project_synapse']['role'],
            goal=AGENT_CONFIG['project_synapse']['goal'],
            backstory=AGENT_CONFIG['project_synapse']['backstory'],
            verbose=True,
            allow_delegation=False,
            llm=self._get_llm(),
        )

    def _get_llm(self):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model_name=MODELS['planner'], temperature=0.1)

    def create_plan(self, objective: str) -> str:
        prompt = dedent(f"""
        **Objective:** {objective}

        **Your Task:**
        Analyze the objective and create a detailed, step-by-step development plan.
        The plan must be structured as a JSON object with the following schema:

        {{
          "project_name": "Generated name for the project",
          "objective": "Reiteration of the core objective",
          "phases": [
            {{
              "name": "Phase name e.g., Design, Development, Testing",
              "description": "Goal of this phase",
              "tasks": [
                {{
                  "id": 1,
                  "description": "A clear, actionable task description",
                  "agent": "Which specialist agent is required? [CodeWeaver, LogicSphere, Q-Arc, PixelGenius, ScriptSensei, Aura, DataScientist, BlockchainDeveloper, DevOpsEngineer]",
                  "dependencies": [] # List of task IDs this task depends on
                }}
              ]
            }}
          ]
        }}

        Be extremely specific and technical in the task descriptions.
        Consider dependencies between tasks.
        """)
        return self.agent.execute_task(task=prompt)
