from crewai import Agent
from textwrap import dedent
from config import MODELS, AGENT_CONFIG
import json
import re

class DataScientistAgent:
    def __init__(self):
        self.agent = Agent(
            role="Data Scientist & ML Engineer",
            goal="Analyze data, build machine learning models, and extract insights.",
            backstory=dedent("""
                You are an expert data scientist with advanced degrees in statistics and computer science.
                You've built predictive models for Fortune 500 companies and published research in top journals.
                You're proficient with pandas, scikit-learn, TensorFlow, and PyTorch.
            """),
            verbose=True,
            allow_delegation=False,
            llm=self._get_llm(),
        )

    def _get_llm(self):
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model_name=MODELS['architect'], temperature=0.1)

    def analyze_data(self, data_description: str, objectives: str) -> dict:
        prompt = dedent(f"""
        **Data Description:**
        {data_description}
        
        **Analysis Objectives:**
        {objectives}
        
        **Your Task:**
        Design a comprehensive data analysis plan including:
        - Data cleaning and preprocessing steps
        - Exploratory data analysis techniques
        - Statistical methods to apply
        - Visualization recommendations
        - Potential machine learning approaches
        
        Format your response as JSON with the following structure:
        {{
          "analysis_plan": "Overall description of the analysis approach",
          "data_cleaning": ["list", "of", "data", "cleaning", "steps"],
          "exploratory_analysis": ["list", "of", "EDA", "techniques"],
          "statistical_methods": ["list", "of", "statistical", "methods"],
          "visualizations": ["list", "of", "recommended", "visualizations"],
          "ml_approaches": ["list", "of", "machine", "learning", "approaches"]
        }}
        """)
        
        print(f"[DataScientist] Creating analysis plan for: {objectives}")
        response = self.agent.execute_task(task=prompt)
        
        try:
            json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            else:
                return json.loads(response)
        except json.JSONDecodeError:
            print(f"[DataScientist] Error: Could not parse JSON response. Raw output: {response}")
            return {"error": "Failed to parse analysis plan"}

    def design_ml_model(self, problem: str, data_type: str) -> dict:
        prompt = dedent(f"""
        **Problem:**
        {problem}
        
        **Data Type:**
        {data_type}
        
        **Your Task:**
        Design a machine learning solution including:
        - Model type and architecture
        - Feature engineering approach
        - Training methodology
        - Evaluation metrics
        - Potential challenges and solutions
        
        Format your response as JSON with the following structure:
        {{
          "model_type": "Type of ML model (e.g., classification, regression)",
          "architecture": "Model architecture details",
          "features": ["list", "of", "potential", "features"],
          "training_approach": "How to train the model",
          "evaluation_metrics": ["list", "of", "evaluation", "metrics"],
          "challenges": ["list", "of", "potential", "challenges"]
        }}
        """)
        
        print(f"[DataScientist] Designing ML model for: {problem}")
        response = self.agent.execute_task(task=prompt)
        
        try:
            json_match = re.search(r'```json\n(.*?)\n```', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            else:
                return json.loads(response)
        except json.JSONDecodeError:
            print(f"[DataScientist] Error: Could not parse JSON response. Raw output: {response}")
            return {"error": "Failed to parse ML design"}
