'use client';

import React from 'react';
import { ShapExplanation } from '../types';
import { HelpCircle, ArrowUpRight, ArrowDownRight, Minus } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell, ReferenceLine } from 'recharts';

interface ShapContributionChartProps {
  explanations: ShapExplanation[];
}

export const ShapContributionChart: React.FC<ShapContributionChartProps> = ({ explanations }) => {
  // Format for Recharts
  const chartData = explanations.slice(0, 8).map((exp) => ({
    name: exp.feature_name_display.split('(')[0].trim(),
    fullName: exp.feature_name_display,
    value: exp.value,
    shapValue: exp.shap_value,
    impactDirection: exp.impact_direction,
    effectLabel: exp.effect_label,
  }));

  const CustomTooltip = ({ active, payload }: any) => {
    if (active && payload && payload.length) {
      const data = payload[0].payload;
      const isProtective = data.shapValue < 0;
      return (
        <div className="rounded-xl bg-slate-900/95 p-3.5 border border-slate-700 shadow-xl text-xs backdrop-blur-md max-w-xs">
          <p className="font-bold text-white mb-1">{data.fullName}</p>
          <div className="flex items-center justify-between text-slate-300 mb-1">
            <span>Observed Value:</span>
            <span className="font-semibold text-white">{data.value}</span>
          </div>
          <div className="flex items-center justify-between text-slate-300 mb-2">
            <span>SHAP Impact Contribution:</span>
            <span className={`font-semibold ${isProtective ? 'text-emerald-400' : 'text-rose-400'}`}>
              {data.shapValue > 0 ? `+${data.shapValue.toFixed(4)}` : data.shapValue.toFixed(4)}
            </span>
          </div>
          <p className="text-[11px] text-slate-400 border-t border-slate-800 pt-1.5 leading-relaxed">
            {isProtective 
              ? 'Negative SHAP value reduces predicted default log-odds, protecting credit health.' 
              : 'Positive SHAP value increases predicted default log-odds, adding to risk.'}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="glass-panel rounded-2xl p-6 border border-slate-800 transition-all">
      
      {/* Header */}
      <div className="flex items-start justify-between border-b border-slate-800 pb-4">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-lg font-bold text-white">Explainable AI: SHAP Feature Contributions</h3>
            <span className="rounded-md bg-blue-500/10 px-2 py-0.5 text-[10px] font-semibold text-blue-400 border border-blue-500/20">
              Auditability
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Exact per-feature impact weights driving the ML default risk prediction. Green bars lower risk; red bars elevate risk.
          </p>
        </div>
        
        {/* Legend */}
        <div className="hidden sm:flex items-center gap-3 text-xs">
          <div className="flex items-center gap-1.5">
            <span className="h-3 w-3 rounded-sm bg-emerald-500"></span>
            <span className="text-slate-300">Lowers Risk</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="h-3 w-3 rounded-sm bg-rose-500"></span>
            <span className="text-slate-300">Elevates Risk</span>
          </div>
        </div>
      </div>

      {/* Bar Chart Visualization */}
      <div className="mt-6 h-64 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
            <XAxis type="number" stroke="#64748B" fontSize={11} tickFormatter={(val) => val.toFixed(2)} />
            <YAxis type="category" dataKey="name" stroke="#94A3B8" fontSize={11} width={130} />
            <Tooltip content={<CustomTooltip />} />
            <ReferenceLine x={0} stroke="#334155" strokeWidth={1.5} />
            <Bar dataKey="shapValue" radius={[4, 4, 4, 4]}>
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={entry.shapValue < 0 ? '#10B981' : '#F43F5E'}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Feature Breakdown Grid */}
      <div className="mt-6 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
        {explanations.slice(0, 6).map((exp, idx) => {
          const isProtective = exp.impact_direction === 'decreases_risk';
          const isNeutral = exp.impact_direction === 'neutral';
          return (
            <div key={idx} className="rounded-xl bg-slate-900/70 p-3 border border-slate-800 text-xs">
              <div className="flex items-center justify-between mb-1">
                <span className="font-semibold text-slate-200 truncate pr-2" title={exp.feature_name_display}>
                  {exp.feature_name_display.split('(')[0].trim()}
                </span>
                <span className="font-mono font-bold text-slate-300">
                  {typeof exp.value === 'number' && exp.value > 100 ? exp.value.toLocaleString() : exp.value}
                </span>
              </div>
              <div className="flex items-center justify-between pt-1 border-t border-slate-800/80">
                <span className="text-[11px] text-slate-400">SHAP: {exp.shap_value > 0 ? `+${exp.shap_value.toFixed(3)}` : exp.shap_value.toFixed(3)}</span>
                <span className={`inline-flex items-center gap-1 font-medium text-[11px] ${
                  isProtective ? 'text-emerald-400' : (isNeutral ? 'text-slate-400' : 'text-rose-400')
                }`}>
                  {isProtective ? <ArrowDownRight className="h-3 w-3" /> : (isNeutral ? <Minus className="h-3 w-3" /> : <ArrowUpRight className="h-3 w-3" />)}
                  {exp.effect_label}
                </span>
              </div>
            </div>
          );
        })}
      </div>

    </div>
  );
};
