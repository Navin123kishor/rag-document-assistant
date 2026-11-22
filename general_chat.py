from config import GENERAL_CHAT_SYSTEM_INSTRUCTION

class GeneralChat:
    def __init__(self, llm_client):
        self.llm_client = llm_client

    def generate_response(self, question):
        return self.llm_client.generate_response(
            prompt=question,
            system_instruction=GENERAL_CHAT_SYSTEM_INSTRUCTION
        )
