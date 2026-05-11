import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from backend.utils import extract_text_from_pdf, truncate_text

load_dotenv()

try:
    import streamlit as st
    api_key = st.secrets["OPENAI_API_KEY"]
except:
    api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=api_key)

def analyse_application(cv_bytes: bytes, job_description: str) -> dict:
    
    # Step 1 — Extract text from CV
    cv_text = extract_text_from_pdf(cv_bytes)
    cv_text = truncate_text(cv_text, max_chars=3000)
    
    # Step 2 — Analyse with GPT
    prompt = f"""You are an expert career coach and CV analyst. 
Analyse the following CV against the job description and provide detailed feedback.

Return your response as valid JSON only. No markdown, no code blocks, just raw JSON.

Use exactly this structure:
{{
    "match_score": <integer 0-100>,
    "match_summary": "<2-3 sentence overview of how well the candidate matches>",
    "key_strengths": [
        "<strength 1>",
        "<strength 2>",
        "<strength 3>"
    ],
    "skill_gaps": [
        {{
            "skill": "<missing skill>",
            "importance": "<High/Medium/Low>",
            "how_to_address": "<specific suggestion>"
        }}
    ],
    "cv_improvements": [
        {{
            "section_name": "<e.g. Professional Summary>",
            "original": "<original text from CV>",
            "rewritten": "<improved version tailored to this job>"
        }}
    ],
    "cover_letter": "<complete professional cover letter tailored to this specific job>"
}}

JOB DESCRIPTION:
{job_description}

CANDIDATE CV:
{cv_text}"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {
                "role": "system",
                "content": "You are an expert career coach. Always respond with valid JSON only."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )
    
    # Step 3 — Parse and return JSON
    raw = response.choices[0].message.content.strip()
    
    # Remove markdown if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    
    return json.loads(raw)