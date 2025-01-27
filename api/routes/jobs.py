from fastapi import APIRouter, HTTPException
from schemas.schema import AgentState, Conversation
from models.agent import JobAgent
from utils.logger import logger

router = APIRouter()
agent = JobAgent()

@router.post("/search")
async def job_search(state: AgentState):
    try:
        result = agent.workflow.run(state)
        return result
    except Exception as e:
        logger.error(f"API Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/conversation/{session_id}")
async def update_conversation(session_id: str, conversation: Conversation):
    agent.conversations[session_id] = conversation
    return {"status": "success"}