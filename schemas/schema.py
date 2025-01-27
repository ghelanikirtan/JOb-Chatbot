from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Dict, Any

class JobData(BaseModel):
    title: str = Field(default="")
    job_type: str = Field(default="")
    description: str = Field(default="")
    posted_date: str = Field(default="")
    company: str = Field(default="")
    location: str = Field(default="")
    salary: Optional[str] = None
    url: Optional[str] = None
    score: Optional[float] = Field(None, ge=0, le=1)

class Conversation(BaseModel):
    session_id: str
    history: List[Dict[str, Any]] = []
    context: Dict[str, Any] = {}

class AgentState(BaseModel):
    query: str
    data: Optional[List[JobData]] = None
    validated: bool = False
    current_tool: Optional[Literal["api_fetcher", "retriever", "web_search"]] = None
    retries: int = 0
    response: Optional[dict] = None
    conversation: Optional[Conversation] = None