from config import ANAMNESIS_AGENT_TEMP
from agents.base_agent import BaseAgent
from prompts.anamnesis_prompts import anamnesis_prompt

class AnamnesisAgent(BaseAgent):
    def __init__(self):
        super().__init__(temperature=ANAMNESIS_AGENT_TEMP)
        self.chain = anamnesis_prompt | self.llm

    def run(self, patient_input: str) -> str:
        """
        Translates colloquial patient input into formal clinical terminology.
        """
        result = self.chain.invoke({
            "patient_input": patient_input
        })
        return result.content
