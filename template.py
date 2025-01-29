import os

def create_structure(base_path=""):
    structure = [
        ".env",
        ".gitignore",
        "backend/Dockerfile",
        "backend/requirements.txt",
        "backend/tests/test_api.py",
        "backend/app/__init__.py",
        "backend/app/main.py",
        "backend/app/agents/job_search_agent.py",
        "backend/app/config/settings.py",
        "backend/app/schemas/models.py",
        "frontend/Dockerfile",
        "frontend/streamlit_app.py",
        "frontend/requirements.txt",
    ]
    
    for path in structure:
        full_path = os.path.join(base_path, path)
        dir_name = os.path.dirname(full_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(full_path, "w") as f:
            pass  # Create an empty file

if __name__ == "__main__":
    create_structure()