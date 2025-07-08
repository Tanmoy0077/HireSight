from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Dict
from app.utils.config import settings


class ExperienceAnalysis(BaseModel):
    overall_experience_score: float
    relevant_experience_years: float
    industry_alignment_score: float
    role_progression_score: float
    leadership_experience_score: float
    achievements_quality_score: float
    experience_gaps: List[str]
    strengths: List[str]


class ExperienceEvaluatorAgent:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME, api_key=api_key, temperature=0.2
        )
        self.parser = PydanticOutputParser(pydantic_object=ExperienceAnalysis)

    def evaluate_experience(
        self, work_experience: List[Dict], job_requirements: Dict
    ) -> ExperienceAnalysis:
        print("Evaluating experience...")
        prompt = PromptTemplate(
            template="""
            Evaluate candidate's work experience against job requirements:
            
            Candidate Experience: {work_experience}
            Job Requirements: {job_requirements}
            
            Analyze:
            1. Overall experience relevance (0-10)
            2. Years of relevant experience
            3. Industry alignment score (0-10)
            4. Career progression score (0-10)
            5. Leadership experience score (0-10)
            6. Quality of achievements (0-10)
            7. Experience gaps
            8. Key strengths
            
            {format_instructions}
            """,
            input_variables=["work_experience", "job_requirements"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        chain = prompt | self.llm | self.parser
        print("Invoking LLM for experience evaluation...")
        analysis = chain.invoke(
            {"work_experience": work_experience, "job_requirements": job_requirements}
        )
        print("Experience evaluation complete.")
        return analysis
