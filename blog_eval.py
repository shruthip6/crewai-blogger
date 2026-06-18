from crewai import LLM, Agent, Process, Task, Crew
from crewai.project import CrewBase, agent, task, crew  
from dotenv import load_dotenv
import os

from fastapi import FastAPI, HTTPException


    
load_dotenv()
@CrewBase
class AiTrendCrew:
    """AiTrendCrew system orchestration using YAML files"""

    # Path paths relative to where this class module sits
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm
        )

    @agent
    def writer(self) -> Agent:
        return Agent(
            config=self.agents_config['writer'],
            verbose=True,
            allow_delegation=False,
            llm=gemini_llm
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task']
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,       # Automatically collected from @agent decorators
            tasks=self.tasks,         # Automatically collected from @task decorators
            process=Process.sequential,  
            verbose=True
        )  
        

    # print("Starting AI Trend Analysis Crew...")
    
    # # Instantiate the decorated class and trigger the crew method
    # ai_crew_instance = AiTrendCrew().crew()
    # result = ai_crew_instance.kickoff()
    
    # print("\n" + "="*50)
    # print("FINAL RESULT:")
    # print("="*50)
    # print(result)        
gemini_llm = LLM(
model="gemini/gemini-2.5-flash-lite",
api_key=os.getenv("google_api_key"),
temperature=0.7
)
app = FastAPI(title="CrewAI Azure Service")

@app.get("/")
def health_check():
    return {"status": "healthy", "service": "CrewAI Runner"}

@app.post("/run-crew")
def run_crew():
    try:
        result = AiTrendCrew().crew().kickoff()
        return {"status": "success", "result": str(result)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

  