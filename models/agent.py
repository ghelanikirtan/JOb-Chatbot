from langgraph.graph import StateGraph, END
from typing import Optional
from schemas.schema import AgentState, Conversation
from utils.config import config
from services.api_client import CareerJetAPI

class JobAgent:
    def __init__(self):
        self.api = CareerJetAPI()
        self.workflow = StateGraph(AgentState)
        self.build_workflow()
        self.conversations = {}

    def get_conversation(self, session_id: str) -> Conversation:
        if session_id not in self.conversations:
            self.conversations[session_id] = Conversation(session_id=session_id)
        return self.conversations[session_id]

    def api_fetcher(self, state: AgentState) -> AgentState:
        conversation = self.get_conversation(state.conversation.session_id)
        jobs = self.api.search_jobs(state.query, conversation.context.get('location', ''))
        state.data = [job for job in jobs if job.score >= config.validation['min_score']]
        return state

    def build_workflow(self):
        # Add nodes and edges similar to original structure
        # Include error handling and circuit breakers
        pass