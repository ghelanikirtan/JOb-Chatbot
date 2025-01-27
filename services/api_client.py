import requests
from typing import List, Optional
from schemas.schema import JobData
from utils.config import config
from utils.logger import logger

class CareerJetAPI:
    def __init__(self):
        self.base_url = config.careerjet_config['endpoint']
        self.params = {
            "locale_code": config.careerjet_config['locale'],
            "pagesize": config.careerjet_config['pagesize'],
            "sort": config.careerjet_config['sort'],
            "affid": config.careerjet_config['affid'],
            "user_ip": config.careerjet_config['user_ip'],
            "user_agent": config.careerjet_config['user_agent']
        }

    def search_jobs(self, query: str, location: str = "") -> Optional[List[JobData]]:
        try:
            params = {**self.params, "keywords": query, "location": location}
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return self.parse_response(response.json())
        except Exception as e:
            logger.error(f"API Error: {str(e)}")
            return None

    def parse_response(self, data: dict) -> List[JobData]:
        jobs = []
        for result in data.get('jobs', []):
            jobs.append(JobData(
                title=result.get('title', ''),
                company=result.get('company', ''),
                location=result.get('locations', ''),
                description=result.get('description', ''),
                url=result.get('url', ''),
                posted_date=result.get('date', ''),
                salary=result.get('salary', '')
            ))
        return jobs
