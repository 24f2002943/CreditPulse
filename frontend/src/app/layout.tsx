import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'CreditPulse — Relationship-Aware Financial Health & Credit Risk Platform for MSMEs',
  description: 'A platform computing MSME financial health and credit risk scores by fusing traditional financial ratios, sector elasticity, and NLP negotiation signals with SHAP explainability.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#090D16] text-slate-100 min-h-screen">
        {children}
      </body>
    </html>
  );
}
