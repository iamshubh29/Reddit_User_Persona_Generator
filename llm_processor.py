# llm_processor.py
import google.generativeai as genai
import os

class LLMProcessor:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        # Using gemini-1.5-flash as it's efficient and has a generous free tier.
        # You can experiment with other models if needed.
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_persona_and_citations(self, text_data):
        """
        Uses the Gemini LLM to generate a user persona and identify supporting citations.
        """
        # Format comments and posts with their original content and URLs for LLM processing
        comments_str = "\n".join([f"Comment: \"{c['text']}\" (Source: {c['url']})" for c in text_data['comments']])
        posts_str = "\n".join([f"Post Title: \"{p['title']}\", Content: \"{p['text']}\" (Source: {p['url']})" for p in text_data['posts']])

        combined_text = ""
        if comments_str:
            combined_text += "--- User Comments ---\n" + comments_str + "\n\n"
        if posts_str:
            combined_text += "--- User Posts ---\n" + posts_str + "\n\n"

        if not combined_text.strip():
            return "No significant content available from the user's Reddit profile to generate a persona."

        # The prompt is critical for getting good results and required citations.
        # It explicitly asks for the persona structure and citation format.
        prompt = f"""
        Analyze the following Reddit user's comments and posts to create a detailed user persona.
        For each characteristic (Interests, Personality Traits, Goals, Pain Points, Online Behavior),
        you MUST cite the exact original Reddit comment or post content and its URL that directly supports the characteristic.
        If a characteristic is an inference from general activity and not directly stated or clearly visible in a single piece of content, state "Inferred from general activity."

        Structure the persona as follows:

        ---
        User Persona:

        **Name:** [Suggest a generic but descriptive name based on the persona, e.g., "Tech Enthusiast Alex" or "Culinary Gardener"]
        **Age:** [Inferred or stated - Cite source, or "Inferred from general activity."]
        **Occupation:** [Inferred or stated - Cite source, or "Inferred from general activity."]
        **Interests & Hobbies:**
        * [Interest 1] (Cite: "[Relevant comment/post text]" - [URL])
        * [Interest 2] (Cite: "[Relevant comment/post text]" - [URL])
        * ...
        **Personality Traits:**
        * [Trait 1] (Cite: "[Relevant comment/post text]" - [URL])
        * [Trait 2] (Cite: "[Relevant comment/post text]" - [URL])
        * ...
        **Goals & Motivations:**
        * [Goal 1] (Cite: "[Relevant comment/post text]" - [URL])
        * [Goal 2] (Cite: "[Relevant comment/post text]" - [URL])
        * ...
        **Pain Points & Challenges:**
        * [Pain Point 1] (Cite: "[Relevant comment/post text]" - [URL])
        * [Pain Point 2] (Cite: "[Relevant comment/post text]" - [URL])
        * ...
        **Online Behavior:**
        * [Behavior 1] (Cite: "[Relevant comment/post text]" - [URL])
        * [Behavior 2] (Cite: "[Relevant comment/post text]" - [URL])
        * ...
        ---

        Here's the user's content for analysis:

        {combined_text}
        """

        try:
            # Using generate_content for multi-turn conversations if needed, or simple text generation
            # Adjust temperature for creativity (higher) vs. more direct answers (lower)
            response = self.model.generate_content(prompt, generation_config={"temperature": 0.7})
            return response.text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return f"Could not generate persona due to LLM error: {e}"