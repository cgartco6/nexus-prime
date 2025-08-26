import json
import re
import uuid
from typing import Dict, List
from agents.project_manager import ProjectManagerAgent
from agents.code_weaver import CodeWeaverAgent
from agents.logic_sphere import LogicSphereAgent
from agents.q_arc import QArcAgent
from agents.pixel_genius import PixelGeniusAgent
from agents.script_sensei import ScriptSenseiAgent
from agents.aura import AuraAgent
from agents.data_scientist import DataScientistAgent
from agents.blockchain_developer import BlockchainDeveloperAgent
from agents.devops_engineer import DevOpsEngineerAgent
from state_manager import ProjectStateManager

class NexusCore:
    def __init__(self):
        self.project_manager = ProjectManagerAgent()
        self.code_weaver = CodeWeaverAgent()
        self.logic_sphere = LogicSphereAgent()
        self.q_arc = QArcAgent()
        self.pixel_genius = PixelGeniusAgent()
        self.script_sensei = ScriptSenseiAgent()
        self.aura = AuraAgent()
        self.data_scientist = DataScientistAgent()
        self.blockchain_developer = BlockchainDeveloperAgent()
        self.devops_engineer = DevOpsEngineerAgent()
        self.state_manager = ProjectStateManager()
        self.active_project_id = None
        self.active_plan = None
        self.workspace_state = {}
        self.task_status = {}

    def create_project(self, user_command: str) -> str:
        project_id = str(uuid.uuid4())[:8]
        self.active_project_id = project_id
        
        print(f"[Nexus Prime] Creating new project: {project_id}")
        print(f"[Nexus Prime] Received command: {user_command}")
        print("[Nexus Prime] Formulating plan...")

        plan_json = self.project_manager.create_plan(user_command)

        try:
            self.active_plan = self._parse_plan(plan_json)
            print(f"[Nexus Prime] Plan '{self.active_plan['project_name']}' created successfully!")
            
            self._initialize_task_status()
            
            self._save_project_state()
            
            return project_id
            
        except (json.JSONDecodeError, KeyError) as e:
            print(f"[Nexus Prime] Error: Failed to parse plan. {e}")
            print(f"Raw output: {plan_json}")
            return None

    def load_project(self, project_id: str) -> bool:
        project_data = self.state_manager.load_project(project_id)
        if project_data:
            self.active_project_id = project_id
            self.active_plan = project_data['state']['active_plan']
            self.workspace_state = project_data['state']['workspace_state']
            self.task_status = project_data['state']['task_status']
            print(f"[Nexus Prime] Loaded project: {self.active_plan['project_name']}")
            return True
        return False

    def _initialize_task_status(self):
        self.task_status = {}
        for phase in self.active_plan['phases']:
            for task in phase['tasks']:
                self.task_status[task['id']] = {
                    'status': 'pending',
                    'dependencies': task.get('dependencies', []),
                    'dependencies_met': False
                }

    def _check_dependencies(self, task_id: int) -> bool:
        task_info = self.task_status[task_id]
        if not task_info['dependencies']:
            return True
            
        for dep_id in task_info['dependencies']:
            if self.task_status[dep_id]['status'] != 'completed':
                return False
        return True

    def _get_next_task(self) -> Dict:
        all_tasks = []
        for phase in self.active_plan['phases']:
            all_tasks.extend(phase['tasks'])
            
        for task in all_tasks:
            task_id = task['id']
            if (self.task_status[task_id]['status'] == 'pending' and 
                self._check_dependencies(task_id)):
                return task
        return None

    def execute_next_task(self) -> Dict:
        next_task = self._get_next_task()
        if not next_task:
            print("[Nexus Prime] No tasks available for execution")
            return None
            
        task_id = next_task['id']
        agent_name = next_task['agent']
        
        print(f"[Nexus Prime] Executing Task {task_id} with {agent_name}")
        self.task_status[task_id]['status'] = 'in_progress'
        self._save_project_state()
        
        try:
            result = self._execute_task_with_feedback(next_task)
            
            self.task_status[task_id]['status'] = 'completed'
            self.workspace_state[f"task_{task_id}"] = result
            self._save_project_state()
            
            print(f"[Nexus Prime] Task {task_id} completed successfully")
            return result
            
        except Exception as e:
            print(f"[Nexus Prime] Task {task_id} failed: {e}")
            self.task_status[task_id]['status'] = 'failed'
            self.task_status[task_id]['error'] = str(e)
            self._save_project_state()
            return {"error": str(e)}

    def _execute_task(self, task: Dict) -> Dict:
        agent_name = task['agent']
        task_description = task['description']
        
        if agent_name == 'CodeWeaver':
            return self.code_weaver.write_code(
                task_description=task_description,
                context=self.active_plan['objective']
            )
                
        elif agent_name == 'LogicSphere':
            if any(keyword in task_description.lower() for keyword in ['algorithm', 'sort', 'search', 'optimize']):
                return self.logic_sphere.design_algorithm(
                    problem_description=task_description,
                    constraints=self.active_plan['objective']
                )
            elif any(keyword in task_description.lower() for keyword in ['architecture', 'system', 'design', 'cloud']):
                return self.logic_sphere.design_architecture(
                    requirements=task_description,
                    scale="medium"
                )
            else:
                return {"error": f"Unknown LogicSphere task type: {task_description}"}
                
        elif agent_name == 'Q-Arc':
            if any(keyword in task_description.lower() for keyword in ['test', 'validate', 'quality']):
                code_files = [f for f in self.workspace_state.keys() if 'files' in self.workspace_state[f]]
                if code_files:
                    latest_task = code_files[-1]
                    code_file = self.workspace_state[latest_task]['files'][0]
                    result = self.q_arc.write_tests(code_file, task_description)
                    
                    if 'test_file' in result:
                        test_result = self.q_arc.run_tests(result['test_file'])
                        result['test_results'] = test_result
                    return result
                else:
                    return {"error": "No code files found to test"}
            elif any(keyword in task_description.lower() for keyword in ['review', 'inspect', 'audit']):
                code_files = [f for f in self.workspace_state.keys() if 'files' in self.workspace_state[f]]
                if code_files:
                    latest_task = code_files[-1]
                    code_file = self.workspace_state[latest_task]['files'][0]
                    return self.q_arc.perform_code_review(code_file)
                else:
                    return {"error": "No code files found to review"}
            else:
                return {"error": f"Unknown Q-Arc task type: {task_description}"}
                
        elif agent_name == 'PixelGenius':
            if any(keyword in task_description.lower() for keyword in ['ui', 'design', 'interface', 'layout']):
                result = self.pixel_genius.design_ui(
                    requirements=task_description,
                    platform="web"
                )
                
                if 'error' not in result:
                    css_code = self.pixel_genius.generate_css(result)
                    result['css_code'] = css_code
                return result
            else:
                return {"error": f"Unknown PixelGenius task type: {task_description}"}
                
        elif agent_name == 'ScriptSensei':
            if any(keyword in task_description.lower() for keyword in ['content', 'copy', 'text', 'write']):
                return self.script_sensei.create_content(
                    topic=task_description,
                    format="web content",
                    tone="professional"
                )
            elif any(keyword in task_description.lower() for keyword in ['story', 'narrative', 'plot']):
                return self.script_sensei.develop_story(
                    premise=task_description,
                    genre="fantasy",
                    length="short"
                )
            elif any(keyword in task_description.lower() for keyword in ['dialogue', 'script', 'conversation']):
                return self.script_sensei.generate_dialogue(
                    characters=["Character A", "Character B"],
                    context=task_description
                )
            else:
                return {"error": f"Unknown ScriptSensei task type: {task_description}"}
                
        elif agent_name == 'Aura':
            if any(keyword in task_description.lower() for keyword in ['sound', 'audio', 'sfx']):
                return self.aura.design_soundscape(
                    context=task_description,
                    mood="appropriate"
                )
            elif any(keyword in task_description.lower() for keyword in ['music', 'score', 'composition']):
                return self.aura.compose_music_brief(
                    requirements=task_description
                )
            else:
                return {"error": f"Unknown Aura task type: {task_description}"}
                
        elif agent_name == 'DataScientist':
            if any(keyword in task_description.lower() for keyword in ['data', 'analyze', 'analysis']):
                return self.data_scientist.analyze_data(
                    data_description=task_description,
                    objectives=self.active_plan['objective']
                )
            elif any(keyword in task_description.lower() for keyword in ['machine learning', 'ml', 'model']):
                return self.data_scientist.design_ml_model(
                    problem=task_description,
                    data_type="structured"  # Default for demo
                )
            else:
                return {"error": f"Unknown DataScientist task type: {task_description}"}
                
        elif agent_name == 'BlockchainDeveloper':
            if any(keyword in task_description.lower() for keyword in ['blockchain', 'smart contract', 'crypto']):
                return self.blockchain_developer.design_smart_contract(
                    requirements=task_description,
                    platform="Ethereum"  # Default for demo
                )
            else:
                return {"error": f"Unknown BlockchainDeveloper task type: {task_description}"}
                
        elif agent_name == 'DevOpsEngineer':
            if any(keyword in task_description.lower() for keyword in ['infrastructure', 'deploy', 'devops']):
                return self.devops_engineer.design_infrastructure(
                    requirements=task_description,
                    cloud_provider="AWS"  # Default for demo
                )
            else:
                return {"error": f"Unknown DevOpsEngineer task type: {task_description}"}
                
        else:
            return {"error": f"Unknown agent: {agent_name}"}

    def _execute_task_with_feedback(self, task: Dict) -> Dict:
        max_attempts = 3
        attempt = 0
        result = None
        
        while attempt < max_attempts:
            attempt += 1
            print(f"[Nexus Prime] Attempt {attempt} for task {task['id']}")
            
            result = self._execute_task(task)
            
            if self._needs_improvement(result, task):
                print(f"[Nexus Prime] Task {task['id']} needs improvement, analyzing...")
                feedback = self._analyze_result(result, task)
                print(f"[Nexus Prime] Feedback: {feedback}")
                
                enhanced_task = task.copy()
                enhanced_task['description'] = f"{task['description']}. Previous attempt issues: {feedback}. Please fix these issues."
                
                result = self._execute_task(enhanced_task)
            else:
                break
                
        return result
    
    def _needs_improvement(self, result: Dict, task: Dict) -> bool:
        if 'error' in result:
            return True
            
        if 'test_results' in result and result['test_results'].get('status') == 'FAIL':
            return True
            
        if 'response' in result and any(keyword in result['response'].lower() 
                                      for keyword in ['issue', 'problem', 'error', 'improve', 'better']):
            return True
            
        return False
    
    def _analyze_result(self, result: Dict, task: Dict) -> str:
        agent_name = task['agent']
        
        if agent_name == 'CodeWeaver' and 'test_results' in result:
            failures = result['test_results'].get('failures', [])
            if failures:
                return f"Tests failed: {', '.join(failures)}"
                
        if 'error' in result:
            return f"Error occurred: {result['error']}"
            
        if 'response' in result:
            prompt = f"""
            Analyze this task result and provide specific feedback for improvement:
            
            Task: {task['description']}
            Result: {result['response']}
            
            Provide concise feedback on what needs to be improved.
            """
            return self.project_manager.agent.execute_task(task=prompt)
            
        return "Unknown issue needs addressing"

    def _save_project_state(self):
        if self.active_project_id:
            state = {
                "active_plan": self.active_plan,
                "workspace_state": self.workspace_state,
                "task_status": self.task_status
            }
            self.state_manager.save_project(self.active_project_id, state)

    def get_project_status(self) -> Dict:
        if not self.active_plan:
            return {"error": "No active project"}
            
        completed = 0
        total = 0
        for task_id, status in self.task_status.items():
            total += 1
            if status['status'] == 'completed':
                completed += 1
                
        return {
            "project_name": self.active_plan['project_name'],
            "progress": f"{completed}/{total} tasks completed",
            "percentage": (completed / total) * 100 if total > 0 else 0
        }

    def _parse_plan(self, plan_text: str) -> dict:
        json_match = re.search(r'```json\n(.*?)\n```', plan_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(1))
        else:
            return json.loads(plan_text)

    def _review_plan(self):
        print("\n--- PROJECT PLAN REVIEW ---")
        print(f"Objective: {self.active_plan['objective']}")
        for phase in self.active_plan['phases']:
            print(f"\nPhase: {phase['name']}")
            for task in phase['tasks']:
                print(f"  [Task {task['id']}] ({task['agent']}): {task['description']}")

if __name__ == "__main__":
    nexus = NexusCore()
    test_command = "Create a simple weather dashboard web app with a clean UI that displays current weather and forecast. Include tests and a brief documentation."
    nexus.execute_command(test_command)
