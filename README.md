# Stratox ☁️ | Enterprise Cloud FinOps & DevSecOps Engine

![Stratox Banner](https://img.shields.io/badge/Status-Production_Ready-emerald?style=for-the-badge)

Stratox is an intelligent, high-performance Cloud Financial Operations (FinOps) and Architecture platform. Designed to shift-left cloud cost optimization, it analyzes infrastructure setups, predicts cloud billing, and automatically remediates zombie resources before deployment.

## 🚀 Key Features

- **Shift-Left IaC Cost Scanner:** Analyzes Terraform/CloudFormation code pre-deployment to identify overprovisioning and predict monthly costs.
- **Zombie Resource Hunter:** Scans telemetry data to find orphaned EBS volumes and idle load balancers, providing instant cleanup commands.
- **Multi-Cloud Arbitrage:** Compares workload pricing across AWS, Google Cloud, and Azure to recommend the most cost-effective cloud strategy.
- **Automated DevSecOps Guardrails:** Detects security vulnerabilities and generates IAM/networking fixes.
- **MoE (Mixture of Experts) Routing & Failover:** Utilizes a custom AI routing layer with Gemini API. If the primary node experiences congestion, requests are automatically routed to a High-Availability Pool to guarantee 100% uptime.

## 💻 Tech Stack
* **Frontend:** Next.js 14, Tailwind CSS (Custom "Linear-style" Dark Theme)
* **Backend:** FastAPI (Python), Uvicorn
* **AI Engine:** Google Gemini API 

## ⚙️ Local Development Setup

**1. Clone the repository:**
```bash
git clone [https://github.com/bhavyagiya217/stratox.git](https://github.com/bhavyagiya217/stratox.git)
cd stratox
