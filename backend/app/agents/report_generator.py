from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from datetime import datetime
from app.utils.config import settings


class InterviewQuestion(BaseModel):
    category: str
    question: str
    focus_area: str
    difficulty_level: str


class RecommendationItem(BaseModel):
    category: str
    priority: str  # High, Medium, Low
    recommendation: str
    timeline: str
    impact: str


class RiskFactor(BaseModel):
    risk_type: str
    severity: str  # High, Medium, Low
    description: str
    mitigation_strategy: str


class ComprehensiveReport(BaseModel):
    executive_summary: str
    overall_recommendation: str
    hiring_confidence: float
    key_strengths: List[str]
    critical_concerns: List[str]
    interview_questions: List[InterviewQuestion]
    development_recommendations: List[RecommendationItem]
    risk_factors: List[RiskFactor]
    salary_recommendation_range: Optional[str]
    onboarding_suggestions: List[str]
    performance_predictions: Dict[str, str]


class ReportGeneratorAgent:
    def __init__(self, api_key: str):
        self.llm = ChatGoogleGenerativeAI(
            model=settings.MODEL_NAME, api_key=api_key, temperature=0.3
        )
        self.parser = PydanticOutputParser(pydantic_object=ComprehensiveReport)

    def generate_comprehensive_report(
        self,
        job_data: Dict,
        resume_data: Dict,
        skills_analysis: Dict,
        experience_analysis: Dict,
        education_analysis: Dict,
        cultural_analysis: Dict,
        overall_score: float,
    ) -> ComprehensiveReport:
        """
        Generate a comprehensive analysis report
        """
        print("Generating comprehensive report...")
        prompt = PromptTemplate(
            template="""
            Generate a comprehensive hiring report based on the complete candidate analysis:
            
            Job Requirements: {job_data}
            Candidate Profile: {resume_data}
            Skills Analysis: {skills_analysis}
            Experience Analysis: {experience_analysis}
            Education Analysis: {education_analysis}
            Cultural Fit Analysis: {cultural_analysis}
            Overall Score: {overall_score}/10
            
            Create a detailed report including:
            
            1. Executive Summary: 2-3 paragraph overview of the candidate's fit
            2. Overall Recommendation: Clear hiring recommendation with rationale
            3. Hiring Confidence: Confidence level in the recommendation (0-1)
            4. Key Strengths: Top 5 candidate strengths
            5. Critical Concerns: Main areas of concern or risk
            6. Interview Questions: 8-10 targeted questions across different categories
            7. Development Recommendations: Specific areas for candidate improvement
            8. Risk Factors: Potential risks and mitigation strategies
            9. Salary Recommendation Range: Suggested salary range if applicable
            10. Onboarding Suggestions: Recommendations for successful onboarding
            11. Performance Predictions: Expected performance in key areas
            
            Make the report actionable and specific to this role and candidate.
            
            {format_instructions}
            """,
            input_variables=[
                "job_data",
                "resume_data",
                "skills_analysis",
                "experience_analysis",
                "education_analysis",
                "cultural_analysis",
                "overall_score",
            ],
            partial_variables={
                "format_instructions": self.parser.get_format_instructions()
            },
        )

        chain = prompt | self.llm | self.parser
        print("Invoking LLM for comprehensive report generation...")
        report = chain.invoke(
            {
                "job_data": job_data,
                "resume_data": resume_data,
                "skills_analysis": skills_analysis,
                "experience_analysis": experience_analysis,
                "education_analysis": education_analysis,
                "cultural_analysis": cultural_analysis,
                "overall_score": overall_score,
            }
        )
        print("Comprehensive report generated successfully.")
        return report


