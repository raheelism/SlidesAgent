import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

class LLMClient:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")
        
        self.client = Groq(api_key=api_key)
        # User requested model
        self.model = "openai/gpt-oss-120b"

    def generate_slide_content(self, topic: str, context: str, num_slides: int, university: str, subject: str, lecturer: str) -> dict:
        prompt = f"""
        You are an expert university professor creating a high-quality lecture presentation.
        
        **Details:**
        - **University:** {university}
        - **Subject:** {subject}
        - **Lecturer:** {lecturer}
        - **Topic:** {topic}
        - **Context/Audience:** {context}
        - **Number of Slides:** {num_slides}
        
        **Goal:**
        Generate content for a {num_slides}-slide presentation. The content must be academic, detailed, and engaging.
        
        **Output Format:**
        Return a valid JSON object with the following structure:
        {{
            "university": "{university}",
            "subject": "{subject}",
            "lecturer": "{lecturer}",
            "topic": "{topic}",
            "slides": [
                {{
                    "title": "Slide Title",
                    "content": [
                        "Detailed bullet point 1",
                        "Detailed bullet point 2",
                        "Detailed bullet point 3"
                    ],
                    "speaker_notes": "Comprehensive notes for the speaker...",
                    "image_search_query": "Keywords to search for an image on the web. Leave empty if no image is needed."
                }}
            ]
        }}
        
        **Requirements:**
        1. **Content:** Deep, accurate, and suitable for university level. Avoid generic fluff.
        2. **Structure:** Logical flow (Intro -> Core Concepts -> Analysis -> Conclusion).
        3. **Images:** The `image_search_query` should be short and specific (e.g., "neural network diagram", "DNA double helix structure"). Do NOT write a long description.
        4. **JSON Only:** Do not include any markdown formatting or text outside the JSON object.
        """
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.6,
                max_tokens=8192,
                top_p=1,
                stream=False,
                stop=None,
            )
            
            response_text = completion.choices[0].message.content
            
            # Clean up potential markdown formatting
            text = response_text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.startswith("```"):
                text = text[3:]
            if text.endswith("```"):
                text = text[:-3]
            
            data = json.loads(text)
            
            # Fallback: Ensure image_search_query exists
            for slide in data.get("slides", []):
                if not slide.get("image_search_query"):
                    slide["image_search_query"] = slide.get("title", "") + " " + data.get("topic", "")
            
            print("Generated Content:", json.dumps(data, indent=2))
            return data
        except Exception as e:
            print(f"Error generating content: {e}")
            raise e
