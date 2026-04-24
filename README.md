# 🛡️ ISEO – Intrinsic Safety & Ethics Optimizer

<p align="center">
  <a href="https://crb-iseo.streamlit.app">
    <img src="https://img.shields.io/badge/Live_App-Online-brightgreen?style=for-the-badge&logo=streamlit" />
  </a>
  <a href="https://iseo-api.ai-coach-lab.com/docs">
    <img src="https://img.shields.io/badge/API-Docs-blue?style=for-the-badge&logo=swagger" />
  </a>
  <img src="https://img.shields.io/badge/Cloud-Railway-0B0D0E?style=for-the-badge&logo=railway" />
  <img src="https://img.shields.io/badge/API-FastAPI-009688?style=for-the-badge&logo=fastapi" />
  <img src="https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit" />
  <img src="https://img.shields.io/badge/LLM-Groq-000000?style=for-the-badge" />
  <img src="https://img.shields.io/badge/Container-Docker-2496ED?style=for-the-badge&logo=docker" />
  <img src="https://img.shields.io/badge/Focus-AI_Safety-critical-red?style=for-the-badge" />
</p>

## 🌐 Live System

- **UI:** https://crb-iseo.streamlit.app  
- **API Base:** https://iseo-api.ai-coach-lab.com  
- **API Docs (Swagger):** https://iseo-api.ai-coach-lab.com/docs  
- **Health Check:** https://iseo-api.ai-coach-lab.com/health  

## 📌 Overview

ISEO is a **production-ready, safety-first AI orchestration system** that evaluates user prompts before invoking LLMs.

Instead of directly generating responses, ISEO:

- Analyzes input for **risk signals**
- Applies **policy-aware decision logic**
- Routes execution through a **controlled pipeline**
- Produces **safe, explainable, and structured outputs**

## 🧠 Core Capabilities

| Capability | Description |
|----------|------------|
| 🛡 Safety Classification | Detects cyber, privacy, and harmful intent patterns |
| 📊 Risk Scoring | Assigns structured risk levels (low / medium / high) |
| ⚖ Decision Engine | Determines allow / review / block outcomes |
| 🔁 Execution Planning | Generates step-by-step AI workflows |
| 📎 Grounded Responses | Controls LLM outputs with structured reasoning |
| 📈 Evaluation Metrics | Built-in evaluation and performance tracking |

## ⚙️ Example Output

```json
{
  "status": "ok",
  "risk_level": "low",
  "decision": "allow",
  "answer": "I am ISEO, an Intrinsic Safety & Ethics Optimizer."
}
