'use client';

import React from 'react';
import { CostStructure } from '../types';
import { Layers, ShieldAlert, CheckCircle, PieChart } from 'lucide-react';

interface CostStructureCardProps {
  costData: CostStructure;
}

export const CostStructureCard: React.FC<CostStructureCardProps> = ({ costData }) => {
  const {
    variable_costs,
    fixed_costs,
    contribution_margin,
    contribution_margin_ratio,
    break_even_revenue,
    margin_of_safety_pct,
    operating_leverage,
    vulnerability_tier
  } = costData;

  const totalCosts = variable_costs + fixed_costs;
  const variablePct = totalCosts > 0 ? (variable_costs / totalCosts) * 100 : 70;
  const fixedPct = totalCosts > 0 ? (fixed_costs / totalCosts) * 100 : 30;

  const isSafe = margin_of_safety_pct > 25.0;

  return (
    <div className="glass-panel rounded-2xl p-6 border border-slate-800 transition-all">
      
      {/* Header */}
      <div className="flex items-start justify-between border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-lg font-bold text-white">Cost Structure & Operating Leverage</h3>
            <span className="rounded-md bg-purple-500/10 px-2 py-0.5 text-[10px] font-semibold text-purple-400 border border-purple-500/20">
              Sensitivity
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            Fixed vs. variable cost classification and break-even vulnerability analysis.
          </p>
        </div>

        <div className={`flex items-center gap-1.5 rounded-full px-3 py-1 text-xs font-semibold border ${
          isSafe ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30' : 'bg-rose-500/10 text-rose-400 border-rose-500/30'
        }`}>
          {isSafe ? <CheckCircle className="h-3.5 w-3.5" /> : <ShieldAlert className="h-3.5 w-3.5" />}
          <span>{isSafe ? 'Resilient Cost Base' : 'Fixed Cost Heavy'}</span>
        </div>
      </div>

      {/* Cost Distribution Bar */}
      <div className="mt-6">
        <div className="flex items-center justify-between text-xs mb-2">
          <span className="text-slate-300 font-medium flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-sm bg-cyan-500"></span>
            Variable Costs ({variablePct.toFixed(1)}%) — ${(variable_costs / 1000).toFixed(0)}k
          </span>
          <span className="text-slate-300 font-medium flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-sm bg-purple-500"></span>
            Fixed Overheads ({fixedPct.toFixed(1)}%) — ${(fixed_costs / 1000).toFixed(0)}k
          </span>
        </div>

        <div className="h-3.5 w-full rounded-full bg-slate-800 overflow-hidden flex">
          <div className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 transition-all" style={{ width: `${variablePct}%` }} />
          <div className="h-full bg-gradient-to-r from-purple-500 to-indigo-500 transition-all" style={{ width: `${fixedPct}%` }} />
        </div>
      </div>

      {/* Break-Even & Metrics Grid */}
      <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-4">
        
        <div className="rounded-xl bg-slate-900/70 p-3.5 border border-slate-800">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Contribution Margin</span>
          <div className="text-xl font-bold text-white mt-1">{(contribution_margin_ratio * 100).toFixed(1)}%</div>
          <span className="text-[11px] text-slate-400">${(contribution_margin / 1000).toFixed(0)}k gross contribution</span>
        </div>

        <div className="rounded-xl bg-slate-900/70 p-3.5 border border-slate-800">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Break-Even Revenue</span>
          <div className="text-xl font-bold text-white mt-1">${(break_even_revenue / 1000).toFixed(0)}k</div>
          <span className="text-[11px] text-slate-400">Minimum turnover needed</span>
        </div>

        <div className="rounded-xl bg-slate-900/70 p-3.5 border border-slate-800">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Margin of Safety</span>
          <div className={`text-xl font-bold mt-1 ${margin_of_safety_pct > 20 ? 'text-emerald-400' : 'text-amber-400'}`}>
            {margin_of_safety_pct.toFixed(1)}%
          </div>
          <span className="text-[11px] text-slate-400">Buffer before net loss</span>
        </div>

        <div className="rounded-xl bg-slate-900/70 p-3.5 border border-slate-800">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Operating Leverage (DOL)</span>
          <div className="text-xl font-bold text-white mt-1">{operating_leverage.toFixed(2)}x</div>
          <span className="text-[11px] text-slate-400">EBIT sensitivity to revenue</span>
        </div>

      </div>

    </div>
  );
};
