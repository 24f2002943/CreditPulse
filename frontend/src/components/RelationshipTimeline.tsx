'use client';

import React from 'react';
import { RelationshipSummary, InteractionLog } from '../types';
import { MessageSquareText, ShieldAlert, CheckCircle2, RefreshCw, Calendar, Tag } from 'lucide-react';

interface RelationshipTimelineProps {
  summary: RelationshipSummary;
  history: InteractionLog[];
}

export const RelationshipTimeline: React.FC<RelationshipTimelineProps> = ({ summary, history }) => {
  const {
    relationship_score,
    relationship_band,
    total_interactions,
    failure_count,
    recovery_count,
    key_findings
  } = summary;

  const isStrong = relationship_score >= 75;

  return (
    <div className="glass-panel rounded-2xl p-6 border border-slate-800 transition-all">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-800 pb-4 gap-3">
        <div>
          <div className="flex items-center gap-2">
            <h3 className="text-lg font-bold text-white">Unstructured NLP: B2B Relationship & Service History</h3>
            <span className="rounded-md bg-cyan-500/10 px-2 py-0.5 text-[10px] font-semibold text-cyan-400 border border-cyan-500/20">
              Alternative Signal
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-0.5">
            NLP sentiment, commercial negotiation friction, and service failure recovery timeline.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="text-right">
            <span className="text-[10px] uppercase tracking-wider text-slate-400">Relationship Score</span>
            <div className={`text-base font-extrabold ${isStrong ? 'text-emerald-400' : 'text-amber-400'}`}>
              {relationship_score} / 100
            </div>
          </div>
          <div className="rounded-xl bg-slate-900 px-3 py-2 border border-slate-800 text-xs text-slate-300">
            {recovery_count}/{failure_count} Recovered
          </div>
        </div>
      </div>

      {/* Key Findings Bulletins */}
      {key_findings && key_findings.length > 0 && (
        <div className="mt-4 rounded-xl bg-slate-900/60 p-3.5 border border-slate-800/80">
          <span className="text-[11px] font-semibold uppercase tracking-wider text-slate-400">Behavioral Insights</span>
          <ul className="mt-1.5 space-y-1 text-xs text-slate-300">
            {key_findings.map((f, idx) => (
              <li key={idx} className="flex items-center gap-2">
                <span className="h-1.5 w-1.5 rounded-full bg-cyan-400"></span>
                <span>{f}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Interactive Timeline */}
      <div className="mt-6 space-y-4">
        {history.map((item, idx) => {
          const isNegotiation = item.interaction_type === 'negotiation';
          const isFailure = item.interaction_type === 'service_failure';
          const isRecovery = item.interaction_type === 'service_recovery';

          const borderCol = isFailure ? 'border-rose-500/30 bg-rose-500/5' : (isRecovery ? 'border-emerald-500/30 bg-emerald-500/5' : 'border-blue-500/30 bg-blue-500/5');
          const badgeText = isFailure ? 'Service Failure' : (isRecovery ? 'Service Recovery' : 'Negotiation / Commercial');
          const badgeStyle = isFailure ? 'text-rose-400 bg-rose-500/10' : (isRecovery ? 'text-emerald-400 bg-emerald-500/10' : 'text-blue-400 bg-blue-500/10');

          return (
            <div key={idx} className={`relative rounded-xl p-4 border ${borderCol} transition-all`}>
              <div className="flex items-center justify-between mb-2">
                <div className="flex items-center gap-2">
                  <span className={`rounded-md px-2 py-0.5 text-[10px] font-bold uppercase tracking-wider ${badgeStyle}`}>
                    {badgeText}
                  </span>
                  {item.date && (
                    <span className="flex items-center gap-1 text-[11px] text-slate-400">
                      <Calendar className="h-3 w-3" />
                      {item.date}
                    </span>
                  )}
                </div>

                {item.sentiment_score !== undefined && (
                  <div className="flex items-center gap-2 text-[11px]">
                    <span className="text-slate-400">Sentiment:</span>
                    <span className={`font-semibold ${item.sentiment_score > 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                      {item.sentiment_score > 0 ? `+${item.sentiment_score}` : item.sentiment_score}
                    </span>
                  </div>
                )}
              </div>

              <p className="text-xs text-slate-200 leading-relaxed italic">
                "{item.transcript_text}"
              </p>
            </div>
          );
        })}
      </div>

    </div>
  );
};
