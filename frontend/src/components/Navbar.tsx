'use client';

import React from 'react';
import { Activity, ShieldCheck, Building2, Layers, UploadCloud, UserCircle2 } from 'lucide-react';

interface NavbarProps {
  currentRole: 'lender' | 'msme_owner';
  onRoleChange: (role: 'lender' | 'msme_owner') => void;
  onOpenUpload: () => void;
  selectedCompanyName?: string;
}

export const Navbar: React.FC<NavbarProps> = ({
  currentRole,
  onRoleChange,
  onOpenUpload,
  selectedCompanyName,
}) => {
  return (
    <header className="sticky top-0 z-40 w-full border-b border-slate-800 bg-[#090D16]/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        
        {/* Brand Logo & Tagline */}
        <div className="flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-400 text-white shadow-glow-blue">
            <Activity className="h-6 w-6 animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xl font-bold tracking-tight text-white">CreditPulse</span>
              <span className="rounded-full bg-blue-500/10 px-2 py-0.5 text-xs font-semibold text-blue-400 border border-blue-500/20">
                v1.0 AI
              </span>
            </div>
            <p className="text-[11px] text-slate-400">Relationship-Aware MSME Credit Risk Platform</p>
          </div>
        </div>

        {/* Action Controls & Role Switcher */}
        <div className="flex items-center gap-4">
          
          {/* Upload Button */}
          <button
            onClick={onOpenUpload}
            className="flex items-center gap-2 rounded-lg bg-slate-850 px-3.5 py-2 text-xs font-medium text-slate-200 border border-slate-700 hover:border-blue-500/50 hover:bg-slate-800 transition-all shadow-sm"
          >
            <UploadCloud className="h-4 w-4 text-cyan-400" />
            <span>Upload Financials (OCR/Excel)</span>
          </button>

          {/* Role Toggle Switcher */}
          <div className="flex items-center rounded-xl bg-slate-900 p-1 border border-slate-800">
            <button
              onClick={() => onRoleChange('lender')}
              className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-medium transition-all ${
                currentRole === 'lender'
                  ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <ShieldCheck className="h-3.5 w-3.5" />
              <span>Lender Analyst</span>
            </button>
            <button
              onClick={() => onRoleChange('msme_owner')}
              className={`flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-medium transition-all ${
                currentRole === 'msme_owner'
                  ? 'bg-gradient-to-r from-emerald-600 to-teal-600 text-white shadow-sm'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              <Building2 className="h-3.5 w-3.5" />
              <span>MSME Health Portal</span>
            </button>
          </div>

          {/* Profile Badge */}
          <div className="hidden sm:flex items-center gap-2 pl-2 border-l border-slate-800 text-xs text-slate-400">
            <UserCircle2 className="h-5 w-5 text-slate-500" />
            <span className="truncate max-w-[130px]">
              {currentRole === 'lender' ? 'analyst@bank.com' : 'owner@apex.com'}
            </span>
          </div>

        </div>

      </div>
    </header>
  );
};
