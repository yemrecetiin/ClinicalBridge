from config import EHR_AGENT_TEMP
from agents.base_agent import BaseAgent
from prompts.ehr_prompts import ehr_prompt

class EHRAgent(BaseAgent):
    def __init__(self):
        super().__init__(temperature=EHR_AGENT_TEMP)
        self.chain = ehr_prompt | self.llm

    def run(self, question: str, context: str) -> str:
        """
        Takes a clinical question and context (retrieved from Vector DB),
        returns a summary without hallucination.
        """
        result = self.chain.invoke({
            "question": question,
            "context": context
        })
        return result.content
