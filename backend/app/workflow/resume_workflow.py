from langgraph.graph import StateGraph, END
from typing import TypedDict, Dict, Any
from app.agents.job_parser import JobParserAgent
from app.agents.resume_extractor import ResumeExtractorAgent
from app.agents.skills_matcher import SkillsMatcherAgent
from app.agents.experience_evaluator import ExperienceEvaluatorAgent
from app.agents.cultural_fit import CulturalFitAgent
from app.agents.education_analyzer import EducationAnalyzerAgent
from app.agents.report_generator import DashboardDataGenerator, ReportGeneratorAgent
import os


class WorkflowState(TypedDict):
    job_description: str
    resume_text: str
    job_data: Dict[str, Any]
    resume_data: Dict[str, Any]
    skills_analysis: Dict[str, Any]
    experience_analysis: Dict[str, Any]
    education_analysis: Dict[str, Any]  # Added
    cultural_analysis: Dict[str, Any]
    overall_score: float
    final_report: Dict[str, Any]
    comprehensive_report: Dict[str, Any]  # Added
    error: str


class ResumeAnalysisWorkflow:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.job_parser = JobParserAgent(api_key)
        self.resume_extractor = ResumeExtractorAgent(api_key)
        self.skills_matcher = SkillsMatcherAgent(api_key)
        self.experience_evaluator = ExperienceEvaluatorAgent(api_key)
        self.education_analyzer = EducationAnalyzerAgent(api_key)  # Added
        self.cultural_fit_agent = CulturalFitAgent(api_key)
        self.report_generator = ReportGeneratorAgent(api_key)  # Added
        self.dashboard_generator = DashboardDataGenerator()  # Added

        # Build the workflow graph
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        workflow = StateGraph(WorkflowState)

        # Add nodes
        workflow.add_node("parse_job", self._parse_job_description)
        workflow.add_node("extract_resume", self._extract_resume_data)
        workflow.add_node("analyze_skills", self._analyze_skills)
        workflow.add_node("evaluate_experience", self._evaluate_experience)
        workflow.add_node("analyze_education", self._analyze_education)
        workflow.add_node("analyze_cultural_fit", self._analyze_cultural_fit)
        workflow.add_node("generate_report", self._generate_comprehensive_report)

        # Add edges
        workflow.add_edge("parse_job", "extract_resume")
        workflow.add_edge("extract_resume", "analyze_skills")
        workflow.add_edge("analyze_skills", "evaluate_experience")
        workflow.add_edge("evaluate_experience", "analyze_education")
        workflow.add_edge("analyze_education", "analyze_cultural_fit")
        workflow.add_edge("analyze_cultural_fit", "generate_report")
        workflow.add_edge("generate_report", END)

        # Set entry point
        workflow.set_entry_point("parse_job")

        return workflow.compile()

    def save_graph_as_mermaid(
        self, folder_path: str, filename: str = "workflow_graph.png"
    ):
        """
        Generates a Mermaid markdown representation of the workflow graph and saves it.

        The output file can be viewed in markdown editors that support Mermaid,
        such as VS Code with the "Markdown Preview Mermaid Support" extension,
        or on platforms like GitHub.
        """
        try:
            # Ensure the output directory exists
            os.makedirs(folder_path, exist_ok=True)
            file_path = os.path.join(folder_path, filename)

            # Get the Mermaid syntax string from the graph
            self.workflow.get_graph().draw_mermaid_png(output_file_path=file_path)

            print(f"Workflow graph (Mermaid) saved to {file_path}")
        except Exception as e:
            print(f"An error occurred while generating the Mermaid graph: {e}")

    def _parse_job_description(self, state: WorkflowState) -> WorkflowState:
        try:
            job_data = self.job_parser.parse_job_description(state["job_description"])
            state["job_data"] = job_data.dict()
            return state
        except Exception as e:
            state["error"] = f"Job parsing error: {str(e)}"
            return state

    def _extract_resume_data(self, state: WorkflowState) -> WorkflowState:
        try:
            resume_data = self.resume_extractor.extract_resume_data(
                state["resume_text"]
            )
            state["resume_data"] = resume_data.dict()
            return state
        except Exception as e:
            state["error"] = f"Resume extraction error: {str(e)}"
            return state

    def _analyze_skills(self, state: WorkflowState) -> WorkflowState:
        try:
            skills_analysis = self.skills_matcher.analyze_skills_match(
                state["resume_data"]["skills"],
                state["job_data"]["required_skills"],
                state["job_data"]["preferred_skills"],
            )
            state["skills_analysis"] = skills_analysis.dict()
            return state
        except Exception as e:
            state["error"] = f"Skills analysis error: {str(e)}"
            return state

    def _evaluate_experience(self, state: WorkflowState) -> WorkflowState:
        try:
            experience_analysis = self.experience_evaluator.evaluate_experience(
                state["resume_data"]["work_experience"], state["job_data"]
            )
            state["experience_analysis"] = experience_analysis.dict()
            return state
        except Exception as e:
            state["error"] = f"Experience evaluation error: {str(e)}"
            return state

    def _analyze_cultural_fit(self, state: WorkflowState) -> WorkflowState:
        try:
            cultural_analysis = self.cultural_fit_agent.analyze_cultural_fit(
                state["resume_data"], state["job_data"]["company_culture_keywords"]
            )
            state["cultural_analysis"] = cultural_analysis.dict()
            return state
        except Exception as e:
            state["error"] = f"Cultural fit analysis error: {str(e)}"
            return state

    def _generate_final_report(self, state: WorkflowState) -> WorkflowState:
        try:
            # Calculate overall score
            skills_score = state["skills_analysis"]["overall_match_score"]
            experience_score = state["experience_analysis"]["overall_experience_score"]
            cultural_score = state["cultural_analysis"]["cultural_fit_score"]

            # Weighted average
            overall_score = (
                skills_score * 0.4 + experience_score * 0.4 + cultural_score * 0.2
            )
            state["overall_score"] = overall_score

            # Generate comprehensive report
            report = self._create_dashboard_data(state)
            state["final_report"] = report

            return state
        except Exception as e:
            state["error"] = f"Report generation error: {str(e)}"
            return state

    def _create_dashboard_data(self, state: WorkflowState) -> Dict[str, Any]:
        """Create structured data for dashboard display"""

        # Determine ranking category
        score = state["overall_score"]
        if score >= 8.5:
            ranking = "Excellent Fit"
            recommendation = "Strong candidate - Proceed to final interview"
        elif score >= 7.0:
            ranking = "Good Fit"
            recommendation = "Good candidate - Proceed to technical interview"
        elif score >= 5.5:
            ranking = "Fair Fit"
            recommendation = "Potential candidate - Requires further evaluation"
        else:
            ranking = "Poor Fit"
            recommendation = "Not recommended for this position"

        # Extract key information
        resume_data = state["resume_data"]
        skills_analysis = state["skills_analysis"]
        experience_analysis = state["experience_analysis"]
        cultural_analysis = state["cultural_analysis"]

        # Create charts data
        charts_data = {
            "score_breakdown": {
                "Skills Match": skills_analysis["overall_match_score"],
                "Experience": experience_analysis["overall_experience_score"],
                "Cultural Fit": cultural_analysis["cultural_fit_score"],
                "Education": 7.5,  # Placeholder - would come from education agent
            },
            "skills_distribution": {
                "Matched": len(skills_analysis["matched_skills"]),
                "Missing": len(skills_analysis["missing_critical_skills"]),
                "Transferable": len(skills_analysis["transferable_skills"]),
            },
        }

        return {
            "candidate_name": resume_data.get("name", "Unknown"),
            "analysis_date": "2024-01-15T10:30:00Z",  # Would be current timestamp
            "overall_fitness_score": round(score, 1),
            "ranking_category": ranking,
            "score_breakdown": charts_data["score_breakdown"],
            "skills_match_percentage": round(
                (
                    len(skills_analysis["matched_skills"])
                    / max(len(state["job_data"]["required_skills"]), 1)
                )
                * 100,
                1,
            ),
            "experience_relevance": experience_analysis["overall_experience_score"],
            "education_alignment": 7.5,  # Placeholder
            "cultural_fit_score": cultural_analysis["cultural_fit_score"],
            "top_strengths": experience_analysis["strengths"][:3],
            "critical_gaps": skills_analysis["missing_critical_skills"][:3],
            "recommendation": recommendation,
            "confidence_level": 0.85,  # Could be calculated based on data completeness
            "interview_focus_areas": [
                "Technical skills assessment",
                "Cultural fit evaluation",
                "Experience deep-dive",
            ],
            "charts_data": charts_data,
            "detailed_analysis": {
                "skills": skills_analysis,
                "experience": experience_analysis,
                "cultural_fit": cultural_analysis,
            },
        }

    def analyze_resume(self, job_description: str, resume_text: str) -> Dict[str, Any]:
        """Run the complete analysis workflow"""
        initial_state = WorkflowState(
            job_description=job_description,
            resume_text=resume_text,
            job_data={},
            resume_data={},
            skills_analysis={},
            experience_analysis={},
            education_analysis={},
            cultural_analysis={},
            overall_score=0.0,
            final_report={},
            comprehensive_report={},
            error="",
        )

        result = self.workflow.invoke(initial_state)

        if result.get("error"):
            raise Exception(result["error"])

        return result["final_report"]

    def _analyze_education(self, state: WorkflowState) -> WorkflowState:
        """Analyze candidate's education and certifications"""
        try:
            education_analysis = self.education_analyzer.analyze_education(
                state["resume_data"]["education"],
                state["resume_data"]["certifications"],
                state["job_data"],
            )
            state["education_analysis"] = education_analysis.dict()
            return state
        except Exception as e:
            state["error"] = f"Education analysis error: {str(e)}"
            return state

    def _generate_comprehensive_report(self, state: WorkflowState) -> WorkflowState:
        """Generate comprehensive analysis report and dashboard data"""
        try:
            # Calculate overall score with education included
            skills_score = state["skills_analysis"]["overall_match_score"]
            experience_score = state["experience_analysis"]["overall_experience_score"]
            education_score = state["education_analysis"]["overall_education_score"]
            cultural_score = state["cultural_analysis"]["cultural_fit_score"]

            # Weighted average (adjusted to include education)
            overall_score = (
                skills_score * 0.35
                + experience_score * 0.35
                + education_score * 0.15
                + cultural_score * 0.15
            )
            state["overall_score"] = overall_score

            # Generate comprehensive report
            comprehensive_report = self.report_generator.generate_comprehensive_report(
                state["job_data"],
                state["resume_data"],
                state["skills_analysis"],
                state["experience_analysis"],
                state["education_analysis"],
                state["cultural_analysis"],
                overall_score,
            )

            # Generate dashboard data
            dashboard_data = self.dashboard_generator.generate_dashboard_data(
                state["job_data"],
                state["resume_data"],
                state["skills_analysis"],
                state["experience_analysis"],
                state["education_analysis"],
                state["cultural_analysis"],
                comprehensive_report,
                overall_score,
            )

            state["final_report"] = dashboard_data
            state["comprehensive_report"] = comprehensive_report.dict()

            return state
        except Exception as e:
            state["error"] = f"Report generation error: {str(e)}"
            return state
