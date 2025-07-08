from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Dict
from app.utils.config import settings


class CulturalFitAnalysis(BaseModel):
    cultural_fit_score: float
    soft_skills_identified: List[str]
    communication_style: str
    leadership_indicators: List[str]
    team_collaboration_signals: List[str]
    adaptability_score: float
    cultural_alignment_factors: List[str]


class CulturalFitAgent:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME, api_key=api_key, temperature=0.3
        )
        self.parser = PydanticOutputParser(pydantic_object=CulturalFitAnalysis)

    def analyze_cultural_fit(
        self, resume_data: Dict, company_culture_keywords: List[str]
    ) -> CulturalFitAnalysis:
        print("Analyzing cultural fit...")
        prompt = PromptTemplate(
            template="""
            Analyze cultural fit based on resume content and company culture:
            
            Resume Data: {resume_data}
            Company Culture Keywords: {company_culture_keywords}
            
            Evaluate:
            1. Cultural fit score (0-10)
            2. Soft skills demonstrated
            3. Communication style indicators
            4. Leadership potential indicators
            5. Team collaboration evidence
            6. Adaptability score (0-10)
            7. Cultural alignment factors
            
            {format_instructions}
            """,
            input_variables=["resume_data", "company_culture_keywords"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        chain = prompt | self.llm | self.parser
        print("Invoking LLM for cultural fit analysis...")
        analysis = chain.invoke(
            {
                "resume_data": resume_data,
                "company_culture_keywords": company_culture_keywords,
            }
        )
        print("Cultural fit analysis complete.")
        return analysis
