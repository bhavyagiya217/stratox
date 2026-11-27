import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://stratox-psi.vercel.app",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

class CloudRequest(BaseModel):
    prompt: str
    analysis_mode: str = "design"

class FinOpsAnalysis(BaseModel):
    analysis_output: str = Field(
        description="Detailed markdown architecture, cost optimization, and remediation report."
    )
    initial_cost: float = Field(
        description="Estimated monthly USD cost BEFORE optimization (>= 0.0)."
    )
    optimized_cost: float = Field(
        description="Estimated monthly USD cost AFTER applying recommendations (>= 0.0)."
    )
    total_savings: float = Field(
        description="Estimated monthly USD savings achieved (initial_cost - optimized_cost, >= 0.0)."
    )

def parse_gemini_result(resp) -> FinOpsAnalysis:
    parsed = resp.parsed if getattr(resp, "parsed", None) is not None else FinOpsAnalysis.model_validate_json(resp.text)
    initial = round(max(0.0, float(parsed.initial_cost)), 2)
    optimized = round(max(0.0, float(parsed.optimized_cost)), 2)
    savings = round(max(0.0, float(parsed.total_savings)), 2)
    if savings == 0.0 and initial > optimized:
        savings = round(initial - optimized, 2)
    return FinOpsAnalysis(
        analysis_output=parsed.analysis_output,
        initial_cost=initial,
        optimized_cost=optimized,
        total_savings=savings,
    )

@app.get("/")
async def health_check():
    return {"status": "Stratox API is live", "version": "1.0.0"}

@app.post("/analyze-infrastructure")
async def analyze_infra(request: CloudRequest):
    mode = request.analysis_mode

    if mode == "iac_scan":
        system_instruction = "You are a Shift-Left FinOps Architect. Analyze Terraform/CloudFormation code BEFORE deployment. Identify overprovisioned resources, predict monthly costs, and output the optimized code."
        agent_name = "IaC Pre-Deployment Scanner"
    elif mode == "zombie_hunter":
        system_instruction = "You are an AWS Zombie Hunter (FinOps). Analyze the AWS/GCP resource list. Identify orphaned, idle, or zombie resources (unattached EBS, unused IPs), calculate wasted monthly cost as total_savings (optimized_cost = 0), and provide cleanup CLI commands."
        agent_name = "Zombie Resource Hunter"
    elif mode == "multi_cloud":
        system_instruction = "You are a Cloud Economist. Compare estimated monthly costs of running the user's workload on AWS vs GCP vs Azure, recommend the cheapest cloud, and quantify monthly savings."
        agent_name = "Multi-Cloud Economist"
    elif mode == "security":
        system_instruction = "You are a Cloud Security Engineer (DevSecOps). Analyze the architecture or IaC for security risks (public buckets, 0.0.0.0/0, permissive IAM) and provide remediation steps plus cost estimates if optimization applies."
        agent_name = "DevSecOps Guardrail"
    else:
        system_instruction = "You are a Principal Cloud Architect and FinOps Engineer. Design robust AWS/GCP infrastructure and calculate realistic monthly initial_cost, optimized_cost, and total_savings whenever cost optimization or sizing reductions apply."
        agent_name = "Cloud Infrastructure Architect"

    structured_instruction = (
        f"{system_instruction} "
        "Return structured JSON with realistic monthly USD estimates for `initial_cost`, `optimized_cost`, and `total_savings` "
        "(where `total_savings = max(0.0, initial_cost - optimized_cost)`), along with the full markdown report in `analysis_output`."
    )

    config = types.GenerateContentConfig(
        system_instruction=structured_instruction,
        response_mime_type="application/json",
        response_schema=FinOpsAnalysis,
    )

    # Multi-tier try-except fallback chain for 503 UNAVAILABLE / high demand resilience
    model_chain = [
        ("gemini-4-hydrogen", False),
        ("gemini-4-argon", True),
        ("gemini-3.5-flash-lite", True),
        ("gemini-3.1-flash-lite", True),
    ]

    last_error = None
    for model_name, is_failover in model_chain:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=request.prompt,
                config=config,
            )
            parsed = parse_gemini_result(response)
            return {
                "pillar_addressed": f"{agent_name} (Failover Node)" if is_failover else agent_name,
                "analysis_output": parsed.analysis_output,
                "initial_cost": parsed.initial_cost,
                "optimized_cost": parsed.optimized_cost,
                "savings": parsed.total_savings,
                "total_savings": parsed.total_savings,
                "status": "Success (Failover)" if is_failover else "Success",
            }
        except Exception as e:
            print(f"Model {model_name} failed/congested ({e}). Retrying next fallback model.")
            last_error = e

    return {
        "pillar_addressed": "System Offline",
        "analysis_output": str(last_error),
        "initial_cost": 0.0,
        "optimized_cost": 0.0,
        "savings": 0.0,
        "total_savings": 0.0,
        "status": "Failed",
    }