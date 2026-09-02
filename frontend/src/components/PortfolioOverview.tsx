'use client';

import React from 'react';
import { PortfolioOverviewData, Company } from '../types';
import { Building, ShieldCheck, AlertTriangle, Users, TrendingUp, Filter, Search } from 'lucide-react';
import { MetricCard } from './MetricCard';

interface PortfolioOverviewProps {
  overview: PortfolioOverviewData;
  companies: Company[];
  selectedCompanyId: number;
  onSelectCompany: (id: number) => void;
  selectedSector: string;
  onSelectSector: (sector: string) => void;
  searchQuery: string;
  onSearchChange: (query: string) => void;
}

export const PortfolioOverview: React.FC<PortfolioOverviewProps> = ({
  overview,
  companies,
  selectedCompanyId,
  onSelectCompany,
  selectedSector,
  onSelectSector,
  searchQuery,
  onSearchChange,
}) => {
  const sectors = ['all', ...Array.from(new Set(companies.map((c) => c.sector)))];

  const filteredCompanies = companies.filter((c) => {
    const matchesSector = selectedSector === 'all' || c.sector === selectedSector;
    const matchesSearch = c.name.toLowerCase().includes(searchQuery.toLowerCase()) || c.sector.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesSector && matchesSearch;
  });

  return (
    <div className="space-y-6">
      
      {/* Top Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <MetricCard
          title="Assessed MSME Entities"
          value={overview.total_assessed_companies}
          subtitle="Portfolio active borrowers"
          change="+3 this month"
          changeType="positive"
          icon={Building}
          iconColor="text-blue-400"
          glowColor="blue"
        />

        <MetricCard
          title="Avg Portfolio Score"
          value={`${overview.average_portfolio_score} / 100`}
          subtitle="Investment grade baseline"
          change="Grade B Average"
          changeType="neutral"
          icon={ShieldCheck}
          iconColor="text-emerald-400"
          glowColor="emerald"
        />

        <MetricCard
          title="Est. Approval Rate"
          value={`${overview.approval_rate_estimate}%`}
          subtitle="Automated underwriting pipeline"
          change="+5.2% YoY"
          changeType="positive"
          icon={TrendingUp}
          iconColor="text-cyan-400"
          glowColor="blue"
        />

        <MetricCard
          title="High Risk Watchlist"
          value={overview.risk_distribution.high_risk_count}
          subtitle="Requires collateral review"
          change="1 Active Breach"
          changeType="negative"
          icon={AlertTriangle}
          iconColor="text-rose-400"
          glowColor="rose"
        />
      </div>

      {/* Company Selector & Filter Bar */}
      <div className="glass-panel rounded-2xl p-5 border border-slate-800">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          
          {/* Search Input */}
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />
            <input
              type="text"
              placeholder="Search MSME company name or sector..."
              value={searchQuery}
              onChange={(e) => onSearchChange(e.target.value)}
              className="w-full rounded-xl bg-slate-900 border border-slate-700 pl-10 pr-4 py-2 text-xs text-white placeholder:text-slate-500 focus:border-blue-500 focus:outline-none"
            />
          </div>

          {/* Sector Pill Filters */}
          <div className="flex items-center gap-1.5 overflow-x-auto pb-1 max-w-full">
            {sectors.map((sec) => (
              <button
                key={sec}
                onClick={() => onSelectSector(sec)}
                className={`rounded-lg px-3 py-1.5 text-xs font-medium whitespace-nowrap transition-all ${
                  selectedSector === sec
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'bg-slate-900/80 text-slate-400 hover:text-white border border-slate-800'
                }`}
              >
                {sec === 'all' ? 'All Sectors' : sec}
              </button>
            ))}
          </div>

        </div>

        {/* Company Quick-Select Horizontal Cards */}
        <div className="mt-4 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-3">
          {filteredCompanies.map((c) => {
            const isSelected = c.id === selectedCompanyId;
            return (
              <button
                key={c.id}
                onClick={() => onSelectCompany(c.id)}
                className={`flex flex-col text-left rounded-xl p-3 border transition-all ${
                  isSelected
                    ? 'bg-blue-600/15 border-blue-500 shadow-glow-blue'
                    : 'bg-slate-900/60 border-slate-800 hover:border-slate-700 hover:bg-slate-900/90'
                }`}
              >
                <span className="font-semibold text-xs text-white truncate w-full">{c.name}</span>
                <span className="text-[11px] text-slate-400 mt-0.5 truncate">{c.sector}</span>
                <span className="mt-2 text-[10px] font-mono text-cyan-400">ID #{c.id}</span>
              </button>
            );
          })}
        </div>

      </div>

    </div>
  );
};
