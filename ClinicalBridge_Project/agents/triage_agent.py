from config import TRIAGE_AGENT_TEMP
from agents.base_agent import BaseAgent
from prompts.triage_prompts import triage_prompt, TriageOutput
import json

class TriageAgent(BaseAgent):
    def __init__(self):
        super().__init__(temperature=TRIAGE_AGENT_TEMP)
        # Enforce structured output to guarantee JSON schema adherence
        self.chain = triage_prompt | self.llm.with_structured_output(TriageOutput)

    def run(self, rpm_alert: dict) -> dict:
        """
        Takes a raw RPM alert and returns a structured triage evaluation.
        """
        # invoke chain with JSON stringified rpm alert
        result = self.chain.invoke({"rpm_alert": json.dumps(rpm_alert)})
        return result.model_dump()
