export interface RiskFactor {
  type: string;
  severity: string;
  description: string;
}

export interface KeyInsights {
  top_strengths: string[];
  critical_gaps: string[];
  risk_factors: RiskFactor[];
}

export interface CandidateSummary {
  name: string;
  email: string;
  phone: string;
  job_title: string;
  analysis_date: string;
}

export interface ScoringOverview {
  overall_fitness_score: number;
  ranking_category: string;
  recommendation: string;
  confidence_level: number;
}

export interface SuggestedQuestion {
  category: string;
  question: string;
  difficulty: string;
}

export interface DevelopmentPlanItem {
  area: string;
  priority: string;
  action: string;
  timeline: string;
  expected_impact: string;
}

export interface AnalysisData {
  candidate_summary: CandidateSummary;
  scoring_overview: ScoringOverview;
  charts_data: {
    radar_chart: {
      categories: string[];
      scores: number[];
    };
    skills_distribution: {
      matched: number;
      missing: number;
      transferable: number;
    };
    score_trend: {
      labels: string[];
      values: number[];
    };
  };
  key_insights: KeyInsights;
  interview_preparation: {
    focus_areas: string[];
    suggested_questions: SuggestedQuestion[];
    assessment_priorities: string[];
  };
  recommendations: {
    hiring_decision: string;
    salary_range: string;
    onboarding_plan: string[];
    development_plan: DevelopmentPlanItem[];
  };
  executive_summary: string;
  detailed_metrics: unknown; // This was destructured in DashboardPage but not used.
}
