# SentinelOps

An AI-powered self-healing infrastructure monitoring agent, built as part of my ProdOps internship at Netsol.

## What it does

SentinelOps monitors AWS infrastructure, detects anomalies (like unusual CPU or memory spikes), 
uses an LLM to diagnose the root cause in plain English, alerts the team via Slack, and 
can safely auto-remediate simple issues (with human approval).

## Why this project

Most monitoring tools just show you a graph and expect a human to interpret it. SentinelOps 
combines a lightweight ML anomaly-detection model with an LLM reasoning layer, so the system 
explains *what's* wrong and suggests or takes action — reducing the time engineers spend 
manually digging through logs during an incident.

## Tech stack

- **Cloud**: AWS (EC2, CloudWatch, IAM, ECS)
- **Containerization**: Docker
- **ML**: Python, scikit-learn (anomaly detection)
- **AI reasoning**: Claude API (Anthropic)
- **CI/CD**: GitHub Actions
- **Infrastructure as Code**: Terraform
- **Alerting**: Slack

## Project status

🚧 In progress — built incrementally over a 6-week internship.

## Architecture

(Diagram coming soon)

## Components

- `sample-app/` — a simple Flask app used as the monitored "test subject"
- `ml-model/` — anomaly detection model (coming Week 2)
- `agent/` — LLM-based reasoning and alerting logic (coming Week 3)
- `infra/` — Terraform infrastructure definitions (coming Week 4)
