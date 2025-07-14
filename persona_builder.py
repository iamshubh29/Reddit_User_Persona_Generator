# persona_builder.py
from llm_processor import LLMProcessor

class PersonaBuilder:
    def __init__(self, google_api_key):
        self.llm_processor = LLMProcessor(google_api_key)

    def build_persona(self, scraped_data):
        """
        Builds the user persona by orchestrating the LLM processing.
        """
        print("Building user persona with LLM...")
        user_persona_output = self.llm_processor.generate_persona_and_citations(scraped_data)
        return user_persona_output