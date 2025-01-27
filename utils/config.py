import os
import yaml
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    def __init__(self):
        self.config_path = Path(__file__).parent.parent / "config" / "config.yaml"
        self.load_config()
        
    def load_config(self):
        with open(self.config_path, 'r') as f:
            self.data = yaml.safe_load(f)
            
    @property
    def model_settings(self):
        return self.data.get('model_settings', {})
    
    @property
    def api_settings(self):
        return self.data.get('api_settings', {})
    
    @property
    def careerjet_config(self):
        return {
            **self.api_settings.get('careerjet', {}),
            "affid": os.getenv("CAREERJET_AFFID"),
            "user_ip": os.getenv("USER_IP", "192.168.0.1"),
            "user_agent": os.getenv("USER_AGENT", "Mozilla/5.0")
        }

config = Config()