from crewai import Agent
from textwrap import dedent
from config import MODELS, AGENT_CONFIG
import os
import re

class CodeWeaverAgent:
    def __init__(self):
        self.agent = Agent(
            role=AGENT_CONFIG['code_weaver']['role'],
            goal=AGENT_CONFIG['code_weaver']['goal'],
            backstory=AGENT_CONFIG['code_weaver']['backstory'],
            verbose=True,
            allow_delegation=False,
            llm=self._get_llm(),
        )
        self.workspace_dir = "workspace"

    def _get_llm(self):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model_name=MODELS['code_agent'], temperature=0.1)

    def _ensure_workspace(self):
        if not os.path.exists(self.workspace_dir):
            os.makedirs(self.workspace_dir)

    def _extract_code_blocks(self, text: str) -> dict:
        code_blocks = {}
        pattern = r"```(?:\w+)?\s*\n([\s\S]*?)```"
        matches = re.findall(pattern, text)
        
        for i, match in enumerate(matches):
            filename = f"generated_code_{i}.py"
            if "def " in match and "class " in match:
                filename = "app.py"
            elif "FROM" in match and "RUN" in match:
                filename = "Dockerfile"
            elif "pytest" in match:
                filename = "test_app.py"
            elif "requirements" in match.lower():
                filename = "requirements.txt"
                
            code_blocks[filename] = match.strip()
            
        return code_blocks

    def _save_code(self, code_blocks: dict):
        for filename, code in code_blocks.items():
            filepath = os.path.join(self.workspace_dir, filename)
            with open(filepath, 'w') as f:
                f.write(code)
            print(f"[CodeWeaver] Saved code to {filepath}")

    def write_code(self, task_description: str, context: str = "") -> dict:
        self._ensure_workspace()
        
        prompt = dedent(f"""
        **Task Description:**
        {task_description}

        **Project Context:**
        {context}

        **Your Instructions:**
        Write clean, production-ready code to complete this task.
        - Follow best practices for the relevant language/framework
        - Include appropriate error handling
        - Add comments where helpful
        - Ensure code is efficient and secure
        - Output your code in markdown code blocks with appropriate language tags

        If this task requires multiple files, generate them all in a single response with separate code blocks.
        """)
        
        print(f"[CodeWeaver] Executing task: {task_description}")
        response = self.agent.execute_task(task=prompt)
        
        code_blocks = self._extract_code_blocks(response)
        
        if code_blocks:
            self._save_code(code_blocks)
            
        return {
            "response": response,
            "files": list(code_blocks.keys())
        }
