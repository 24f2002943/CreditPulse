'use client';

import React, { useState } from 'react';
import { FinancialRatios, RatioBenchmark } from '../types';
import { CheckCircle2, AlertTriangle, XCircle, TrendingUp, DollarSign, Scale, Clock } from 'lucide-react';

interface FinancialRatiosGridProps {
  ratios: FinancialRatios;
  benchmarks: RatioBenchmark[];
}

export const FinancialRatiosGrid: React.FC<FinancialRatiosGridProps> = ({ ratios, benchmarks }) => {
  const [activeTab, setActiveTab] = useState<'all' | 'liquidity' | 'solvency' | 'profitability' | 'efficiency'>('all');

  const getStatusBadge = (status: 'healthy' | 'warning' | 'critical') => {
    if (status === 'healthy') {
      return (
        <span className="inline-flex items-center gap-1 rounded-full bg-emerald-500/10 px-2 py-0.5 text-[10px] font-semibold text-emerald-400 border border-emerald-500/20">
          <CheckCircle2 className="h-3 w-3" /> Healthy
        </span>
      );
    }
    if (status === 'warning') {
      return (
        <span className="inline-flex items-center gap-1 rounded-full bg-amber-500/10 px-2 py-0.5 text-[10px] font-semibold text-amber-400 border border-amber-500/20">
          <AlertTriangle className="h-3 w-3" /> Warning
        </span>
      );
    }
    return (
      <span className="inline-flex items-center gap-1 rounded-full bg-rose-500/10 px-2 py-0.5 text-[10px] font-semibold text-rose-400 border border-rose-500/20">
        <XCircle className="h-3 w-3" /> Critical
      </span>
    );
  };

  const ratioCards = [
    {
      category: 'liquidity',
      name: 'Current Ratio',
      value: ratios.current_ratio ? `${ratios.current_ratio.toFixed(2)}x` : 'N/A',
      benchmark: benchmarks.find((b) => b.key === 'current_ratio'),
      description: 'Current Assets / Current Liabilities',
      ideal: '> 1.50x'
    },
    {
      category: 'liquidity',
      name: 'Quick Ratio',
      value: ratios.quick_ratio ? `${ratios.quick_ratio.toFixed(2)}x` : 'N/A',
      benchmark: benchmarks.find((b) => b.key === 'quick_ratio'),
      description: '(Current Assets - Inventory) / Liabilities',
      ideal: '> 1.00x'
    },
    {
      category: 'liquidity',
      name: 'Working Capital',
      value: ratios.working_capital ? `$${(ratios.working_capital / 1000).toFixed(0)}k` : 'N/A',
      description: 'Net Short-Term Capital Buffer',
      ideal: 'Positive'
    },
    {
      category: 'solvency',
      name: 'Debt-to-Equity',
      value: ratios.debt_to_equity ? `${ratios.debt_to_equity.toFixed(2)}x` : 'N/A',
      benchmark: benchmarks.find((b) => b.key === 'debt_to_equity'),
      description: 'Total Debt / Shareholders Net Worth',
      ideal: '< 1.50x'
    },
    {
      category: 'solvency',
      name: 'Interest Coverage',
      value: ratios.interest_coverage_ratio ? `${ratios.interest_coverage_ratio.toFixed(1)}x` : 'N/A',
      description: 'EBIT / Finance Cost',
      ideal: '> 3.0x'
    },
    {
      category: 'profitability',
      name: 'Gross Margin',
      value: ratios.gross_margin ? `${(ratios.gross_margin * 100).toFixed(1)}%` : 'N/A',
      benchmark: benchmarks.find((b) => b.key === 'gross_margin'),
      description: 'Gross Profit / Revenue',
      ideal: 'Sector Avg'
    },
    {
      category: 'profitability',
      name: 'Net Profit Margin',
      value: ratios.net_margin ? `${(ratios.net_margin * 100).toFixed(1)}%` : 'N/A',
      benchmark: benchmarks.find((b) => b.key === 'net_margin'),
      description: 'Net Income / Revenue',
      ideal: '> 5.0%'
    },
    {
      category: 'profitability',
      name: 'Return on Equity (ROE)',
      value: ratios.roe ? `${(ratios.roe * 100).toFixed(1)}%` : 'N/A',
      description: 'Net Profit / Net Worth',
      ideal: '> 15.0%'
    },
    {
      category: 'efficiency',
      name: 'Days Sales Outstanding (DSO)',
      value: ratios.dso_days ? `${ratios.dso_days.toFixed(0)} days` : 'N/A',
      benchmark: benchmarks.find((b) => b.key === 'dso_days'),
      description: 'Debtor Cash Conversion Cycle',
      ideal: '< 60 days'
    },
    {
      category: 'efficiency',
      name: 'Inventory Turnover',
      value: ratios.inventory_turnover ? `${ratios.inventory_turnover.toFixed(1)}x` : 'N/A',
      description: 'COGS / Inventory',
      ideal: '> 4.0x'
    },
  ];

  const filteredCards = activeTab === 'all' 
    ? ratioCards 
    : ratioCards.filter((card) => card.category === activeTab);

  return (
    <div className="glass-panel rounded-2xl p-6 border border-slate-800 transition-all">
      
      {/* Header & Tabs */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-800 pb-4 gap-3">
        <div>
          <h3 className="text-lg font-bold text-white">Financial Statement Ratio Analysis</h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Auto-computed liquidity, solvency, leverage, and profitability ratios benchmarked to sector peers.
          </p>
        </div>

        {/* Category Tabs */}
        <div className="flex flex-wrap items-center gap-1.5 bg-slate-900/80 p-1 rounded-xl border border-slate-800">
          {(['all', 'liquidity', 'solvency', 'profitability', 'efficiency'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`rounded-lg px-2.5 py-1 text-xs font-medium capitalize transition-all ${
                activeTab === tab 
                  ? 'bg-blue-600 text-white shadow-sm' 
                  : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* Ratios Grid */}
      <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
        {filteredCards.map((card, idx) => (
          <div
            key={idx}
            className="rounded-xl bg-slate-900/60 p-4 border border-slate-800 hover:border-slate-700 transition-all flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-2">
                <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">{card.name}</span>
                {card.benchmark && getStatusBadge(card.benchmark.status)}
              </div>
              <div className="text-xl font-extrabold text-white tracking-tight">{card.value}</div>
              <p className="text-[11px] text-slate-400 mt-1 leading-snug">{card.description}</p>
            </div>

            {card.benchmark && (
              <div className="mt-3 pt-2 border-t border-slate-800/80 flex items-center justify-between text-[11px]">
                <span className="text-slate-400">Sector Median:</span>
                <span className="font-semibold text-slate-300">
                  {typeof card.benchmark.sector_median === 'number' && card.benchmark.sector_median < 1 && card.benchmark.sector_median > 0
                    ? `${(card.benchmark.sector_median * 100).toFixed(1)}%`
                    : `${card.benchmark.sector_median}`}
                </span>
              </div>
            )}
          </div>
        ))}
      </div>

    </div>
  );
};
