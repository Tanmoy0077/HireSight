from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from app.workflow.resume_workflow import ResumeAnalysisWorkflow
from app.utils.file_processor import FileProcessor
from app.utils.config import settings
from typing import Dict, Any

router = APIRouter()

workflow = ResumeAnalysisWorkflow(settings.GOOGLE_API_KEY)
file_processor = FileProcessor()


@router.post("/analyze-resume", response_model=Dict[str, Any])
async def analyze_resume(
    job_description: str = Form(...), resume_file: UploadFile = File(...)
):
    """
    Analyze a resume against a job description
    """
    try:
        # Validate file
        if not resume_file.filename:
            raise HTTPException(status_code=400, detail="No file uploaded")

        # Check file size
        file_content = await resume_file.read()
        if len(file_content) > settings.MAX_FILE_SIZE:
            raise HTTPException(status_code=400, detail="File too large")

        # Check file extension
        file_extension = "." + resume_file.filename.split(".")[-1].lower()
        if file_extension not in settings.ALLOWED_EXTENSIONS:
            raise HTTPException(status_code=400, detail="Unsupported file format")

        # Extract text from file
        resume_text = file_processor.extract_text(resume_file.filename, file_content)

        if not resume_text.strip():
            raise HTTPException(
                status_code=400, detail="Could not extract text from file"
            )

        # Run analysis
        result = workflow.analyze_resume(job_description, resume_text)

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.post("/analyze-resume-text")
async def analyze_resume_text(
    job_description: str = Form(...), resume_text: str = Form(...)
):
    """
    Analyze resume text directly against a job description
    """
    try:
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Resume text cannot be empty")

        if not job_description.strip():
            raise HTTPException(
                status_code=400, detail="Job description cannot be empty"
            )

        # Run analysis
        result = workflow.analyze_resume(job_description, resume_text)

        return JSONResponse(content=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@router.get("/dashboard-sample")
async def get_dashboard_sample():
    """
    Get sample dashboard data for frontend development
    """
    sample_data = {
        "candidate_name": "John Doe",
        "analysis_date": "2024-01-15T10:30:00Z",
        "overall_fitness_score": 8.2,
        "ranking_category": "Excellent Fit",
        "score_breakdown": {
            "Skills Match": 8.5,
            "Experience": 8.0,
            "Cultural Fit": 8.8,
            "Education": 7.5,
        },
        "skills_match_percentage": 85.0,
        "experience_relevance": 8.0,
        "education_alignment": 7.5,
        "cultural_fit_score": 8.8,
        "top_strengths": [
            "Strong technical skills in required technologies",
            "Excellent leadership experience",
            "Proven track record of project delivery",
        ],
        "critical_gaps": [
            "Limited experience with cloud technologies",
            "No formal certification in required domain",
            "Lacks experience in agile methodologies",
        ],
        "recommendation": "Strong candidate - Proceed to final interview",
        "confidence_level": 0.85,
        "interview_focus_areas": [
            "Deep dive into cloud architecture experience",
            "Assess leadership style and team management",
            "Evaluate problem-solving approach",
        ],
        "charts_data": {
            "score_breakdown": {
                "Skills Match": 8.5,
                "Experience": 8.0,
                "Cultural Fit": 8.8,
                "Education": 7.5,
            },
            "skills_distribution": {"Matched": 12, "Missing": 3, "Transferable": 5},
        },
    }

    return JSONResponse(content=sample_data)
