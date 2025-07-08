from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Optional
from app.utils.config import settings


class WorkExperience(BaseModel):
    company: str
    position: str
    duration: str
    responsibilities: List[str]
    achievements: List[str]


class Education(BaseModel):
    institution: str
    degree: str
    field_of_study: str
    graduation_year: Optional[str]


class ResumeData(BaseModel):
    name: str
    email: Optional[str]
    phone: Optional[str]
    skills: List[str]
    work_experience: List[WorkExperience]
    education: List[Education]
    certifications: List[str]
    projects: List[str]
    summary: Optional[str]


class ResumeExtractorAgent:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME, api_key=api_key, temperature=0.1
        )
        self.parser = PydanticOutputParser(pydantic_object=ResumeData)

    def extract_resume_data(self, resume_text: str) -> ResumeData:
        print("Extracting structured data from resume...")
        prompt = PromptTemplate(
            template="""
            Extract structured information from the following resume:
            
            Resume Text:
            {resume_text}
            
            Extract:
            1. Personal information (name, email, phone)
            2. Skills (technical and soft skills)
            3. Work experience with details
            4. Education background
            5. Certifications
            6. Notable projects
            7. Professional summary
            
            {format_instructions}
            """,
            input_variables=["resume_text"],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        chain = prompt | self.llm | self.parser
        print("Invoking LLM for resume data extraction...")
        data = chain.invoke({"resume_text": resume_text})
        print("Resume data extracted successfully.")
        return data
