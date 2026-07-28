# ClinicalBridge: Bridging the Clinical Context Gap

**COP-3442: Prompt Engineering Capstone Project**  
**Bahçeşehir University, Artificial Intelligence Engineering Department**

## 📖 Overview
ClinicalBridge is an LLM-powered, multi-agent clinical decision-support prototype designed to bridge the "Clinical Context Gap." In modern healthcare, patient data is severely fragmented across three isolated silos:
1. **Electronic Health Records (EHR)** - The Patient's Past
2. **Remote Patient Monitoring (RPM)** - The Patient's Present 
3. **Anamnesis** - The Patient's Voice

ClinicalBridge acts as an intelligent intermediary, automatically synthesizing incoming RPM device alerts with the patient's EHR and Anamnesis to produce a structured, actionable **Clinical Context Brief (CCB)** for physicians in under 5 seconds.

## 🏗 System Architecture
The system employs a parallelized multi-agent architecture built with LangChain, leveraging OpenRouter and Gemini 2.5 models. 

1. **Alert Triage Agent:** Analyzes raw RPM alerts, predicts severity (Critical, Urgent, Routine, Informational), and formulates natural language queries.
2. **EHR Retrieval Agent:** A Retrieval-Augmented Generation (RAG) agent that searches longitudinal patient records via FAISS vector DB. Guardrailed against hallucination.
3. **Anamnesis Agent:** Interprets patient self-reported logs, translating colloquial symptoms (e.g., "black tarry stool") into clinical terminology (e.g., "melena").
4. **Synthesis Agent:** The final decision engine. Correlates all 3 data streams, provides a final triage level, confidence score, and inline citations.
5. **Orchestrator:** Manages parallel execution of the agents and enforces a **Critical Safety Guardrail** (Immediate human escalation bypassing synthesis if Triage flags a life-threatening alert).

## 📊 Dataset & Scenarios
This repository uses a 100% simulated dataset of 15 fictional patients with chronic conditions. It is evaluated against 5 complex clinical scenarios:
- **The Missed Medication**
- **The False Alarm** (System successfully downgrades device alerts based on context)
- **The Silent Deterioration**
- **The Incomplete Record**
- **The Conflicting Data** (System successfully upgrades device alerts based on context)

## 🚀 Installation & Setup

1. **Create Virtual Environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your OpenRouter and Google GenAI API keys:
   ```env
   GOOGLE_API_KEY="your_google_api_key"
   OPENROUTER_API_KEY="your_openrouter_api_key"
   ```

## 🧪 Running the Evaluation Harness
To execute the multi-agent system against the 5 clinical test scenarios and view the generated Clinical Context Briefs (CCB):

```bash
venv/bin/python main.py
```

### Final System Metrics
- **Triage Accuracy:** 100.0%
- **Average Latency:** ~4.95 seconds 
- **Overall Hallucination Rate:** 0.0%
- **Pass Rate:** 5/5 Scenarios

## 📁 Repository Structure
- `/agents/` - LLM Agent classes (Triage, EHR, Anamnesis, Synthesis)
- `/core/` - Orchestrator and Vector DB Service
- `/data/` - Simulated `patient_cohort.json` and test `scenarios.json`
- `/evaluation/` - Evaluation harness and advanced metric calculations
- `/prompts/` - Few-shot, CoT prompt libraries
- `/portfolio/` - Prompt engineering iteration logs for academic submission

---
*Disclaimer: This is an educational prototype built for a university capstone project. It is not a medical device and should never be used for real patient diagnosis or treatment.*
