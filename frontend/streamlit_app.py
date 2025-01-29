import streamlit as st
import requests
from typing import Dict

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.title("Job Search Chatbot")

# Sidebar for settings
with st.sidebar:
    st.header("Settings")
    pagesize = st.slider("Results per page", 5, 50, 10)
    api_preference = st.selectbox(
        "Search Preference",
        ["API First", "Web First"]
    )

# Chat interface
user_input = st.chat_input("Enter your job search query...")

if user_input:
    # Add user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    
    # Call FastAPI backend
    response = requests.post(
        "http://localhost:8000/search",
        json={
            "query": user_input,
            "chat_history": st.session_state.chat_history,
            "pagesize": pagesize
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        st.session_state.chat_history = data['chat_history']
        response_content = data['response']
        
        if response_content['status'] == 'success':
            if isinstance(response_content['data'], list):
                st.success(f"Found {len(response_content['data'])} jobs:")
                for job in response_content['data']:
                    if isinstance(job, dict) and 'title' in job and 'company' in job:
                        st.markdown(f"""
                        <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px;">
                            <h4 style="margin: 0;">{job['title']}</h4>
                            <p style="margin: 0;"><strong>Company:</strong> {job['company']}</p>
                            <p style="margin: 0;"><strong>Location:</strong> {job['location']}</p>
                            <p style="margin: 0;"><strong>Posted Date:</strong> {job['posted_date']}</p>
                            <p style="margin: 0;"><a href="{job['url'] or '#'}" target="_blank">Job Link</a></p>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.write(job)
            else:
                st.write(response_content['data'])
        else:
            st.error(response_content['message'])
    else:
        st.error("Error processing request")

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        content = message["content"]
        if isinstance(content, Dict):
            if content['status'] == 'success':
                if isinstance(content['data'], list):
                    st.success(f"Found {len(content['data'])} jobs:")
                    for job in content['data']:
                        if isinstance(job, dict) and 'title' in job and 'company' in job:
                            st.markdown(f"""
                            <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px; border-radius: 5px;">
                                <h4 style="margin: 0;">{job['title']}</h4>
                                <p style="margin: 0;"><strong>Company:</strong> {job['company']}</p>
                                <p style="margin: 0;"><strong>Location:</strong> {job['location']}</p>
                                <p style="margin: 0;"><strong>Posted Date:</strong> {job['posted_date']}</p>
                                <p style="margin: 0;"><a href="{job['url'] or '#'}" target="_blank">Job Link</a></p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.write(job)
                else:
                    st.write(content['data'])
            else:
                st.error(content['message'])
        else:
            st.write(content)