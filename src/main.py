import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from src.agents.planner import PlannerAgent
from src.utils.logger import setup_logger
from fastapi.responses import HTMLResponse
from datetime import datetime
from pathlib import Path
from fastapi.responses import HTMLResponse, PlainTextResponse

logger = setup_logger("API")
app = FastAPI(title="AI Agent Pipeline API")


class QueryRequest(BaseModel):
    query: str


# --- ADD THIS NEW ROUTE ---
@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the landing dashboard."""
    html_path = Path("src/templates/index.html")
    if html_path.exists():
        return html_path.read_text(encoding="utf-8")
    return "<h1>Dashboard Loading...</h1>"


# --------------------------
@app.get("/logs", response_class=PlainTextResponse)
async def view_logs():
    """Endpoint to view the live production logs, bypassing timezone issues."""
    log_dir = Path("logs")

    # 1. Check if the directory exists
    if not log_dir.exists():
        return "Logs directory does not exist yet."

    # 2. Find all .log files in the directory
    log_files = list(log_dir.glob("*.log"))

    # 3. Check if any log files were found
    if not log_files:
        return (
            "No logs found yet. Try clicking 'Run Demo' first to generate some traffic!"
        )

    # 4. Grab the most recently modified log file (completely ignores the date name)
    latest_log = max(log_files, key=os.path.getctime)

    try:
        return latest_log.read_text(encoding="utf-8")
    except Exception as e:
        return f"Error reading log file: {str(e)}"


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
