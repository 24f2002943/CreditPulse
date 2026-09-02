import React from 'react';
import { LucideIcon } from 'lucide-react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  change?: string;
  changeType?: 'positive' | 'negative' | 'neutral';
  icon: LucideIcon;
  iconColor?: string;
  glowColor?: 'blue' | 'emerald' | 'amber' | 'rose' | 'purple';
}

export const MetricCard: React.FC<MetricCardProps> = ({
  title,
  value,
  subtitle,
  change,
  changeType = 'neutral',
  icon: Icon,
  iconColor = 'text-blue-400',
  glowColor = 'blue',
}) => {
  const glowStyles = {
    blue: 'hover:shadow-glow-blue hover:border-blue-500/30',
    emerald: 'hover:shadow-glow-emerald hover:border-emerald-500/30',
    amber: 'hover:shadow-glow-amber hover:border-amber-500/30',
    rose: 'hover:shadow-glow-rose hover:border-rose-500/30',
    purple: 'hover:shadow-glow-blue hover:border-purple-500/30',
  }[glowColor];

  const changeBadgeStyles = {
    positive: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
    negative: 'text-rose-400 bg-rose-500/10 border-rose-500/20',
    neutral: 'text-slate-400 bg-slate-800/40 border-slate-700/40',
  }[changeType];

  return (
    <div className={`glass-panel glass-panel-hover rounded-2xl p-5 transition-all duration-300 ${glowStyles}`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-slate-400">{title}</p>
          <h3 className="mt-2 text-2xl font-bold tracking-tight text-white">{value}</h3>
        </div>
        <div className={`rounded-xl bg-slate-900/80 p-3 border border-slate-800 ${iconColor}`}>
          <Icon className="h-5 w-5" />
        </div>
      </div>
      
      {(subtitle || change) && (
        <div className="mt-4 flex items-center gap-2 text-xs">
          {change && (
            <span className={`inline-flex items-center rounded-md border px-2 py-0.5 font-medium ${changeBadgeStyles}`}>
              {change}
            </span>
          )}
          {subtitle && <span className="text-slate-400 truncate">{subtitle}</span>}
        </div>
      )}
    </div>
  );
};
