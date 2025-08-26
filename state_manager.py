import json
import os
from datetime import datetime
from typing import Dict, Any, List

class ProjectStateManager:
    def __init__(self, storage_dir="projects"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
    
    def save_project(self, project_id: str, state: Dict[str, Any]) -> bool:
        try:
            file_path = os.path.join(self.storage_dir, f"{project_id}.json")
            with open(file_path, 'w') as f:
                json.dump({
                    "project_id": project_id,
                    "last_updated": datetime.now().isoformat(),
                    "state": state
                }, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving project {project_id}: {e}")
            return False
    
    def load_project(self, project_id: str) -> Dict[str, Any]:
        try:
            file_path = os.path.join(self.storage_dir, f"{project_id}.json")
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            print(f"Error loading project {project_id}: {e}")
            return None
    
    def list_projects(self) -> List[Dict[str, Any]]:
        projects = []
        for file_name in os.listdir(self.storage_dir):
            if file_name.endswith('.json'):
                project_id = file_name[:-5]
                project_data = self.load_project(project_id)
                if project_data:
                    projects.append({
                        "id": project_id,
                        "last_updated": project_data.get("last_updated"),
                        "name": project_data.get("state", {}).get("active_plan", {}).get("project_name", "Unknown")
                    })
        return projects
    
    def delete_project(self, project_id: str) -> bool:
        try:
            file_path = os.path.join(self.storage_dir, f"{project_id}.json")
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting project {project_id}: {e}")
            return False
