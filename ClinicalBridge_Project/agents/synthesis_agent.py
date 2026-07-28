import json
from config import SYNTHESIS_AGENT_TEMP
from agents.base_agent import BaseAgent
from prompts.synthesis_prompts import synthesis_prompt

class SynthesisAgent(BaseAgent):
    def __init__(self):
        super().__init__(temperature=SYNTHESIS_AGENT_TEMP)
        self.chain = synthesis_prompt | self.llm

    def run(self, triage_level: str, patient_id: str, triage_data: dict, ehr_data: str, anamnesis_data: str) -> str:
        """
        Synthesizes all incoming streams into a comprehensive Clinical Context Brief (CCB) in Markdown.
        """
        result = self.chain.invoke({
            "triage_level": triage_level,
            "patient_id": patient_id,
            "triage_data": json.dumps(triage_data, indent=2),
            "ehr_data": ehr_data,
            "anamnesis_data": anamnesis_data
        })
        return result.content
