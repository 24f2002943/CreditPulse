export interface Company {
  id: number;
  name: string;
  sector: string;
  registration_number?: string;
  created_at: string;
}

export interface FinancialRatios {
  current_ratio: number | null;
  quick_ratio: number | null;
  cash_ratio: number | null;
  working_capital: number | null;
  debt_to_equity: number | null;
  debt_to_assets: number | null;
  interest_coverage_ratio: number | null;
  inventory_turnover: number | null;
  receivables_turnover: number | null;
  dso_days: number | null;
  asset_turnover: number | null;
  gross_margin: number | null;
  operating_margin: number | null;
  net_margin: number | null;
  roe: number | null;
  roa: number | null;
  price_to_book: number | null;
}

export interface RatioBenchmark {
  ratio_name: string;
  key: string;
  company_value: number | null;
  sector_median: number;
  status: 'healthy' | 'warning' | 'critical';
  percentile: number;
  higher_is_better: boolean;
}

export interface ShapExplanation {
  feature: string;
  feature_name_display: string;
  value: number;
  shap_value: number;
  impact_direction: 'increases_risk' | 'decreases_risk' | 'neutral';
  effect_label: string;
  importance_magnitude: number;
}

export interface CostStructure {
  variable_costs: number;
  fixed_costs: number;
  contribution_margin: number;
  contribution_margin_ratio: number;
  break_even_revenue: number;
  margin_of_safety_pct: number;
  operating_leverage: number;
  vulnerability_tier: string;
}

export interface InteractionLog {
  id?: number;
  transcript_text: string;
  interaction_type: 'negotiation' | 'service_failure' | 'service_recovery';
  sentiment_score?: number;
  risk_flag_score?: number;
  date?: string;
}

export interface RelationshipSummary {
  relationship_score: number;
  relationship_band: string;
  total_interactions: number;
  average_sentiment: number;
  average_risk_flag: number;
  failure_count: number;
  recovery_count: number;
  failure_resolution_rate: number;
  key_findings: string[];
}

export interface MacroSummary {
  sector: string;
  macro_adjustment: number;
  macro_score: number;
  elasticity: number;
  cyclicality: number;
  sector_growth_rate: number;
  rationale: string;
}

export interface CompanyRiskScore {
  company_id: number;
  company_name: string;
  sector: string;
  fiscal_year: number;
  composite_score: number;
  risk_band: 'low' | 'medium' | 'high';
  risk_band_label: string;
  probability_of_default: number;
  financial_score: number;
  relationship_score: number;
  macro_score: number;
  macro_adjustment: number;
  weight_distribution: {
    financial_weight: number;
    relationship_weight: number;
    macro_weight: number;
  };
  recommendation: string;
  shap_explanation: ShapExplanation[];
  financial_ratios: FinancialRatios;
  benchmarks: RatioBenchmark[];
  cost_structure: CostStructure;
  relationship_summary: RelationshipSummary;
  macro_summary: MacroSummary;
  key_strengths: string[];
  critical_vulnerabilities: string[];
  actionable_recommendations: string[];
}

export interface PortfolioOverviewData {
  total_assessed_companies: number;
  average_portfolio_score: number;
  risk_distribution: {
    low_risk_count: number;
    medium_risk_count: number;
    high_risk_count: number;
  };
  approval_rate_estimate: number;
}
