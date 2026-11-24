import pathlib
import subprocess

BASE = pathlib.Path(__file__).parent.resolve()

def write(path: str, content: str):
    p = BASE / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content.strip() + "\n", encoding="utf-8")
    print(f"  [+] Created {path}")

print("\n--- Generating Apex Gateway Files ---")

# 1. package.json
write("package.json", """{
  "name": "apex-gateway",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint"
  },
  "dependencies": {
    "next": "14.2.5",
    "react": "^18",
    "react-dom": "^18",
    "lucide-react": "^0.400.0",
    "recharts": "^2.12.7"
  },
  "devDependencies": {
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18",
    "autoprefixer": "^10.0.1",
    "postcss": "^8",
    "tailwindcss": "^3.4.1",
    "typescript": "^5",
    "eslint": "^8",
    "eslint-config-next": "14.2.5"
  }
}""")

# 2. tsconfig.json
write("tsconfig.json", """{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}""")

# 3. tailwind.config.ts
write("tailwind.config.ts", """import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        "apex-dark": "#0a0f1e",
        "apex-panel": "#111827",
        "apex-border": "#1f2937",
        "apex-accent": "#6366f1",
        "apex-accent2": "#8b5cf6",
      },
      backgroundImage: {
        "apex-gradient": "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)",
      },
    },
  },
  plugins: [],
};
export default config;""")

# 4. postcss.config.js
write("postcss.config.js", """module.exports = {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};""")

# 5. next.config.js
write("next.config.js", """/** @type {import('next').NextConfig} */
const nextConfig = {};
module.exports = nextConfig;""")

# 6. app/layout.tsx
write("app/layout.tsx", """import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Apex Gateway — Enterprise LLM Router",
  description: "Intelligent LLM routing middleware for enterprise AI workloads",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} bg-apex-dark text-white antialiased`}>
        {children}
      </body>
    </html>
  );
}""")

# 7. app/globals.css
write("app/globals.css", """@tailwind base;
@tailwind components;
@tailwind utilities;

:root {
  --foreground-rgb: 255, 255, 255;
}

* {
  box-sizing: border-box;
  padding: 0;
  margin: 0;
}

html, body {
  max-width: 100vw;
  overflow-x: hidden;
  background-color: #0a0f1e;
  color: white;
  min-height: 100vh;
}""")

