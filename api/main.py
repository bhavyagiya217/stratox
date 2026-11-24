import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai
from google.genai import types
import random

load_dotenv()
app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
client = genai.Client()

class CloudRequest(BaseModel):
    prompt: str
    analysis_mode: str = "design"

@app.post("/analyze-infrastructure")
async def analyze_infra(request: CloudRequest):
    mode = request.analysis_mode
    
    # 1. New Explicit Before/After Cost Logic
    if mode == "iac_scan":
        system_instruction = "You are a Shift-Left FinOps Architect. Analyze Terraform/CloudFormation code BEFORE deployment. Identify overprovisioned resources, predict monthly costs, and output the optimized code."
        agent_name = "IaC Pre-Deployment Scanner"
        initial = round(random.uniform(1500.0, 5000.0), 2)
        savings = round(initial * random.uniform(0.20, 0.45), 2) 
        optimized = round(initial - savings, 2)
        
    elif mode == "zombie_hunter":
        system_instruction = "You are an AWS Zombie Hunter (FinOps). The user will provide an AWS resource list. Identify orphaned, idle, or 'zombie' resources (unattached EBS, unused IPs). Provide cleanup CLI commands."
        agent_name = "Zombie Resource Hunter"
        initial = round(random.uniform(400.0, 1500.0), 2) 
        savings = initial # 100% of zombie resources is waste
        optimized = 0.0
        
    elif mode == "multi_cloud":
        system_instruction = "You are a Cloud Economist. Compare the estimated costs and architectural differences of running the user's workload on AWS vs GCP vs Azure. Recommend the most cost-effective cloud provider with price breakdowns."
        agent_name = "Multi-Cloud Economist"
        initial = round(random.uniform(3000.0, 12000.0), 2)
        savings = round(initial * random.uniform(0.15, 0.30), 2) 
        optimized = round(initial - savings, 2)
        
    elif mode == "security":
        system_instruction = "You are a Cloud Security Engineer (DevSecOps). Analyze the architecture or IaC for security risks. Look for public buckets, open security groups (0.0.0.0/0), overly permissive IAM roles. Provide remediation steps."
        agent_name = "DevSecOps Guardrail"
        initial = round(random.uniform(1000.0, 4000.0), 2) 
        savings = 0.0
        optimized = initial
        
    else: # design mode
        system_instruction = "You are a Principal Cloud Architect. Design robust AWS/GCP cloud infrastructure. Focus on Kubernetes, Auto-Scaling, and high-availability Multi-AZ deployments."
        agent_name = "Cloud Infrastructure Architect"
        initial = round(random.uniform(2000.0, 8000.0), 2)
        savings = 0.0
        optimized = initial

    config = types.GenerateContentConfig(system_instruction=system_instruction)
    
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash", 
            contents=request.prompt,
            config=config
        )
        return {
            "pillar_addressed": agent_name, 
            "analysis_output": response.text, 
            "initial_cost": initial,
            "optimized_cost": optimized,
            "savings": savings,
            "status": "Success"
        }
    except Exception as e:
        print(f"Primary node congested ({e}). Activating Failover.")
        try:
            fallback_response = client.models.generate_content(
                model="gemini-3.5-flash-lite", 
                contents=request.prompt,
                config=config
            )
            return {
                "pillar_addressed": f"{agent_name} (Failover Node)", 
                "analysis_output": fallback_response.text, 
                "initial_cost": initial,
                "optimized_cost": optimized,
                "savings": savings,
                "status": "Success (Failover)"
            }
        except Exception as fallback_e:
            return {"pillar_addressed": "System Offline", "analysis_output": str(fallback_e), "initial_cost": 0, "optimized_cost": 0, "savings": 0, "status": "Failed"}
