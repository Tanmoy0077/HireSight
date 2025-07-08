from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List
from app.utils.config import settings


class JobRequirements(BaseModel):
    role_title: str
    required_skills: List[str]
    preferred_skills: List[str]
    experience_level: str
    education_requirements: List[str]
    responsibilities: List[str]
    company_culture_keywords: List[str]
    industry: str
    seniority_level: str


class JobParserAgent:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME, api_key=api_key, temperature=0.1
        )
        self.parser = PydanticOutputParser(pydantic_object=JobRequirements)

    def parse_job_description(self, job_text: str) -> JobRequirements:
        print("Parsing job description...")
        prompt = PromptTemplate(
            template="""
            Analyze the following job description and extract structured information:
            
            Job Description:
            {job_description}
            
            Extract the following information:
            1. Role title
            2. Required technical skills (must-have)
            3. Preferred skills (nice-to-have)
            4. Experience level required
            5. Education requirements
            6. Key responsibilities
            7. Company culture keywords
            8. Industry
            9. Seniority level
            
            {format_instructions}
            """,
            input_variables=["job_description"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        chain = prompt | self.llm | self.parser
        print("Invoking LLM for job description parsing...")
        data = chain.invoke({"job_description": job_text})
        print("Job description parsed successfully.")
        return data