# 8. app/page.tsx
write("app/page.tsx", """\\"use client\\";

import { useState, useRef, useEffect } from "react";
import {
  Zap,
  DollarSign,
  Send,
  Cpu,
  Activity,
  AlertCircle,
  CheckCircle2,
  Loader2,
  BarChart3,
  ArrowUpRight,
  Bot,
  Sparkles,
} from "lucide-react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface RouteResponse {
  model_used: string;
  routing_reason: string;
  cost_saved: number;
  model_output: string;
}

interface HistoryEntry extends RouteResponse {
  prompt: string;
  timestamp: string;
}

const initialChartData = [
  { time: "00:00", requests: 0, cost: 0 },
  { time: "04:00", requests: 0, cost: 0 },
  { time: "08:00", requests: 0, cost: 0 },
  { time: "12:00", requests: 0, cost: 0 },
  { time: "16:00", requests: 0, cost: 0 },
  { time: "20:00", requests: 0, cost: 0 },
];

function MetricCard({
  icon: Icon,
  label,
  value,
  sub,
  color,
  gradient,
}: {
  icon: React.ElementType;
  label: string;
  value: string | number;
  sub?: string;
  color: string;
  gradient: string;
}) {
  return (
    <div className="relative overflow-hidden rounded-2xl border border-apex-border bg-apex-panel p-6 flex flex-col gap-3 shadow-lg group hover:border-opacity-60 transition-all duration-300">
      <div className={`absolute inset-0 opacity-0 group-hover:opacity-5 transition-opacity duration-300 ${gradient}`} />
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-gray-400">{label}</span>
        <div className={`p-2 rounded-xl ${color} bg-opacity-10`}>
          <Icon className={`w-5 h-5 ${color.replace("bg-", "text-")}`} />
        </div>
      </div>
      <div className="flex items-end gap-2">
        <span className="text-3xl font-bold text-white">{value}</span>
        {sub && <span className="text-sm text-gray-500 mb-1">{sub}</span>}
      </div>
      <div className={`h-1 w-full rounded-full ${gradient} opacity-60`} />
    </div>
  );
}

function ModelBadge({ model }: { model: string }) {
  const isPro = model.includes("pro");
  return (
    <span
      className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold border ${
        isPro
          ? "bg-indigo-500/10 text-indigo-400 border-indigo-500/30"
          : "bg-emerald-500/10 text-emerald-400 border-emerald-500/30"
      }`}
    >
      <Cpu className="w-3 h-3" />
      {model}
    </span>
  );
}

export default function ApexGateway() {
  const [prompt, setPrompt] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<RouteResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [totalRequests, setTotalRequests] = useState(0);
  const [totalCostSaved, setTotalCostSaved] = useState(0);
  const [history, setHistory] = useState<HistoryEntry[]>([]);
  const [chartData, setChartData] = useState(initialChartData);
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const responseRef = useRef<HTMLDivElement>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!prompt.trim() || loading) return;

    setLoading(true);
    setError(null);
    setResponse(null);

    try {
      const res = await fetch("http://127.0.0.1:8000/route-prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: prompt.trim() }),
      });

      if (!res.ok) {
        const errData = await res.json().catch(() => ({}));
        throw new Error((errData as { detail?: string }).detail || `Server error: ${res.status}`);
      }

      const data: RouteResponse = await res.json();
      setResponse(data);
      setTotalRequests((prev) => prev + 1);
      setTotalCostSaved((prev) => prev + data.cost_saved);

      const now = new Date();
      setHistory((prev) => [
        { ...data, prompt: prompt.trim(), timestamp: now.toLocaleTimeString() },
        ...prev,
      ].slice(0, 10));

      setChartData((prev) => {
        const updated = [...prev];
        const last = { ...updated[updated.length - 1] };
        last.requests = (last.requests || 0) + 1;
        last.cost = parseFloat(((last.cost || 0) + data.cost_saved).toFixed(6));
        updated[updated.length - 1] = last;
        return updated;
      });

      setTimeout(() => responseRef.current?.scrollIntoView({ behavior: "smooth" }), 100);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : "Unknown error occurred");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e as unknown as React.FormEvent);
    }
  };

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
    }
  }, [prompt]);

  return (
    <div className="min-h-screen bg-apex-dark flex flex-col">
      <header className="border-b border-apex-border bg-apex-panel/50 backdrop-blur-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 rounded-xl bg-apex-gradient">
              <Zap className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white tracking-tight">Apex Gateway</h1>
              <p className="text-xs text-gray-500">Enterprise LLM Routing Middleware</p>
            </div>
          </div>
          <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
            <div className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-xs text-emerald-400 font-medium">System Online</span>
          </div>
        </div>
      </header>

      <main className="flex-1 max-w-7xl mx-auto w-full px-6 py-8 flex flex-col gap-8">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <MetricCard
            icon={Activity}
            label="Total Requests"
            value={totalRequests}
            sub="routed"
            color="bg-indigo-500"
            gradient="bg-gradient-to-r from-indigo-500 to-purple-600"
          />
          <MetricCard
            icon={DollarSign}
            label="Total Cost Saved"
            value={`$${totalCostSaved.toFixed(6)}`}
            color="bg-emerald-500"
            gradient="bg-gradient-to-r from-emerald-500 to-teal-500"
          />
          <MetricCard
            icon={Cpu}
            label="Active Models"
            value={2}
            sub="available"
            color="bg-purple-500"
            gradient="bg-gradient-to-r from-purple-500 to-pink-500"
          />
          <MetricCard
            icon={BarChart3}
            label="Routing Accuracy"
            value="100%"
            color="bg-amber-500"
            gradient="bg-gradient-to-r from-amber-500 to-orange-500"
          />
        </div>

        <div className="rounded-2xl border border-apex-border bg-apex-panel p-6">
          <div className="flex items-center gap-2 mb-6">
            <BarChart3 className="w-5 h-5 text-indigo-400" />
            <h2 className="text-base font-semibold text-white">Request &amp; Cost Activity</h2>
          </div>
          <ResponsiveContainer width="100%" height={180}>
            <AreaChart data={chartData}>
              <defs>
                <linearGradient id="reqGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
                </linearGradient>
                <linearGradient id="costGrad" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#10b981" stopOpacity={0.3} />
                  <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
              <XAxis dataKey="time" stroke="#374151" tick={{ fill: "#6b7280", fontSize: 11 }} />
              <YAxis stroke="#374151" tick={{ fill: "#6b7280", fontSize: 11 }} />
              <Tooltip
                contentStyle={{ background: "#111827", border: "1px solid #1f2937", borderRadius: "12px" }}
                labelStyle={{ color: "#9ca3af" }}
              />
              <Area type="monotone" dataKey="requests" stroke="#6366f1" strokeWidth={2} fill="url(#reqGrad)" name="Requests" />
              <Area type="monotone" dataKey="cost" stroke="#10b981" strokeWidth={2} fill="url(#costGrad)" name="Cost Saved ($)" />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 flex flex-col gap-4">
            <div className="rounded-2xl border border-apex-border bg-apex-panel p-6">
              <div className="flex items-center gap-2 mb-4">
                <Bot className="w-5 h-5 text-indigo-400" />
                <h2 className="text-base font-semibold text-white">Route a Prompt</h2>
              </div>
              <form onSubmit={handleSubmit} className="flex flex-col gap-4">
                <div className="relative">
                  <textarea
                    ref={textareaRef}
                    value={prompt}
                    onChange={(e) => setPrompt(e.target.value)}
                    onKeyDown={handleKeyDown}
                    placeholder="Enter your prompt here... (Shift+Enter for newline, Enter to submit)"
                    className="w-full min-h-[100px] max-h-[160px] resize-none rounded-xl border border-apex-border bg-apex-dark text-white placeholder-gray-600 p-4 pr-14 text-sm focus:outline-none focus:border-indigo-500/60 focus:ring-1 focus:ring-indigo-500/30 transition-all"
                    disabled={loading}
                  />
                  <div className="absolute bottom-3 right-3 text-xs text-gray-600">
                    {prompt.trim().split(/\\s+/).filter(Boolean).length} words
                  </div>
                </div>
                <button
                  type="submit"
                  disabled={loading || !prompt.trim()}
                  className="flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-apex-gradient text-white font-semibold text-sm disabled:opacity-40 disabled:cursor-not-allowed hover:shadow-lg hover:shadow-indigo-500/20 transition-all duration-200 active:scale-[0.98]"
                >
                  {loading ? (
                    <><Loader2 className="w-4 h-4 animate-spin" /> Routing...</>
                  ) : (
                    <><Send className="w-4 h-4" /> Route Prompt</>
                  )}
                </button>
              </form>
            </div>

            {error && (
              <div ref={responseRef} className="rounded-2xl border border-red-500/30 bg-red-500/5 p-6 flex gap-3">
                <AlertCircle className="w-5 h-5 text-red-400 shrink-0 mt-0.5" />
                <div>
                  <p className="text-sm font-semibold text-red-400 mb-1">Routing Error</p>
                  <p className="text-sm text-red-300/80">{error}</p>
                  <p className="text-xs text-red-400/60 mt-2">Make sure the FastAPI server is running on port 8000.</p>
                </div>
              </div>
            )}

            {response && (
              <div ref={responseRef} className="rounded-2xl border border-indigo-500/20 bg-apex-panel p-6 flex flex-col gap-5">
                <div className="flex items-center gap-2 pb-3 border-b border-apex-border">
                  <CheckCircle2 className="w-5 h-5 text-emerald-400" />
                  <span className="text-sm font-semibold text-white">Routing Decision</span>
                  <div className="ml-auto">
                    <ModelBadge model={response.model_used} />
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div className="rounded-xl bg-apex-dark border border-apex-border p-4">
                    <p className="text-xs text-gray-500 mb-1 uppercase tracking-wider">Model Used</p>
                    <p className="text-sm font-semibold text-white">{response.model_used}</p>
                  </div>
                  <div className="rounded-xl bg-apex-dark border border-apex-border p-4">
                    <p className="text-xs text-gray-500 mb-1 uppercase tracking-wider">Cost Saved</p>
                    <p className="text-sm font-bold text-emerald-400">${response.cost_saved.toFixed(6)}</p>
                  </div>
                </div>

                <div className="rounded-xl bg-apex-dark border border-apex-border p-4">
                  <p className="text-xs text-gray-500 mb-2 uppercase tracking-wider flex items-center gap-1.5">
                    <Sparkles className="w-3 h-3" /> Routing Reason
                  </p>
                  <p className="text-sm text-gray-300 leading-relaxed">{response.routing_reason}</p>
                </div>

                <div className="rounded-xl bg-apex-dark border border-apex-border p-4">
                  <p className="text-xs text-gray-500 mb-2 uppercase tracking-wider flex items-center gap-1.5">
                    <Bot className="w-3 h-3" /> Model Output
                  </p>
                  <p className="text-sm text-gray-200 leading-relaxed whitespace-pre-wrap">{response.model_output}</p>
                </div>
              </div>
            )}
          </div>

          <div className="rounded-2xl border border-apex-border bg-apex-panel p-6 h-fit">
            <div className="flex items-center gap-2 mb-4">
              <Activity className="w-4 h-4 text-purple-400" />
              <h2 className="text-sm font-semibold text-white">Recent Requests</h2>
              <span className="ml-auto text-xs text-gray-600">{history.length}/10</span>
            </div>
            {history.length === 0 ? (
              <div className="text-center py-8">
                <Zap className="w-8 h-8 text-gray-700 mx-auto mb-2" />
                <p className="text-xs text-gray-600">No requests yet</p>
              </div>
            ) : (
              <div className="flex flex-col gap-2">
                {history.map((h, i) => (
                  <div key={i} className="rounded-xl bg-apex-dark border border-apex-border p-3 group hover:border-indigo-500/30 transition-colors">
                    <div className="flex items-center justify-between mb-1.5">
                      <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${
                        h.model_used.includes("pro") ? "bg-indigo-500/10 text-indigo-400" : "bg-emerald-500/10 text-emerald-400"
                      }`}>{h.model_used.includes("pro") ? "Pro" : "Flash"}</span>
                      <span className="text-xs text-gray-600">{h.timestamp}</span>
                    </div>
                    <p className="text-xs text-gray-400 truncate">{h.prompt}</p>
                    <div className="flex items-center gap-1 mt-1.5">
                      <ArrowUpRight className="w-3 h-3 text-emerald-500" />
                      <span className="text-xs text-emerald-500">${h.cost_saved.toFixed(6)} saved</span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </main>

      <footer className="border-t border-apex-border bg-apex-panel/30 py-4 mt-auto">
        <div className="max-w-7xl mx-auto px-6 flex items-center justify-between">
          <p className="text-xs text-gray-600">Apex Gateway v1.0 — Enterprise LLM Router</p>
          <p className="text-xs text-gray-600">Powered by Google Gemini</p>
        </div>
      </footer>
    </div>
  );
}""")

