from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agents.planner import PlannerAgent
from src.utils.logger import setup_logger

logger = setup_logger("API")
app = FastAPI(title="AI Agent Pipeline API")


class QueryRequest(BaseModel):
    query: str


@app.post("/api/v1/plan")
async def create_plan(request: QueryRequest):
    """Endpoint to generate an AI plan based on a user query."""
    try:
        planner = PlannerAgent()
        logger.info(f"Received API request for query: {request.query}")
        result = planner.process(request.query)
        return {"status": "success", "data": result}
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Load balancers use this to check if the server is alive."""
    return {"status": "healthy"}
