import os
import google.generativeai as genai
from prompts.prompt import PROMPT_TEMPLATE
from dotenv import load_dotenv
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def generate_explanation(prediction: int, confidence: float) -> str:
    filled_prompt = PROMPT_TEMPLATE.format(prediction=prediction, confidence=confidence)
    response = model.generate_content(filled_prompt)
    return response.text.strip()
