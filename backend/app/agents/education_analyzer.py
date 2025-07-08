from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Dict
from app.utils.config import settings


class EducationMatch(BaseModel):
    degree_type: str
    field_relevance_score: float
    institution_reputation_score: float
    meets_minimum_requirement: bool


class CertificationAnalysis(BaseModel):
    certification_name: str
    relevance_score: float
    validity_status: str
    industry_recognition: str


class EducationAnalysis(BaseModel):
    overall_education_score: float
    degree_alignment_score: float
    field_of_study_relevance: float
    institution_quality_score: float
    education_level_match: bool
    relevant_certifications: List[CertificationAnalysis]
    missing_certifications: List[str]
    continuous_learning_indicators: List[str]
    education_strengths: List[str]
    education_gaps: List[str]
    recommendations: List[str]


class EducationAnalyzerAgent:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME, api_key=api_key, temperature=0.2
        )
        self.parser = PydanticOutputParser(pydantic_object=EducationAnalysis)

    def analyze_education(
        self,
        candidate_education: List[Dict],
        candidate_certifications: List[str],
        job_requirements: Dict,
    ) -> EducationAnalysis:
        """
        Analyze candidate's education and certifications against job requirements
        """
        print("Analyzing education...")
        prompt = PromptTemplate(
            template="""
            Analyze the candidate's educational background against job requirements:
            
            Candidate Education: {candidate_education}
            Candidate Certifications: {candidate_certifications}
            Job Requirements: {job_requirements}
            
            Evaluate the following aspects:
            
            1. Overall Education Score (0-10): Comprehensive assessment of educational fit
            2. Degree Alignment Score (0-10): How well the degree type matches requirements
            3. Field of Study Relevance (0-10): Relevance of academic field to the job
            4. Institution Quality Score (0-10): Reputation and quality of educational institutions
            5. Education Level Match: Whether minimum education requirements are met
            6. Relevant Certifications: List and analyze relevant certifications with scores
            7. Missing Certifications: Important certifications the candidate lacks
            8. Continuous Learning Indicators: Evidence of ongoing professional development
            9. Education Strengths: Key educational advantages
            10. Education Gaps: Areas where education falls short
            11. Recommendations: Specific suggestions for educational improvement
            
            Consider:
            - Degree level (Bachelor's, Master's, PhD) vs requirements
            - Field of study relevance to job domain
            - Institution reputation and accreditation
            - Recency of education
            - Professional certifications and their validity
            - Evidence of continuous learning (recent courses, workshops, etc.)
            - Industry-specific educational requirements
            - Alternative education paths (bootcamps, online courses, self-taught skills)
            
            {format_instructions}
            """,
            input_variables=[
                "candidate_education",
                "candidate_certifications",
                "job_requirements",
            ],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        chain = prompt | self.llm | self.parser
        print("Invoking LLM for education analysis...")
        analysis = chain.invoke(
            {
                "candidate_education": candidate_education,
                "candidate_certifications": candidate_certifications,
                "job_requirements": job_requirements,
            }
        )
        print("Education analysis complete.")
        return analysis

    def get_education_recommendations(
        self, analysis: EducationAnalysis, job_title: str
    ) -> List[str]:
        """
        Generate specific educational recommendations based on analysis
        """
        recommendations = []

        if analysis.overall_education_score < 7.0:
            if not analysis.education_level_match:
                recommendations.append(
                    f"Consider pursuing higher education relevant to {job_title}"
                )

            if analysis.field_of_study_relevance < 6.0:
                recommendations.append(
                    "Consider additional coursework in job-relevant subjects"
                )

        if analysis.missing_certifications:
            for cert in analysis.missing_certifications[:3]:  # Top 3 missing certs
                recommendations.append(
                    f"Obtain {cert} certification to strengthen profile"
                )

        if len(analysis.continuous_learning_indicators) < 2:
            recommendations.append(
                "Engage in continuous learning through online courses or workshops"
            )

        return recommendations


class EducationScoringEngine:
    """
    Advanced scoring engine for education analysis
    """

    @staticmethod
    def calculate_degree_relevance(candidate_degree: str, job_field: str) -> float:
        """Calculate how relevant the degree is to the job field"""
        # This would typically use a more sophisticated matching algorithm
        # For now, using a simplified approach

        tech_degrees = [
            "computer science",
            "software engineering",
            "information technology",
            "electrical engineering",
            "data science",
            "cybersecurity",
        ]
        business_degrees = [
            "business administration",
            "management",
            "marketing",
            "finance",
            "economics",
            "accounting",
        ]

        if "software" in job_field.lower() or "developer" in job_field.lower():
            if any(tech in candidate_degree.lower() for tech in tech_degrees):
                return 9.0
            elif any(bus in candidate_degree.lower() for bus in business_degrees):
                return 6.0
            else:
                return 4.0

        # Add more field-specific logic here
        return 7.0  # Default score

    @staticmethod
    def assess_institution_quality(institution_name: str) -> float:
        """Assess the quality/reputation of the educational institution"""
        # This would typically use a database of institution rankings
        # For demonstration, using a simplified approach

        top_tier = ["mit", "stanford", "harvard", "berkeley", "carnegie mellon"]
        if any(top in institution_name.lower() for top in top_tier):
            return 10.0

        # Would include more comprehensive institution ranking logic
        return 7.5  # Default score for unknown institutions
