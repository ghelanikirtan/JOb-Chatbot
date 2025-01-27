import streamlit as st
import requests
from schemas.schema import AgentState, Conversation

BASE_API_URL = "http://localhost:8000/api"

def init_session():
    if 'session_id' not in st.session_state:
        response = requests.post(f"{BASE_API_URL}/session")
        st.session_state.session_id = response.json()['session_id']

def get_response(query: str):
    state = AgentState(
        query=query,
        conversation=Conversation(session_id=st.session_state.session_id)
    )
    
    response = requests.post(
        f"{BASE_API_URL}/search",
        json=state.dict()
    )
    
    return response.json()

def main():
    st.title("AI Job Search Assistant")
    init_session()
    
    query = st.text_input("What kind of job are you looking for?")
    if query:
        result = get_response(query)
        
        if result['status'] == 'success':
            for job in result['data']:
                st.subheader(job['title'])
                st.write(f"**Company:** {job['company']}")
                st.write(f"**Location:** {job['location']}")
                st.write(job['description'][:300] + "...")
                st.markdown(f"[Apply Here]({job['url']})")
        else:
            st.error("Failed to find relevant jobs. Please try again.")

if __name__ == "__main__":
    main()  