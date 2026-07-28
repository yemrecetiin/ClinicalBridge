import concurrent.futures
from agents.triage_agent import TriageAgent
from agents.ehr_agent import EHRAgent
from agents.anamnesis_agent import AnamnesisAgent
from agents.synthesis_agent import SynthesisAgent
from core.vector_service import VectorService

class Orchestrator:
    def __init__(self):
        self.triage_agent = TriageAgent()
        self.ehr_agent = EHRAgent()
        self.anamnesis_agent = AnamnesisAgent()
        self.synthesis_agent = SynthesisAgent()
        self.vector_service = VectorService()

    def process_scenario(self, scenario: dict) -> str:
        """
        Runs the full workflow for a given scenario.
        """
        patient_id = scenario.get("patient_id")
        rpm_alert = scenario.get("rpm_alert")
        anamnesis_input = scenario.get("anamnesis_input")

        # Run Triage, EHR, and Anamnesis Agents concurrently for speed
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # 1. Submit Triage Agent
            future_triage = executor.submit(self.triage_agent.run, rpm_alert)
            
            # 2. Submit EHR Agent
            try:
                ehr_context = self.vector_service.retrieve_context(patient_id, query="Summarize medical history and medications")
            except FileNotFoundError:
                ehr_context = "UNKNOWN (Vector DB not initialized)"
            future_ehr = executor.submit(self.ehr_agent.run, question="What are the patient's active diagnoses and medications?", context=ehr_context)
            
            # 3. Submit Anamnesis Agent
            future_anamnesis = executor.submit(self.anamnesis_agent.run, anamnesis_input)
            
            # Wait for results
            triage_result = future_triage.result()
            ehr_summary = future_ehr.result()
            anamnesis_summary = future_anamnesis.result()

        triage_level = triage_result.get("triage_level")
        
        # Clinical Guardrail: Bypass standard review UI for critical alerts
        escalation_warning = ""
        if triage_level == "Critical":
            escalation_warning = "> [!CAUTION]\n> **IMMEDIATE ESCALATION REQUIRED. BYPASSING STANDARD REVIEW DELAYS.**\n\n"

        # 4. Synthesis Agent
        ccb = self.synthesis_agent.run(
            triage_level=triage_level,
            patient_id=patient_id,
            triage_data=triage_result,
            ehr_data=ehr_summary,
            anamnesis_data=anamnesis_summary
        )

        return escalation_warning + ccb
