"use client";
import { useState } from "react";
import { 
  Terminal, Code2, Layers, 
  Activity, DollarSign, ArrowRight,
  CheckCircle2, Cloud, Globe, ShieldAlert, 
  Building, CreditCard, Download, Copy, Check
} from "lucide-react";

const BACKEND_URL = "https://stratox.onrender.com";

export default function StratoxCommandCenter() {
  const [prompt, setPrompt] = useState("");
  const [analysisMode, setAnalysisMode] = useState("design"); 
  const [result, setResult] = useState<any>(null);
  const [totalMonitoredSpend, setTotalMonitoredSpend] = useState(0);
  const [totalSavings, setTotalSavings] = useState(0);
  const [loading, setLoading] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt) return;
    setLoading(true);
    setResult(null); 
    try {
        const res = await fetch(`${BACKEND_URL}/analyze-infrastructure`, {
          method: "POST", 
          headers: { "Content-Type": "application/json" }, 
          body: JSON.stringify({ prompt, analysis_mode: analysisMode }),
        });
        const data = await res.json();
        setResult(data);
        setTotalMonitoredSpend(prev => prev + (data.initial_cost || 0));
        setTotalSavings(prev => prev + (data.savings || 0));
    } catch (err) {
        console.error(err);
    }
    setLoading(false);
  };

  const getPlaceholder = () => {
    if (analysisMode === "iac_scan") return "Paste Terraform (.tf) or CloudFormation code here...";
    if (analysisMode === "zombie_hunter") return "Paste AWS CLI output or resource JSON export...";
    if (analysisMode === "multi_cloud") return "Describe your workload to compare costs across AWS, GCP, and Azure...";
    if (analysisMode === "security") return "Paste architecture specs or code to scan for IAM risks, open ports, and vulnerabilities...";
    return "Describe cloud architecture requirements (e.g., 'K8s backend for 100k users')...";
  };

  const handleCopy = () => {
    if (!result) return;
    navigator.clipboard.writeText(result.analysis_output);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    if (!result) return;
    const dateStr = new Date().toISOString().split('T')[0];
    const reportContent = `# Stratox FinOps Intelligence Report\n\n**Analysis Mode:** ${analysisMode.toUpperCase()}\n**Timestamp:** ${new Date().toLocaleString()}\n**Routing Node:** ${result.pillar_addressed}\n\n### FinOps Telemetry\n- **Initial Projected Cost:** $${result.initial_cost.toFixed(2)}/mo\n- **Optimized Cost:** $${result.optimized_cost.toFixed(2)}/mo\n- **Total Savings Realized:** $${result.savings.toFixed(2)}/mo\n\n---\n\n## Architecture & Remediation Details\n\n${result.analysis_output}`;
    const blob = new Blob([reportContent], { type: "text/markdown" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `Stratox-Report-${analysisMode}-${dateStr}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-[#0e0e11] text-[#a1a1aa] font-sans selection:bg-amber-500/20">
      
      <header className="h-16 border-b border-[#27272a] bg-[#0e0e11]/80 backdrop-blur-md flex items-center justify-between px-8 sticky top-0 z-50">
        <div className="flex items-center gap-3">
          <div className="bg-[#18181b] p-1.5 rounded-md border border-[#27272a] shadow-sm">
            <Cloud className="w-4 h-4 text-amber-500" />
          </div>
          <span className="font-semibold text-[15px] tracking-wide text-[#ededed]">Stratox</span>
          <div className="h-4 w-px bg-[#27272a] mx-3"></div>
          <span className="text-xs font-medium text-amber-500/90 flex items-center gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-amber-500 animate-pulse"></div> FinOps Engine Live
          </span>
        </div>
        <div className="flex items-center gap-3 cursor-pointer hover:bg-[#18181b] px-3 py-1.5 rounded-lg transition-colors border border-transparent hover:border-[#27272a]">
          <div className="text-right hidden md:block">
            <p className="text-[13px] font-medium text-[#ededed]">Production Org</p>
            <p className="text-[11px] text-[#71717a]">Admin Workspace</p>
          </div>
          <div className="w-8 h-8 rounded-md bg-[#18181b] border border-[#27272a] flex items-center justify-center shadow-inner">
            <Building className="w-4 h-4 text-amber-500/80" />
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto p-6 md:p-10 space-y-8">
        <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6 pb-8 border-b border-[#27272a]">
          <div>
            <h1 className="text-3xl font-semibold text-[#ededed] tracking-tight mb-2">Infrastructure Intelligence</h1>
            <p className="text-[15px] text-[#71717a]">Scan IaC, analyze cost leaks, compare cloud pricing, and enforce security.</p>
          </div>
          <div className="flex items-center gap-6 bg-[#18181b] px-6 py-4 rounded-xl border border-[#27272a] shadow-sm shrink-0 overflow-x-auto">
            <div>
              <p className="text-[11px] text-[#71717a] uppercase tracking-widest font-semibold mb-1.5">Monitored Spend</p>
              <p className="text-xl font-mono text-[#ededed] flex items-center gap-1.5 leading-none">
                <CreditCard className="w-4 h-4 text-[#71717a]"/>
                ${totalMonitoredSpend.toFixed(2)}
              </p>
            </div>
            <div className="w-px h-10 bg-[#27272a]"></div>
            <div>
              <p className="text-[11px] text-[#71717a] uppercase tracking-widest font-semibold mb-1.5">Total Savings</p>
              <p className="text-xl font-mono text-[#ededed] flex items-center gap-1.5 leading-none">
                <DollarSign className="w-4 h-4 text-amber-500"/>
                ${totalSavings.toFixed(2)}
              </p>
            </div>
            <div className="w-px h-10 bg-[#27272a]"></div>
            <div>
              <p className="text-[11px] text-[#71717a] uppercase tracking-widest font-semibold mb-1.5">Routing Node</p>
              <p className="text-[14px] font-medium text-[#ededed] flex items-center gap-2">
                <Activity className="w-3.5 h-3.5 text-amber-500"/>
                {result ? (result.status.includes("Failover") ? "HA Pool (1.5)" : "Premium (2.0)") : "Standby"}
              </p>
            </div>
          </div>
        </div>

        <div className="border border-[#27272a] bg-[#18181b] rounded-xl shadow-sm overflow-hidden">
          <div className="flex border-b border-[#27272a] bg-[#0e0e11]/50 px-2 pt-2 gap-2 overflow-x-auto custom-scrollbar">
            <button onClick={() => setAnalysisMode("design")} className={`flex shrink-0 items-center gap-2 px-4 py-2.5 text-[13px] font-medium transition-all rounded-t-lg ${analysisMode === "design" ? "text-[#ededed] bg-[#18181b] border-t border-l border-r border-[#27272a]" : "text-[#71717a] hover:text-[#a1a1aa] border-t border-l border-r border-transparent"}`}>
              <Layers className="w-4 h-4"/> Architecture
            </button>
            <button onClick={() => setAnalysisMode("iac_scan")} className={`flex shrink-0 items-center gap-2 px-4 py-2.5 text-[13px] font-medium transition-all rounded-t-lg ${analysisMode === "iac_scan" ? "text-[#ededed] bg-[#18181b] border-t border-l border-r border-[#27272a]" : "text-[#71717a] hover:text-[#a1a1aa] border-t border-l border-r border-transparent"}`}>
              <Code2 className="w-4 h-4"/> IaC Scan
            </button>
            <button onClick={() => setAnalysisMode("zombie_hunter")} className={`flex shrink-0 items-center gap-2 px-4 py-2.5 text-[13px] font-medium transition-all rounded-t-lg ${analysisMode === "zombie_hunter" ? "text-[#ededed] bg-[#18181b] border-t border-l border-r border-[#27272a]" : "text-[#71717a] hover:text-[#a1a1aa] border-t border-l border-r border-transparent"}`}>
              <Terminal className="w-4 h-4"/> Zombies
            </button>
            <button onClick={() => setAnalysisMode("multi_cloud")} className={`flex shrink-0 items-center gap-2 px-4 py-2.5 text-[13px] font-medium transition-all rounded-t-lg ${analysisMode === "multi_cloud" ? "text-[#ededed] bg-[#18181b] border-t border-l border-r border-[#27272a]" : "text-[#71717a] hover:text-[#a1a1aa] border-t border-l border-r border-transparent"}`}>
              <Globe className="w-4 h-4"/> Multi-Cloud Compare
            </button>
            <button onClick={() => setAnalysisMode("security")} className={`flex shrink-0 items-center gap-2 px-4 py-2.5 text-[13px] font-medium transition-all rounded-t-lg ${analysisMode === "security" ? "text-[#ededed] bg-[#18181b] border-t border-l border-r border-transparent" : "text-[#71717a] hover:text-[#a1a1aa] border-t border-l border-r border-transparent"}`}>
              <ShieldAlert className="w-4 h-4"/> Security Check
            </button>
          </div>

          <form onSubmit={handleSubmit} className="p-5">
            <textarea 
                value={prompt} 
                onChange={(e) => setPrompt(e.target.value)} 
                className="w-full h-36 bg-[#0e0e11] border border-[#27272a] rounded-lg px-4 py-3 text-[#ededed] focus:border-amber-500/50 focus:ring-1 focus:ring-amber-500/50 focus:outline-none resize-none font-mono text-[13px] placeholder:text-[#52525b] leading-relaxed transition-all shadow-inner" 
                placeholder={getPlaceholder()} 
            />
            <div className="flex justify-end mt-5">
              <button 
                  type="submit" 
                  disabled={loading || !prompt} 
                  className="bg-[#ededed] hover:bg-white text-[#0e0e11] px-6 py-2.5 rounded-lg font-semibold text-[13px] disabled:opacity-50 transition-colors flex items-center gap-2 shadow-sm"
              >
                  {loading ? (
                    <span className="flex items-center gap-2"><Activity className="w-4 h-4 animate-spin"/> Processing...</span>
                  ) : (
                    <span className="flex items-center gap-2">Execute Analysis <ArrowRight className="w-4 h-4"/></span>
                  )}
              </button>
            </div>
          </form>
        </div>

        {result && !loading && (
          <div className="border border-[#27272a] bg-[#18181b] rounded-xl overflow-hidden shadow-sm animate-in fade-in duration-500">
            <div className="bg-[#0e0e11]/50 px-5 py-3.5 border-b border-[#27272a] flex flex-col xl:flex-row justify-between items-start xl:items-center gap-4">
              <div className="flex items-center gap-2.5">
                <CheckCircle2 className="w-4 h-4 text-amber-500 shrink-0" />
                <span className="text-[13px] font-semibold text-[#ededed] tracking-wide truncate">Analysis Complete</span>
              </div>
              <div className="flex flex-wrap items-center gap-3 w-full xl:w-auto">
                <div className="flex items-center bg-[#0e0e11] border border-[#27272a] rounded-lg p-1 mr-2">
                  <span className="text-[12px] font-mono text-[#71717a] px-2" title="Initial Projected Cost">
                    Before: ${result.initial_cost.toFixed(2)}
                  </span>
                  {result.savings > 0 && (
                    <>
                      <ArrowRight className="w-3 h-3 text-[#52525b]" />
                      <span className="text-[12px] font-mono text-emerald-400 px-2" title="Cost after Stratox Optimization">
                        After: ${result.optimized_cost.toFixed(2)}
                      </span>
                      <div className="w-px h-4 bg-[#27272a] mx-1"></div>
                      <span className="text-[12px] font-mono font-medium text-[#0e0e11] bg-amber-500 px-2 py-0.5 rounded-md">
                        Saved: ${result.savings.toFixed(2)}
                      </span>
                    </>
                  )}
                </div>
                <button onClick={handleCopy} className="p-1.5 text-[#71717a] hover:text-[#ededed] bg-[#18181b] hover:bg-[#27272a] border border-[#27272a] rounded-md transition-colors flex items-center gap-1.5">
                  {copied ? <Check className="w-4 h-4 text-emerald-500" /> : <Copy className="w-4 h-4" />}
                  {copied && <span className="text-[11px] font-medium text-emerald-500">Copied!</span>}
                </button>
                <button onClick={handleDownload} className="flex items-center gap-1.5 px-3 py-1.5 text-[12px] font-medium text-[#ededed] bg-[#27272a] hover:bg-[#3f3f46] rounded-md transition-colors">
                  <Download className="w-3.5 h-3.5" /> Export
                </button>
              </div>
            </div>
            <div className="p-6 md:p-8 overflow-x-auto">
              <pre className="font-sans text-[14.5px] text-[#d4d4d8] leading-relaxed whitespace-pre-wrap">
                {result.analysis_output}
              </pre>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
