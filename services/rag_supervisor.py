from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import torch
import random
from typing import Optional
from schemas.schema import JobData
from utils.logger import logger

class RAGSupervisor:
    def __init__(self, config):
        self.config = config
        self.qa_model_name = config.model_settings['qa_model']
        self.min_score = config.validation['min_score']
        self.initialize_models()

    def initialize_models(self):
        self.tokenizer = AutoTokenizer.from_pretrained(self.qa_model_name)
        self.model = AutoModelForQuestionAnswering.from_pretrained(self.qa_model_name)
        self.qa_pipeline = pipeline(
            "question-answering",
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if torch.cuda.is_available() else -1
        )

    def refine_query(self, query: str, conversation: dict) -> str:
        context = " ".join([msg['content'] for msg in conversation.get('history', [])])
        refinement_prompts = [
            f"Extract key details from: {query} considering context: {context}",
            f"Summarize core requirements from: {query} with context: {context}"
        ]
        
        try:
            prompt = random.choice(refinement_prompts)
            result = self.qa_pipeline({'question': prompt, 'context': query})
            return result['answer'] if result['score'] > 0.5 else query
        except Exception as e:
            logger.error(f"Refinement error: {str(e)}")
            return query

    def validate_job(self, job: JobData, query: str) -> bool:
        context = f"""
        Title: {job.title}
        Company: {job.company}
        Location: {job.location}
        Description: {job.description[:500]}
        """
        
        questions = [
            f"Is this {job.title} position relevant to {query}?",
            f"Does this job in {job.location} match location preferences?"
        ]
        
        scores = []
        for question in questions:
            try:
                result = self.qa_pipeline({'question': question, 'context': context})
                scores.append(result['score'])
            except Exception as e:
                logger.error(f"Validation error: {str(e)}")
                scores.append(0)
                
        avg_score = sum(scores) / len(scores)
        job.score = avg_score
        return avg_score >= self.min_score