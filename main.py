import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from PyPDF2 import PdfReader
import re
import json

# Load .env file ONLY for local development (does nothing on Railway)
load_dotenv()

# Get API key from environment variable (works everywhere)
google_api_key = os.getenv("GOOGLE_API_KEY")

# Validate the key is present - FIX THIS LINE
if not google_api_key:
    # CHANGE THIS: Don't mention .env file in the error
    raise ValueError("GOOGLE_API_KEY environment variable is not set. Please add it in Railway dashboard.")

app = FastAPI(title="Job Fit & Skill Gap Analyzer API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM with the key from environment
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=google_api_key
)

# --- Prompt Template ---
template = """
You are an expert career evaluator having 20+ years of experience in HR and recruitment.you match resume with job descriptions.

Compare the following:
1. Resume Text:
{resume}

2. Job Description:
{job}

Analyze and provide:
- Job Match Percentage (0-100%)
- Matching Skills
- Missing Skills
- Suggested Skills to Learn (for better fit)
Return ONLY a valid JSON object with this exact structure:
{{
  "matched_jobs": [
    {{
      "job_title": "string",
      "match_percentage": "integer (0-100)",
      "matched_skills": ["list of matched skills"]
    }}
  ],
  "missing_skills": ["list of missing skills from resume"]
}}

Do not include any explanations or markdown.
"""

prompt = PromptTemplate(template=template, input_variables=["resume", "job"])


def extract_text_from_pdf(file: UploadFile):
    reader = PdfReader(file.file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text






import json  # Add at the top

@app.post("/analyze")
async def analyze_job_fit(
    resume_file: UploadFile = File(...),
    job_description: str = Form(...)
):
    resume_text = extract_text_from_pdf(resume_file)
    formatted_prompt = prompt.format(resume=resume_text, job=job_description)
    response = llm.invoke(formatted_prompt).content

    # Clean JSON if necessary
    json_str = re.search(r"\{.*\}", response, re.DOTALL)
    if json_str:
        response = json_str.group()
    
    # Parse the JSON string into a Python dict
    parsed_analysis = json.loads(response)
    
    # Return the parsed object directly
    return parsed_analysis
