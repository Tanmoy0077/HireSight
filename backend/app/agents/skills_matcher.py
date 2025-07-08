from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Dict
from app.utils.config import settings


class SkillsAnalysis(BaseModel):
    overall_match_score: float
    matched_skills: List[str]
    missing_critical_skills: List[str]
    transferable_skills: List[str]
    skill_categories: Dict[str, List[str]]
    recommendations: List[str]


class SkillsMatcherAgent:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME, api_key=api_key, temperature=0.2
        )
        self.parser = PydanticOutputParser(pydantic_object=SkillsAnalysis)

    def analyze_skills_match(
        self,
        candidate_skills: List[str],
        required_skills: List[str],
        preferred_skills: List[str],
    ) -> SkillsAnalysis:
        print("Analyzing skills match...")
        prompt = PromptTemplate(
            template="""
            Analyze the skill match between candidate and job requirements:
            
            Candidate Skills: {candidate_skills}
            Required Skills: {required_skills}
            Preferred Skills: {preferred_skills}
            
            Provide:
            1. Overall match score (0-10)
            2. List of matched skills
            3. Missing critical skills
            4. Transferable skills that could apply
            5. Skill categories (technical, soft, domain-specific)
            6. Recommendations for skill development
            
            {format_instructions}
            """,
            input_variables=["candidate_skills", "required_skills", "preferred_skills"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        chain = prompt | self.llm | self.parser
        print("Invoking LLM for skills analysis...")
        analysis = chain.invoke(
            {
                "candidate_skills": candidate_skills,
                "required_skills": required_skills,
                "preferred_skills": preferred_skills,
            }
        )
        print("Skills analysis complete.")
        return analysis
