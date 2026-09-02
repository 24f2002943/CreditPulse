'use client';

import React, { useState } from 'react';
import { Sliders, Sparkles, TrendingUp, ArrowRight, ShieldCheck } from 'lucide-react';
import { CompanyRiskScore } from '../types';

interface WhatIfSimulatorProps {
  scoreData: CompanyRiskScore;
}

export const WhatIfSimulator: React.FC<WhatIfSimulatorProps> = ({ scoreData }) => {
  const baseScore = scoreData.composite_score;
  const baseMargin = (scoreData.financial_ratios.net_margin || 0.05) * 100;
  const baseDSO = scoreData.financial_ratios.dso_days || 60;
  const baseDE = scoreData.financial_ratios.debt_to_equity || 1.2;

  // Simulator State Levers
  const [marginDelta, setMarginDelta] = useState<number>(1.5); // +1.5% margin
  const [dsoDelta, setDsoDelta] = useState<number>(-15); // -15 days DSO
  const [debtPaydownPct, setDebtPaydownPct] = useState<number>(20); // 20% debt paydown

  // Dynamic Simulated Score Calculation
  // 1% margin expansion adds ~4.5 points
  // 10 days DSO reduction adds ~3.2 points
  // 10% debt paydown adds ~2.8 points
  const simulatedScore = Math.min(
    98.5,
    Math.max(
      15.0,
      Number((baseScore + (marginDelta * 4.2) + (Math.abs(dsoDelta) * 0.32) + (debtPaydownPct * 0.28)).toFixed(1))
    )
  );

  const scoreGain = Number((simulatedScore - baseScore).toFixed(1));
  const newRiskBand = simulatedScore >= 75 ? 'Low Risk (Grade A)' : (simulatedScore >= 50 ? 'Medium Risk (Grade B)' : 'High Risk (Grade D)');
  const estInterestDiscount = (scoreGain * 0.08).toFixed(2); // Estimated ~8bps loan interest discount per point

  return (
    <div className="glass-panel rounded-2xl p-6 border border-slate-800 transition-all shadow-glow-blue">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-800 pb-4 gap-3">
        <div>
          <div className="flex items-center gap-2">
            <div className="flex h-7 w-7 items-center justify-center rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
              <Sliders className="h-4 w-4" />
            </div>
            <h3 className="text-lg font-bold text-white">Interactive What-If Credit Readiness Simulator</h3>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Simulate how financial optimizations (margin expansion, DSO compression, debt reduction) impact loan eligibility.
          </p>
        </div>

        {/* Score Comparison Badge */}
        <div className="flex items-center gap-3 bg-slate-900/90 px-4 py-2 rounded-xl border border-slate-800">
          <div className="text-right">
            <span className="text-[10px] uppercase tracking-wider text-slate-400">Current</span>
            <div className="text-base font-bold text-slate-300">{baseScore}</div>
          </div>
          <ArrowRight className="h-4 w-4 text-emerald-400" />
          <div>
            <span className="text-[10px] uppercase tracking-wider text-emerald-400">Simulated</span>
            <div className="text-xl font-extrabold text-emerald-400">
              {simulatedScore} <span className="text-xs font-semibold text-emerald-300">(+{scoreGain})</span>
            </div>
          </div>
        </div>
      </div>

      {/* Simulator Sliders Grid */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-6">
        
        {/* Lever 1: Margin Improvement */}
        <div className="rounded-xl bg-slate-900/60 p-4 border border-slate-800">
          <div className="flex items-center justify-between text-xs mb-2">
            <span className="font-semibold text-slate-200">Net Profit Margin Delta</span>
            <span className="font-bold text-cyan-400">{marginDelta > 0 ? `+${marginDelta}%` : `${marginDelta}%`}</span>
          </div>
          <input
            type="range"
            min="-2.0"
            max="5.0"
            step="0.5"
            value={marginDelta}
            onChange={(e) => setMarginDelta(Number(e.target.value))}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400"
          />
          <div className="mt-2 flex items-center justify-between text-[11px] text-slate-400">
            <span>Base: {baseMargin.toFixed(1)}%</span>
            <span>Target: {(baseMargin + marginDelta).toFixed(1)}%</span>
          </div>
        </div>

        {/* Lever 2: DSO Compression */}
        <div className="rounded-xl bg-slate-900/60 p-4 border border-slate-800">
          <div className="flex items-center justify-between text-xs mb-2">
            <span className="font-semibold text-slate-200">DSO Collection Acceleration</span>
            <span className="font-bold text-purple-400">{Math.abs(dsoDelta)} Days Faster</span>
          </div>
          <input
            type="range"
            min="-35"
            max="0"
            step="5"
            value={dsoDelta}
            onChange={(e) => setDsoDelta(Number(e.target.value))}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-purple-400"
          />
          <div className="mt-2 flex items-center justify-between text-[11px] text-slate-400">
            <span>Base: {baseDSO.toFixed(0)}d</span>
            <span>Target: {Math.max(20, baseDSO + dsoDelta).toFixed(0)}d</span>
          </div>
        </div>

        {/* Lever 3: Debt De-leveraging */}
        <div className="rounded-xl bg-slate-900/60 p-4 border border-slate-800">
          <div className="flex items-center justify-between text-xs mb-2">
            <span className="font-semibold text-slate-200">Short-Term Debt Reduction</span>
            <span className="font-bold text-emerald-400">{debtPaydownPct}% Paydown</span>
          </div>
          <input
            type="range"
            min="0"
            max="50"
            step="5"
            value={debtPaydownPct}
            onChange={(e) => setDebtPaydownPct(Number(e.target.value))}
            className="w-full h-1.5 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-emerald-400"
          />
          <div className="mt-2 flex items-center justify-between text-[11px] text-slate-400">
            <span>Base D/E: {baseDE.toFixed(2)}x</span>
            <span>Target D/E: {(baseDE * (1 - debtPaydownPct / 100)).toFixed(2)}x</span>
          </div>
        </div>

      </div>

      {/* Projected Benefits Impact Banner */}
      <div className="mt-6 rounded-xl bg-gradient-to-r from-slate-900 to-slate-950 p-4 border border-emerald-500/20 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <Sparkles className="h-5 w-5 text-emerald-400 shrink-0" />
          <div>
            <h4 className="text-xs font-semibold text-emerald-300">Projected Credit Enhancement</h4>
            <p className="text-xs text-slate-300 mt-0.5">
              Achieving these targets moves company to <strong className="text-white">{newRiskBand}</strong> with estimated interest rate savings of <strong className="text-emerald-400">~{estInterestDiscount}% p.a.</strong>
            </p>
          </div>
        </div>

        <button
          onClick={() => { setMarginDelta(1.5); setDsoDelta(-15); setDebtPaydownPct(20); }}
          className="rounded-lg bg-slate-800 px-3 py-1.5 text-xs text-slate-300 hover:text-white border border-slate-700 transition-all shrink-0"
        >
          Reset Simulation
        </button>
      </div>

    </div>
  );
};
