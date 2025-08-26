import os
import requests
from typing import Dict, Any

class ExternalAPIManager:
    def __init__(self):
        self.stability_api_key = os.getenv("STABILITY_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
    
    def generate_image(self, prompt: str, style: str = "digital-art") -> Dict[str, Any]:
        if not self.stability_api_key:
            return {"error": "Stability API key not configured"}
        
        try:
            response = requests.post(
                "https://api.stability.ai/v1/generation/stable-diffusion-v1-6/text-to-image",
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": f"Bearer {self.stability_api_key}"
                },
                json={
                    "text_prompts": [{"text": prompt}],
                    "cfg_scale": 7,
                    "height": 512,
                    "width": 512,
                    "samples": 1,
                    "steps": 30,
                    "style_preset": style
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                image_path = f"workspace/generated_image_{hash(prompt)}.png"
                with open(image_path, 'wb') as f:
                    f.write(data['artifacts'][0]['base64'])
                return {"success": True, "image_path": image_path}
            else:
                return {"error": f"API error: {response.status_code}", "details": response.text}
                
        except Exception as e:
            return {"error": f"Failed to generate image: {str(e)}"}
    
    def deploy_to_netlify(self, site_name: str) -> Dict[str, Any]:
        return {
            "success": True,
            "url": f"https://{site_name}.netlify.app",
            "message": "Deployment initiated (simulated)"
        }
    
    def execute_code(self, code: str, language: str = "python") -> Dict[str, Any]:
        try:
            response = requests.post(
                "https://emkc.org/api/v2/piston/execute",
                json={
                    "language": language,
                    "version": "3.10.0",
                    "files": [{"content": code}]
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "output": result.get('run', {}).get('output', ''),
                    "error": result.get('run', {}).get('stderr', '')
                }
            else:
                return {"error": f"API error: {response.status_code}"}
                
        except Exception as e:
            return {"error": f"Failed to execute code: {str(e)}"}