# 9. api/requirements.txt
write("api/requirements.txt", """fastapi
uvicorn[standard]
google-genai
python-dotenv
pydantic""")

# 10. api/.env
write("api/.env", "GEMINI_API_KEY=AQ.AB_YOUR_KEY_HERE")

# 11. api/main.py
write("api/main.py", """from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from google import genai

client = genai.Client()

app = FastAPI(title="Apex Gateway API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

COMPLEX_KEYWORDS = {
    "architect", "kubernetes", "microservices",
    "infrastructure", "orchestration", "deployment", "distributed"
}


class PromptRequest(BaseModel):
    prompt: str


@app.get("/")
def health_check():
    return {"status": "online", "service": "Apex Gateway API", "version": "1.0.0"}


@app.post("/route-prompt")
async def route_prompt(request: PromptRequest):
    prompt = request.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    word_count = len(prompt.split())
    prompt_lower = prompt.lower()
    has_complex_keyword = any(kw in prompt_lower for kw in COMPLEX_KEYWORDS)
    use_pro = word_count > 50 or has_complex_keyword

    if use_pro:
        model_id = "gemini-1.5-pro"
        cost_saved = 0.0
        if has_complex_keyword:
            matched = [kw for kw in COMPLEX_KEYWORDS if kw in prompt_lower]
            routing_reason = (
                f"Routed to Gemini 1.5 Pro: detected complex enterprise keyword(s): "
                f"{', '.join(matched)}. This model handles complex architectural reasoning tasks."
            )
        else:
            routing_reason = (
                f"Routed to Gemini 1.5 Pro: prompt exceeds 50 words ({word_count} words). "
                f"Extended context requires the Pro model."
            )
    else:
        model_id = "gemini-1.5-flash"
        cost_saved = 0.0019
        routing_reason = (
            f"Routed to Gemini 1.5 Flash: prompt is concise ({word_count} words) with no complex keywords. "
            f"Flash model is optimal for speed and cost efficiency."
        )

    try:
        response = client.models.generate_content(model=model_id, contents=prompt)
        model_output = response.text
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Model generation failed: {str(e)}")

    return {
        "model_used": model_id,
        "routing_reason": routing_reason,
        "model_output": model_output,
        "cost_saved": cost_saved,
    }""")

print("\nAll files successfully created!")
