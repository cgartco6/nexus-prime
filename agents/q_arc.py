from crewai import Agent
from textwrap import dedent
from config import MODELS, AGENT_CONFIG
import subprocess
import os
import re

class QArcAgent:
    def __init__(self):
        self.agent = Agent(
            role=AGENT_CONFIG['q_arc']['role'],
            goal=AGENT_CONFIG['q_arc']['goal'],
            backstory=AGENT_CONFIG['q_arc']['backstory'],
            verbose=True,
            allow_delegation=False,
            llm=self._get_llm(),
        )
        self.workspace_dir = "workspace"

    def _get_llm(self):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model_name=MODELS['qa_agent'], temperature=0.1)

    def _run_command(self, command, cwd=None):
        if cwd is None:
            cwd = self.workspace_dir
            
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                capture_output=True, 
                text=True, 
                cwd=cwd
            )
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def write_tests(self, code_file: str, functionality: str) -> dict:
        code_path = os.path.join(self.workspace_dir, code_file)
        if not os.path.exists(code_path):
            return {"error": f"File {code_file} not found in workspace"}
            
        with open(code_path, 'r') as f:
            code_content = f.read()
        
        prompt = dedent(f"""
        **Code to Test:**
        ```python
        {code_content}
        ```
        
        **Functionality to Test:**
        {functionality}
        
        **Your Task:**
        Write comprehensive unit tests for this code using pytest.
        - Cover all functions and edge cases
        - Test both success and failure scenarios
        - Include appropriate fixtures if needed
        - Ensure tests are isolated and independent
        
        Provide the complete test implementation in a single code block.
        The test file should be named test_{code_file}.
        """)
        
        print(f"[Q-Arc] Writing tests for {code_file}")
        response = self.agent.execute_task(task=prompt)
        
        code_blocks = self._extract_code_blocks(response)
        
        if code_blocks:
            test_filename = f"test_{code_file}"
            with open(os.path.join(self.workspace_dir, test_filename), 'w') as f:
                f.write(list(code_blocks.values())[0])
            print(f"[Q-Arc] Saved tests to {test_filename}")
            
            return {
                "response": response,
                "test_file": test_filename
            }
        else:
            return {"error": "No test code found in response"}

    def run_tests(self, test_file: str) -> dict:
        if not os.path.exists(os.path.join(self.workspace_dir, test_file)):
            return {"error": f"Test file {test_file} not found"}
            
        print(f"[Q-Arc] Running tests from {test_file}")
        
        self._run_command("pip install pytest")
        
        result = self._run_command(f"python -m pytest {test_file} -v")
        
        if result['success']:
            status = "PASS"
        else:
            status = "FAIL"
            
            failure_pattern = r'FAILED.*\.py::.*::.* - (.*)'
            failures = re.findall(failure_pattern, result['stdout'] + result['stderr'])
            
            if failures:
                result['failures'] = failures
        
        result['status'] = status
        return result

    def _extract_code_blocks(self, text: str) -> dict:
        code_blocks = {}
        pattern = r"```(?:\w+)?\s*\n([\s\S]*?)```"
        matches = re.findall(pattern, text)
        
        for i, match in enumerate(matches):
            code_blocks[f"code_block_{i}"] = match.strip()
            
        return code_blocks

    def perform_code_review(self, code_file: str) -> dict:
        code_path = os.path.join(self.workspace_dir, code_file)
        if not os.path.exists(code_path):
            return {"error": f"File {code_file} not found in workspace"}
            
        with open(code_path, 'r') as f:
            code_content = f.read()
        
        prompt = dedent(f"""
        **Code to Review:**
        ```python
        {code_content}
        ```
        
        **Your Task:**
        Perform a comprehensive code review focusing on:
        - Code quality and readability
        - Potential bugs or edge cases
        - Security vulnerabilities
        - Performance optimizations
        - Adherence to best practices
        - Documentation completeness
        
        Provide a detailed review with specific suggestions for improvement.
        """)
        
        print(f"[Q-Arc] Reviewing code in {code_file}")
        response = self.agent.execute_task(task=prompt)
        
        return {
            "response": response,
            "code_file": code_file
        }
