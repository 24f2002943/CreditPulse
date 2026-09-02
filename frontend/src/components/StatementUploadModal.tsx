'use client';

import React, { useState } from 'react';
import { X, UploadCloud, FileSpreadsheet, FileText, CheckCircle2, AlertTriangle, Loader2 } from 'lucide-react';
import { uploadFinancialStatement } from '../services/api';

interface StatementUploadModalProps {
  isOpen: boolean;
  onClose: () => void;
  companies: { id: number; name: string }[];
  onUploadSuccess: (companyId: number) => void;
}

export const StatementUploadModal: React.FC<StatementUploadModalProps> = ({
  isOpen,
  onClose,
  companies,
  onUploadSuccess,
}) => {
  const [selectedCompanyId, setSelectedCompanyId] = useState<number>(companies[0]?.id || 1);
  const [fiscalYear, setFiscalYear] = useState<number>(2024);
  const [file, setFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadResult, setUploadResult] = useState<any>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  if (!isOpen) return null;

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setErrorMsg(null);
      setUploadResult(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) {
      setErrorMsg('Please select an Excel, CSV, or PDF file to upload.');
      return;
    }

    setIsUploading(true);
    setErrorMsg(null);

    const formData = new FormData();
    formData.append('company_id', selectedCompanyId.toString());
    formData.append('fiscal_year', fiscalYear.toString());
    formData.append('statement_type', 'combined');
    formData.append('file', file);

    try {
      const res = await uploadFinancialStatement(formData);
      setUploadResult(res);
      setIsUploading(false);
      onUploadSuccess(selectedCompanyId);
    } catch (err: any) {
      setIsUploading(false);
      setErrorMsg(err.message || 'Upload and parsing failed. Please check file formatting.');
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
      <div className="glass-panel w-full max-w-lg rounded-2xl border border-slate-700 bg-slate-950/95 p-6 shadow-2xl">
        
        {/* Modal Header */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-blue-500/10 text-blue-400 border border-blue-500/20">
              <UploadCloud className="h-4 w-4" />
            </div>
            <div>
              <h3 className="text-base font-bold text-white">Upload Financial Statement</h3>
              <p className="text-[11px] text-slate-400">Excel (.xlsx, .csv) & Scanned PDF OCR Ingestion</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="rounded-lg p-1.5 text-slate-400 hover:bg-slate-800 hover:text-white transition-all"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Modal Form */}
        <form onSubmit={handleSubmit} className="mt-5 space-y-4">
          
          {/* Company Selector */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
              Select MSME Entity
            </label>
            <select
              value={selectedCompanyId}
              onChange={(e) => setSelectedCompanyId(Number(e.target.value))}
              className="w-full rounded-xl bg-slate-900 border border-slate-700 px-3.5 py-2.5 text-xs text-white focus:border-blue-500 focus:outline-none"
            >
              {companies.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.name}
                </option>
              ))}
            </select>
          </div>

          {/* Fiscal Year */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
              Fiscal Year
            </label>
            <input
              type="number"
              value={fiscalYear}
              onChange={(e) => setFiscalYear(Number(e.target.value))}
              className="w-full rounded-xl bg-slate-900 border border-slate-700 px-3.5 py-2.5 text-xs text-white focus:border-blue-500 focus:outline-none"
            />
          </div>

          {/* File Drag and Drop / Input */}
          <div>
            <label className="block text-xs font-semibold uppercase tracking-wider text-slate-400 mb-1.5">
              Financial Document File
            </label>
            <div className="relative flex flex-col items-center justify-center rounded-xl border-2 border-dashed border-slate-700 bg-slate-900/50 p-6 text-center hover:border-blue-500/50 transition-all">
              <input
                type="file"
                accept=".xlsx,.xls,.csv,.pdf"
                onChange={handleFileChange}
                className="absolute inset-0 cursor-pointer opacity-0"
              />
              <div className="flex gap-2 mb-2 text-slate-400">
                <FileSpreadsheet className="h-6 w-6 text-emerald-400" />
                <FileText className="h-6 w-6 text-cyan-400" />
              </div>
              <p className="text-xs font-medium text-slate-200">
                {file ? file.name : 'Click or drag & drop balance sheet / P&L here'}
              </p>
              <p className="text-[11px] text-slate-400 mt-1">Supports Excel workbooks, CSV books, or PDF scanned statements</p>
            </div>
          </div>

          {/* Error Notice */}
          {errorMsg && (
            <div className="rounded-xl bg-rose-500/10 p-3 border border-rose-500/30 text-xs text-rose-300 flex items-center gap-2">
              <AlertTriangle className="h-4 w-4 shrink-0" />
              <span>{errorMsg}</span>
            </div>
          )}

          {/* Upload Result / Validation Box */}
          {uploadResult && (
            <div className="rounded-xl bg-emerald-500/10 p-3.5 border border-emerald-500/30 text-xs text-emerald-200 space-y-1">
              <div className="flex items-center gap-1.5 font-bold">
                <CheckCircle2 className="h-4 w-4 text-emerald-400" />
                <span>Extracted {uploadResult.line_items_count} Financial Line Items</span>
              </div>
              <p className="text-[11px] text-emerald-300">
                Accounting Equation Balance: {uploadResult.validation?.accounting_equation_balanced ? 'Verified (Assets = Liabilities + Equity)' : 'Discrepancy Detected'}
              </p>
            </div>
          )}

          {/* Action Buttons */}
          <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              className="rounded-xl px-4 py-2 text-xs font-medium text-slate-400 hover:text-white transition-all"
            >
              Close
            </button>
            <button
              type="submit"
              disabled={isUploading}
              className="flex items-center gap-2 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 px-5 py-2 text-xs font-semibold text-white shadow-glow-blue hover:from-blue-500 hover:to-cyan-400 disabled:opacity-50 transition-all"
            >
              {isUploading ? (
                <>
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span>Processing OCR & Parser...</span>
                </>
              ) : (
                <span>Ingest & Run Risk Models</span>
              )}
            </button>
          </div>

        </form>

      </div>
    </div>
  );
};