class DashboardDataGenerator:
    """
    Generates structured data specifically for dashboard visualization
    """

    def __init__(self):
        self.score_thresholds = {
            "excellent": 8.5,
            "good": 7.0,
            "fair": 5.5,
            "poor": 0.0,
        }

    def generate_dashboard_data(
        self,
        job_data: Dict,
        resume_data: Dict,
        skills_analysis: Dict,
        experience_analysis: Dict,
        education_analysis: Dict,
        cultural_analysis: Dict,
        comprehensive_report: ComprehensiveReport,
        overall_score: float,
    ) -> Dict[str, Any]:
        """
        Generate structured data for dashboard display
        """
        print("Generating dashboard data...")

        # Calculate individual scores
        print("Calculating individual scores...")
        skills_score = skills_analysis.get("overall_match_score", 0)
        experience_score = experience_analysis.get("overall_experience_score", 0)
        education_score = education_analysis.get("overall_education_score", 0)
        cultural_score = cultural_analysis.get("cultural_fit_score", 0)

        # Determine ranking and recommendation
        print("Determining ranking and recommendation...")
        ranking_info = self._get_ranking_info(overall_score)

        # Generate charts data
        print("Generating charts data...")
        charts_data = self._generate_charts_data(
            skills_analysis, experience_analysis, education_analysis, cultural_analysis
        )

        # Create comprehensive dashboard data
        print("Structuring comprehensive dashboard data...")
        dashboard_data = {
            "candidate_summary": {
                "name": resume_data.get("name", "Unknown Candidate"),
                "email": resume_data.get("email", ""),
                "phone": resume_data.get("phone", ""),
                "analysis_date": datetime.now().isoformat(),
                "job_title": job_data.get("role_title", ""),
                "company": job_data.get("company", ""),
            },
            "scoring_overview": {
                "overall_fitness_score": round(overall_score, 1),
                "ranking_category": ranking_info["category"],
                "recommendation": ranking_info["recommendation"],
                "confidence_level": comprehensive_report.hiring_confidence,
                "score_breakdown": {
                    "Skills Match": round(skills_score, 1),
                    "Experience": round(experience_score, 1),
                    "Education": round(education_score, 1),
                    "Cultural Fit": round(cultural_score, 1),
                },
            },
            "detailed_metrics": {
                "skills_match_percentage": self._calculate_skills_percentage(
                    skills_analysis
                ),
                "experience_relevance": round(experience_score, 1),
                "education_alignment": round(education_score, 1),
                "cultural_fit_score": round(cultural_score, 1),
                "years_relevant_experience": experience_analysis.get(
                    "relevant_experience_years", 0
                ),
            },
            "key_insights": {
                "top_strengths": comprehensive_report.key_strengths[:5],
                "critical_gaps": self._extract_critical_gaps(
                    skills_analysis, experience_analysis, education_analysis
                ),
                "risk_factors": [
                    {
                        "type": risk.risk_type,
                        "severity": risk.severity,
                        "description": risk.description,
                    }
                    for risk in comprehensive_report.risk_factors
                ],
                "development_areas": [
                    rec.recommendation
                    for rec in comprehensive_report.development_recommendations
                    if rec.priority in ["High", "Medium"]
                ][:5],
            },
            "interview_preparation": {
                "focus_areas": self._extract_interview_focus_areas(
                    comprehensive_report
                ),
                "suggested_questions": [
                    {
                        "category": q.category,
                        "question": q.question,
                        "difficulty": q.difficulty_level,
                    }
                    for q in comprehensive_report.interview_questions
                ],
                "assessment_priorities": self._get_assessment_priorities(
                    overall_score, skills_analysis
                ),
            },
            "charts_data": charts_data,
            "detailed_analysis": {
                "skills": {
                    "matched_skills": skills_analysis.get("matched_skills", []),
                    "missing_skills": skills_analysis.get(
                        "missing_critical_skills", []
                    ),
                    "transferable_skills": skills_analysis.get(
                        "transferable_skills", []
                    ),
                    "skill_categories": skills_analysis.get("skill_categories", {}),
                },
                "experience": {
                    "relevant_years": experience_analysis.get(
                        "relevant_experience_years", 0
                    ),
                    "industry_alignment": experience_analysis.get(
                        "industry_alignment_score", 0
                    ),
                    "leadership_score": experience_analysis.get(
                        "leadership_experience_score", 0
                    ),
                    "career_progression": experience_analysis.get(
                        "role_progression_score", 0
                    ),
                },
                "education": {
                    "degree_match": education_analysis.get(
                        "education_level_match", False
                    ),
                    "field_relevance": education_analysis.get(
                        "field_of_study_relevance", 0
                    ),
                    "certifications": education_analysis.get(
                        "relevant_certifications", []
                    ),
                    "continuous_learning": education_analysis.get(
                        "continuous_learning_indicators", []
                    ),
                },
                "cultural_fit": {
                    "soft_skills": cultural_analysis.get("soft_skills_identified", []),
                    "communication_style": cultural_analysis.get(
                        "communication_style", ""
                    ),
                    "team_indicators": cultural_analysis.get(
                        "team_collaboration_signals", []
                    ),
                    "leadership_potential": cultural_analysis.get(
                        "leadership_indicators", []
                    ),
                },
            },
            "recommendations": {
                "hiring_decision": comprehensive_report.overall_recommendation,
                "salary_range": comprehensive_report.salary_recommendation_range,
                "onboarding_plan": comprehensive_report.onboarding_suggestions,
                "development_plan": [
                    {
                        "area": rec.category,
                        "priority": rec.priority,
                        "action": rec.recommendation,
                        "timeline": rec.timeline,
                        "expected_impact": rec.impact,
                    }
                    for rec in comprehensive_report.development_recommendations
                ],
            },
            "executive_summary": comprehensive_report.executive_summary,
        }

        print("Dashboard data generated successfully.")
        return dashboard_data

    def _get_ranking_info(self, score: float) -> Dict[str, str]:
        """Determine ranking category and recommendation based on score"""
        if score >= self.score_thresholds["excellent"]:
            return {
                "category": "Excellent Fit",
                "recommendation": "Strong candidate - Proceed to final interview",
            }
        elif score >= self.score_thresholds["good"]:
            return {
                "category": "Good Fit",
                "recommendation": "Good candidate - Proceed to technical interview",
            }
        elif score >= self.score_thresholds["fair"]:
            return {
                "category": "Fair Fit",
                "recommendation": "Potential candidate - Requires further evaluation",
            }
        else:
            return {
                "category": "Poor Fit",
                "recommendation": "Not recommended for this position",
            }

    def _calculate_skills_percentage(self, skills_analysis: Dict) -> float:
        """Calculate skills match percentage"""
        matched = len(skills_analysis.get("matched_skills", []))
        total_required = len(skills_analysis.get("matched_skills", [])) + len(
            skills_analysis.get("missing_critical_skills", [])
        )

        if total_required == 0:
            return 0.0

        return round((matched / total_required) * 100, 1)

    def _extract_critical_gaps(
        self, skills_analysis: Dict, experience_analysis: Dict, education_analysis: Dict
    ) -> List[str]:
        """Extract the most critical gaps across all areas"""
        gaps = []

        # Skills gaps
        critical_skills = skills_analysis.get("missing_critical_skills", [])[:2]
        gaps.extend([f"Missing skill: {skill}" for skill in critical_skills])

        # Experience gaps
        exp_gaps = experience_analysis.get("experience_gaps", [])[:2]
        gaps.extend(exp_gaps)

        # Education gaps
        edu_gaps = education_analysis.get("education_gaps", [])[:1]
        gaps.extend(edu_gaps)

        return gaps[:5]  # Return top 5 gaps

    def _extract_interview_focus_areas(self, report: ComprehensiveReport) -> List[str]:
        """Extract key areas to focus on during interviews"""
        focus_areas = []

        # Group questions by category to identify focus areas
        question_categories = {}
        for question in report.interview_questions:
            if question.category not in question_categories:
                question_categories[question.category] = 0
            question_categories[question.category] += 1

        # Sort by frequency and take top areas
        sorted_categories = sorted(
            question_categories.items(), key=lambda x: x[1], reverse=True
        )
        focus_areas = [category for category, _ in sorted_categories[:4]]

        return focus_areas

    def _get_assessment_priorities(
        self, overall_score: float, skills_analysis: Dict
    ) -> List[str]:
        """Determine assessment priorities based on analysis"""
        priorities = []

        if overall_score < 7.0:
            priorities.append("Comprehensive technical assessment required")

        missing_skills = len(skills_analysis.get("missing_critical_skills", []))
        if missing_skills > 2:
            priorities.append("Focus on skill gap evaluation")

        if overall_score >= 8.0:
            priorities.append("Cultural fit and team dynamics assessment")
            priorities.append("Leadership potential evaluation")

        return priorities

    def _generate_charts_data(
        self,
        skills_analysis: Dict,
        experience_analysis: Dict,
        education_analysis: Dict,
        cultural_analysis: Dict,
    ) -> Dict[str, Any]:
        """Generate data for various dashboard charts"""

        return {
            "radar_chart": {
                "categories": [
                    "Technical Skills",
                    "Experience",
                    "Education",
                    "Cultural Fit",
                    "Leadership",
                ],
                "scores": [
                    skills_analysis.get("overall_match_score", 0),
                    experience_analysis.get("overall_experience_score", 0),
                    education_analysis.get("overall_education_score", 0),
                    cultural_analysis.get("cultural_fit_score", 0),
                    experience_analysis.get("leadership_experience_score", 0),
                ],
            },
            "skills_distribution": {
                "matched": len(skills_analysis.get("matched_skills", [])),
                "missing": len(skills_analysis.get("missing_critical_skills", [])),
                "transferable": len(skills_analysis.get("transferable_skills", [])),
            },
            "experience_breakdown": {
                "relevant_years": experience_analysis.get(
                    "relevant_experience_years", 0
                ),
                "total_years": experience_analysis.get("total_experience_years", 0),
                "industry_alignment": experience_analysis.get(
                    "industry_alignment_score", 0
                ),
                "progression_score": experience_analysis.get(
                    "role_progression_score", 0
                ),
            },
            "education_metrics": {
                "degree_relevance": education_analysis.get(
                    "field_of_study_relevance", 0
                ),
                "institution_quality": education_analysis.get(
                    "institution_quality_score", 0
                ),
                "certifications_count": len(
                    education_analysis.get("relevant_certifications", [])
                ),
                "continuous_learning": len(
                    education_analysis.get("continuous_learning_indicators", [])
                ),
            },
            "score_trend": {
                "labels": ["Skills", "Experience", "Education", "Cultural Fit"],
                "values": [
                    skills_analysis.get("overall_match_score", 0),
                    experience_analysis.get("overall_experience_score", 0),
                    education_analysis.get("overall_education_score", 0),
                    cultural_analysis.get("cultural_fit_score", 0),
                ],
            },
        }
