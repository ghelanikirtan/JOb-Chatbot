import os

def create_project_structure():
    structure = {
        "config": ["config.yaml", "__init__.py"],
        "schemas": ["__init__.py", "schema.py"],
        "services": ["__init__.py", "api_client.py", "rag_supervisor.py"],
        "models": ["__init__.py", "agent.py"],
        "utils": ["__init__.py", "logger.py", "config.py"],
        "api": {
            "": ["__init__.py", "main.py"],
            "routes": ["__init__.py", "jobs.py"]
        },
        "web": ["__init__.py", "streamlit_app.py"],
        "": [".env", "requirements.txt", "Dockerfile"]

    def create_files_and_dirs(base_path, items):
        for name, content in items.items():
            if name:
                path = os.path.join(base_path, name)
                os.makedirs(path, exist_ok=True)
            else:
                path = base_path

            if isinstance(content, list):
                for file_name in content:
                    file_path = os.path.join(path, file_name)
                    open(file_path, 'w').close()
            elif isinstance(content, dict):
                create_files_and_dirs(path, content)

    base_dir = os.getcwd()
    create_files_and_dirs(base_dir, structure)

if __name__ == "__main__":
    create_project_structure()
    print("Project structure created successfully.")
