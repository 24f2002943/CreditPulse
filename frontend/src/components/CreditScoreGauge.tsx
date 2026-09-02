'use client';

import React from 'react';
import { ShieldCheck, AlertTriangle, AlertOctagon, TrendingUp, Sparkles } from 'lucide-react';
import { CompanyRiskScore } from '../types';

interface CreditScoreGaugeProps {
  scoreData: CompanyRiskScore;
}

export const CreditScoreGauge: React.FC<CreditScoreGaugeProps> = ({ scoreData }) => {
  const {
    composite_score,
    risk_band,
    risk_band_label,
    probability_of_default,
    financial_score,
    relationship_score,
    macro_score,
    recommendation,
  } = scoreData;

  // Visual styling based on risk band
  const isLow = risk_band === 'low';
  const isMedium = risk_band === 'medium';

  const strokeColor = isLow ? '#10B981' : (isMedium ? '#F59E0B' : '#F43F5E');
  const glowClass = isLow ? 'shadow-glow-emerald' : (isMedium ? 'shadow-glow-amber' : 'shadow-glow-rose');
  const textGlow = isLow ? 'text-glow-emerald text-emerald-400' : (isMedium ? 'text-amber-400' : 'text-glow-rose text-rose-400');
  
  const badgeStyle = isLow 
    ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
    : (isMedium ? 'bg-amber-500/10 text-amber-400 border-amber-500/30' : 'bg-rose-500/10 text-rose-400 border-rose-500/30');

  const Icon = isLow ? ShieldCheck : (isMedium ? AlertTriangle : AlertOctagon);

  // SVG Gauge calculations
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (composite_score / 100) * circumference;

  return (
    <div className={`glass-panel rounded-2xl p-6 border ${glowClass} transition-all`}>
      
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-4">
        <div>
          <span className="text-xs font-semibold uppercase tracking-wider text-slate-400">Multi-Modal Risk Assessment</span>
          <h2 className="text-xl font-bold text-white mt-0.5">Composite CreditPulse Score</h2>
        </div>
        <div className={`flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold border ${badgeStyle}`}>
          <Icon className="h-4 w-4" />
          <span>{risk_band_label}</span>
        </div>
      </div>

      {/* Main Gauge Body */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
        
        {/* Radial Gauge */}
        <div className="md:col-span-5 flex flex-col items-center justify-center relative py-2">
          <div className="relative flex items-center justify-center">
            <svg className="h-44 w-44 -rotate-90 transform" viewBox="0 0 160 160">
              {/* Background Ring */}
              <circle
                cx="80"
                cy="80"
                r={radius}
                className="stroke-slate-800"
                strokeWidth="12"
                fill="transparent"
              />
              {/* Animated Progress Ring */}
              <circle
                cx="80"
                cy="80"
                r={radius}
                stroke={strokeColor}
                strokeWidth="12"
                fill="transparent"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round"
                style={{ transition: 'stroke-dashoffset 1s ease-in-out' }}
              />
            </svg>

            {/* Score Text in Center */}
            <div className="absolute flex flex-col items-center justify-center text-center">
              <span className={`text-4xl font-extrabold tracking-tight ${textGlow}`}>
                {composite_score}
              </span>
              <span className="text-[11px] font-medium uppercase tracking-widest text-slate-400 mt-0.5">
                Out of 100
              </span>
              <span className="mt-1 text-[10px] text-slate-400 bg-slate-900/90 px-2 py-0.5 rounded-full border border-slate-800">
                PD: {(probability_of_default * 100).toFixed(1)}%
              </span>
            </div>
          </div>

          <p className="mt-2 text-center text-xs text-slate-400">
            Probability of Default: <strong className="text-slate-200">{(probability_of_default * 100).toFixed(2)}%</strong> (1-Yr horizon)
          </p>
        </div>

        {/* Multi-Modal Fusion Sub-Scores */}
        <div className="md:col-span-7 flex flex-col justify-between space-y-3.5">
          
          {/* Financial Score Bar */}
          <div className="rounded-xl bg-slate-900/60 p-3 border border-slate-800">
            <div className="flex items-center justify-between text-xs mb-1.5">
              <span className="text-slate-300 font-medium flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-blue-500"></span>
                Structured Financial Model (60% weight)
              </span>
              <span className="font-bold text-blue-400">{financial_score} / 100</span>
            </div>
            <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full rounded-full bg-gradient-to-r from-blue-600 to-cyan-400"
                style={{ width: `${financial_score}%` }}
              />
            </div>
          </div>

          {/* Relationship NLP Score Bar */}
          <div className="rounded-xl bg-slate-900/60 p-3 border border-slate-800">
            <div className="flex items-center justify-between text-xs mb-1.5">
              <span className="text-slate-300 font-medium flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-purple-500"></span>
                B2B Relationship & Negotiation NLP (25% weight)
              </span>
              <span className="font-bold text-purple-400">{relationship_score} / 100</span>
            </div>
            <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full rounded-full bg-gradient-to-r from-purple-600 to-indigo-400"
                style={{ width: `${relationship_score}%` }}
              />
            </div>
          </div>

          {/* Macro Resilience Score Bar */}
          <div className="rounded-xl bg-slate-900/60 p-3 border border-slate-800">
            <div className="flex items-center justify-between text-xs mb-1.5">
              <span className="text-slate-300 font-medium flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-emerald-500"></span>
                Sector Macro & Elasticity Resilience (15% weight)
              </span>
              <span className="font-bold text-emerald-400">{macro_score} / 100</span>
            </div>
            <div className="h-2 w-full rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full rounded-full bg-gradient-to-r from-emerald-600 to-teal-400"
                style={{ width: `${macro_score}%` }}
              />
            </div>
          </div>

        </div>

      </div>

      {/* Underwriter Recommendation Banner */}
      <div className="mt-5 rounded-xl bg-slate-900/90 p-4 border border-slate-800 flex items-start gap-3">
        <Sparkles className="h-5 w-5 text-blue-400 shrink-0 mt-0.5" />
        <div>
          <h4 className="text-xs font-semibold text-slate-200 uppercase tracking-wider">Credit Decision & Covenant Guidance</h4>
          <p className="text-xs text-slate-300 mt-1 leading-relaxed">{recommendation}</p>
        </div>
      </div>

    </div>
  );
};
