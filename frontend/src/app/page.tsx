'use client';

import React, { useState, useEffect } from 'react';
import { Navbar } from '../components/Navbar';
import { CreditScoreGauge } from '../components/CreditScoreGauge';
import { ShapContributionChart } from '../components/ShapContributionChart';
import { FinancialRatiosGrid } from '../components/FinancialRatiosGrid';
import { CostStructureCard } from '../components/CostStructureCard';
import { RelationshipTimeline } from '../components/RelationshipTimeline';
import { StatementUploadModal } from '../components/StatementUploadModal';
import { WhatIfSimulator } from '../components/WhatIfSimulator';
import { PortfolioOverview } from '../components/PortfolioOverview';
import { Company, CompanyRiskScore, PortfolioOverviewData, InteractionLog } from '../types';
import { fetchCompanies, fetchCompanyScore, fetchPortfolioOverview, fetchInteractions } from '../services/api';
import { Building2, ShieldCheck, Sparkles, AlertCircle, CheckCircle2, ArrowUpRight, TrendingUp, Lightbulb, FileText } from 'lucide-react';

export default function Home() {
  const [role, setRole] = useState<'lender' | 'msme_owner'>('lender');
  const [companies, setCompanies] = useState<Company[]>([]);
  const [selectedCompanyId, setSelectedCompanyId] = useState<number>(1);
  const [selectedSector, setSelectedSector] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  
  const [scoreData, setScoreData] = useState<CompanyRiskScore | null>(null);
  const [portfolioData, setPortfolioData] = useState<PortfolioOverviewData | null>(null);
  const [interactions, setInteractions] = useState<{ analysis: any; history: InteractionLog[] } | null>(null);
  
  const [isUploadModalOpen, setIsUploadModalOpen] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Load initial companies and portfolio data
  useEffect(() => {
    async function loadInitial() {
      setIsLoading(true);
      const [comps, port] = await Promise.all([fetchCompanies(), fetchPortfolioOverview()]);
      setCompanies(comps);
      setPortfolioData(port);
      if (comps.length > 0) {
        setSelectedCompanyId(comps[0].id);
      }
      setIsLoading(false);
    }
    loadInitial();
  }, []);

  // Fetch score and interactions when selected company changes
  useEffect(() => {
    if (!selectedCompanyId) return;
    async function loadCompanyDetails() {
      const [score, inter] = await Promise.all([
        fetchCompanyScore(selectedCompanyId),
        fetchInteractions(selectedCompanyId)
      ]);
      setScoreData(score);
      setInteractions(inter);
    }
    loadCompanyDetails();
  }, [selectedCompanyId]);

  const selectedCompany = companies.find((c) => c.id === selectedCompanyId);

  return (
    <div className="min-h-screen bg-[#090D16] text-slate-100 flex flex-col">
      
      {/* Top Navigation */}
      <Navbar
        currentRole={role}
        onRoleChange={setRole}
        onOpenUpload={() => setIsUploadModalOpen(true)}
        selectedCompanyName={selectedCompany?.name}
      />

      {/* Main Content Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
        
        {/* Research Novelty Banner */}
        <div className="rounded-2xl bg-gradient-to-r from-blue-950/40 via-slate-900/80 to-purple-950/40 p-4 border border-blue-500/20 backdrop-blur-md flex flex-col md:flex-row md:items-center justify-between gap-4 shadow-sm">
          <div className="flex items-center gap-3">
            <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-blue-500/10 text-blue-400 border border-blue-500/20">
              <Sparkles className="h-5 w-5" />
            </div>
            <div>
              <h1 className="text-sm font-bold text-white">
                Multi-Modal MSME Credit Risk Architecture
              </h1>
              <p className="text-xs text-slate-300 mt-0.5">
                Fuses structured financial ratio analysis (60%), unstructured NLP relationship signals (25%), and sector elasticity dynamics (15%) with SHAP explainability.
              </p>
            </div>
          </div>
          <div className="flex items-center gap-2 shrink-0">
            <span className="rounded-lg bg-slate-800/80 px-2.5 py-1 text-[11px] font-medium text-slate-300 border border-slate-700">
              XGBoost + Calibrated PD
            </span>
            <span className="rounded-lg bg-slate-800/80 px-2.5 py-1 text-[11px] font-medium text-slate-300 border border-slate-700">
              SHAP Audit
            </span>
          </div>
        </div>

        {/* ========================================================================= */}
        {/* LENDER ANALYST VIEW                                                      */}
        {/* ========================================================================= */}
        {role === 'lender' && (
          <div className="space-y-8">
            
            {/* Portfolio Overview & Quick Selector */}
            {portfolioData && (
              <PortfolioOverview
                overview={portfolioData}
                companies={companies}
                selectedCompanyId={selectedCompanyId}
                onSelectCompany={setSelectedCompanyId}
                selectedSector={selectedSector}
                onSelectSector={setSelectedSector}
                searchQuery={searchQuery}
                onSearchChange={setSearchQuery}
              />
            )}

            {/* Selected Company Header Banner */}
            {scoreData && (
              <div className="glass-panel rounded-2xl p-5 border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-semibold uppercase tracking-wider text-cyan-400">
                      Active Underwriting Assessment
                    </span>
                    <span className="text-xs text-slate-500">•</span>
                    <span className="text-xs text-slate-400">FY{scoreData.fiscal_year} Financials</span>
                  </div>
                  <h2 className="text-2xl font-black text-white mt-1">{scoreData.company_name}</h2>
                  <p className="text-xs text-slate-400 mt-0.5">{scoreData.sector} • Reg #{scoreData.company_id}</p>
                </div>

                <div className="flex items-center gap-3">
                  <div className="text-right">
                    <span className="text-[10px] uppercase tracking-wider text-slate-400">Sector Elasticity</span>
                    <div className="text-xs font-bold text-slate-200">{scoreData.macro_summary.elasticity} (Multiplier: {scoreData.macro_adjustment}x)</div>
                  </div>
                  <button
                    onClick={() => setIsUploadModalOpen(true)}
                    className="rounded-xl bg-blue-600 px-4 py-2 text-xs font-semibold text-white shadow-glow-blue hover:bg-blue-500 transition-all"
                  >
                    Re-evaluate Statement
                  </button>
                </div>
              </div>
            )}

            {/* Main Deep-Dive Grid: Gauge + SHAP */}
            {scoreData && (
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
                
                {/* Composite Risk Gauge */}
                <div className="lg:col-span-6">
                  <CreditScoreGauge scoreData={scoreData} />
                </div>

                {/* SHAP Feature Contribution Chart */}
                <div className="lg:col-span-6">
                  <ShapContributionChart explanations={scoreData.shap_explanation} />
                </div>

              </div>
            )}

            {/* Financial Ratios Grid */}
            {scoreData && (
              <FinancialRatiosGrid
                ratios={scoreData.financial_ratios}
                benchmarks={scoreData.benchmarks}
              />
            )}

            {/* Cost Structure & Break-Even Analysis */}
            {scoreData && (
              <CostStructureCard costData={scoreData.cost_structure} />
            )}

            {/* B2B Relationship & Negotiation NLP Timeline */}
            {scoreData && interactions && (
              <RelationshipTimeline
                summary={scoreData.relationship_summary}
                history={interactions.history}
              />
            )}

          </div>
        )}

        {/* ========================================================================= */}
        {/* MSME OWNER VIEW                                                           */}
        {/* ========================================================================= */}
        {role === 'msme_owner' && scoreData && (
          <div className="space-y-8">
            
            {/* Health Overview Hero Card */}
            <div className="glass-panel rounded-3xl p-8 border border-slate-800 shadow-glow-blue">
              <div className="grid grid-cols-1 md:grid-cols-12 gap-8 items-center">
                
                <div className="md:col-span-7 space-y-4">
                  <div className="inline-flex items-center gap-2 rounded-full bg-emerald-500/10 px-3 py-1 text-xs font-semibold text-emerald-400 border border-emerald-500/20">
                    <Building2 className="h-4 w-4" />
                    <span>MSME Credit Readiness Portal</span>
                  </div>

                  <h2 className="text-3xl font-extrabold text-white tracking-tight">
                    {scoreData.company_name}
                  </h2>
                  <p className="text-xs text-slate-300 leading-relaxed max-w-xl">
                    Your CreditPulse score combines your balance sheet ratios with your commercial partnership track record to give lenders an auditable, fair assessment of your loan readiness.
                  </p>

                  <div className="pt-2 flex flex-wrap items-center gap-4 text-xs">
                    <div className="rounded-xl bg-slate-900/80 px-4 py-2.5 border border-slate-800">
                      <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Risk Band</span>
                      <strong className="text-white text-sm">{scoreData.risk_band_label}</strong>
                    </div>
                    <div className="rounded-xl bg-slate-900/80 px-4 py-2.5 border border-slate-800">
                      <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Sector Growth</span>
                      <strong className="text-white text-sm">+{(scoreData.macro_summary.sector_growth_rate * 100).toFixed(1)}% YoY</strong>
                    </div>
                    <div className="rounded-xl bg-slate-900/80 px-4 py-2.5 border border-slate-800">
                      <span className="text-[10px] text-slate-400 uppercase tracking-wider block">Est. Loan Eligibility</span>
                      <strong className="text-emerald-400 text-sm">
                        {scoreData.composite_score >= 70 ? '$500,000 - $1.2M' : '$150,000 - $350,000'}
                      </strong>
                    </div>
                  </div>
                </div>

                {/* Health Radial Display */}
                <div className="md:col-span-5 flex flex-col items-center justify-center p-4 rounded-2xl bg-slate-900/60 border border-slate-800">
                  <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Credit Readiness Score</span>
                  <div className="mt-3 text-5xl font-black text-emerald-400 text-glow-emerald">
                    {scoreData.composite_score}
                  </div>
                  <span className="text-xs text-slate-400 mt-1">out of 100</span>
                  <p className="mt-3 text-center text-xs text-slate-300 max-w-xs leading-snug">
                    {scoreData.recommendation}
                  </p>
                </div>

              </div>
            </div>

            {/* Actionable Health Recommendations */}
            <div className="glass-panel rounded-2xl p-6 border border-slate-800">
              <div className="flex items-center gap-2 border-b border-slate-800 pb-4">
                <Lightbulb className="h-5 w-5 text-amber-400" />
                <div>
                  <h3 className="text-lg font-bold text-white">Actionable Steps to Enhance Your Credit Score</h3>
                  <p className="text-xs text-slate-400">Prioritized guidance to optimize financial ratios and negotiate better lending terms.</p>
                </div>
              </div>

              <div className="mt-5 grid grid-cols-1 md:grid-cols-2 gap-4">
                {scoreData.actionable_recommendations.map((rec, idx) => (
                  <div key={idx} className="rounded-xl bg-slate-900/70 p-4 border border-slate-800 flex items-start gap-3">
                    <span className="flex h-6 w-6 shrink-0 items-center justify-center rounded-full bg-blue-500/10 text-xs font-bold text-blue-400 border border-blue-500/20">
                      {idx + 1}
                    </span>
                    <p className="text-xs text-slate-200 leading-relaxed">{rec}</p>
                  </div>
                ))}
              </div>
            </div>

            {/* What-If Scenario Simulator */}
            <WhatIfSimulator scoreData={scoreData} />

            {/* Ratios Breakdown for MSME */}
            <FinancialRatiosGrid
              ratios={scoreData.financial_ratios}
              benchmarks={scoreData.benchmarks}
            />

          </div>
        )}

      </main>

      {/* Statement Upload Modal */}
      <StatementUploadModal
        isOpen={isUploadModalOpen}
        onClose={() => setIsUploadModalOpen(false)}
        companies={companies}
        onUploadSuccess={(compId) => {
          setSelectedCompanyId(compId);
        }}
      />

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-[#090D16]/90 py-6 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <p>© 2026 CreditPulse — Relationship-Aware MSME Credit Scoring & Risk Analytics.</p>
          <div className="flex items-center gap-4">
            <span>FastAPI + XGBoost + SHAP</span>
            <span>•</span>
            <span>Next.js 14 + Tailwind</span>
            <span>•</span>
            <span className="text-slate-400">Research & Portfolio Release v1.0</span>
          </div>
        </div>
      </footer>

    </div>
  );
}
