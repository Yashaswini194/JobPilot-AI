import json
import os
import time

from dotenv import load_dotenv
from google import genai

load_dotenv()

PROMPT = """You are a career coach. Compare the job description with the resume.
Return ONLY valid JSON with exactly these keys:
- "required_skills": list of the key skills/tools the job needs
- "matched_skills": list of required skills that appear in the resume
- "missing_skills": list of required skills NOT found in the resume
- "match_score": integer from 0 to 100
- "tips": list of 3 short, practical tips to improve the application

JOB DESCRIPTION:
{job}

RESUME:
{resume}
"""


def _call(client, model, prompt):
    response = client.models.generate_content(
        model=model,
        contents=prompt,
        config={"response_mime_type": "application/json"},
    )
    text = response.text.strip().removeprefix("```json").removesuffix("```").strip()
    return json.loads(text)


def analyze_job(job_description, resume_text):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY is missing. Add it to your .env file.")

    client = genai.Client(api_key=api_key)
    prompt = PROMPT.format(job=job_description, resume=resume_text)

    models = [os.getenv("GEMINI_MODEL", "gemini-3.8-flash")]
    fallback = os.getenv("GEMINI_FALLBACK_MODEL")
    if fallback:
        models.append(fallback)

    last_error = None
    for model in models:
        for attempt in range(4):
            try:
                return _call(client, model, prompt)
            except Exception as exc:
                last_error = exc
                msg = str(exc)
                if "503" in msg or "UNAVAILABLE" in msg or "429" in msg:
                    time.sleep(2 ** attempt)  # wait 1s, 2s, 4s, 8s
                else:
                    raise
    raise last_error