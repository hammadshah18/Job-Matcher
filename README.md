# Job Fit & Skill Gap Analyzer API

An intelligent REST API that analyzes job fit and identifies skill gaps by comparing resumes with job descriptions using Google's Gemini AI.

## Features

- **PDF Resume Parsing**: Extracts text from PDF resume files
- **AI-Powered Analysis**: Leverages Google Gemini 2.5 Flash for intelligent matching
- **Comprehensive Insights**: Provides:
  - Job match percentage (0-100%)
  - Matched skills between resume and job description
  - Missing skills needed for the role
  - Suggested skills to learn for better fit
- **CORS Enabled**: Support for frontend integrations
- **JSON Response**: Structured, easy-to-consume API responses

## Prerequisites

- Python 3.9+
- Google Gemini API key
- FastAPI
- LangChain
- PyPDF2

## Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd JobFit_SkillGap
   ```

2. **Create and activate a virtual environment** (optional but recommended):
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install manually:
   ```bash
   pip install fastapi uvicorn langchain-google-genai langchain PyPDF2 python-dotenv python-multipart
   ```

## Configuration

1. **Create a `.env` file** in the project root:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

2. **Get your Google API Key**:
   - Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Click "Get API Key" or "Create API key in new project"
   - Copy the generated key and paste it in your `.env` file

## Usage

### Start the Server

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`

### API Documentation

- **Interactive API Docs**: http://127.0.0.1:8000/docs (Swagger UI)
- **Alternative Docs**: http://127.0.0.1:8000/redoc (ReDoc)

### Endpoints

#### POST `/analyze`

Analyzes job fit by comparing a resume with a job description.

**Request**:
- `resume_file` (File): PDF file of the resume
- `job_description` (Form): Job description text

**Example with cURL**:
```bash
curl -X POST "http://127.0.0.1:8000/analyze" \
  -F "resume_file=@resume.pdf" \
  -F "job_description=Software Engineer role seeking 5+ years Python experience..."
```

**Example with Python**:
```python
import requests

with open('resume.pdf', 'rb') as f:
    files = {'resume_file': f}
    data = {'job_description': 'Your job description here...'}
    response = requests.post('http://127.0.0.1:8000/analyze', files=files, data=data)
    print(response.json())
```

**Response**:
```json
{
  "matched_jobs": [
    {
      "job_title": "Software Engineer",
      "match_percentage": 75,
      "matched_skills": ["Python", "FastAPI", "REST APIs", "Docker"]
    }
  ],
  "missing_skills": ["Kubernetes", "AWS", "GraphQL"]
}
```

## Project Structure

```
JobFit_SkillGap/
├── main.py              # Main API application
├── .env                 # Environment variables (not in repo)
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

## How It Works

1. **Resume Upload**: User uploads a PDF resume
2. **Text Extraction**: `extract_text_from_pdf()` extracts text from the PDF
3. **Prompt Formatting**: The resume and job description are formatted into a prompt template
4. **AI Analysis**: Google Gemini analyzes the match and generates structured JSON
5. **JSON Parsing**: Response is parsed and returned to the user

## Troubleshooting

### "API Key not found" Error
- Verify `.env` file exists in the project root
- Ensure `GOOGLE_API_KEY=your_key` is in the `.env` file (no extra quotes)
- Restart the server after updating `.env`

### "Invalid API Key" Error
- Check that your Google API key is valid
- Ensure the Generative AI API is enabled in your Google Cloud project
- Generate a new API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

### PDF Parsing Issues
- Ensure PDF is not corrupted
- Verify resume contains extractable text (not scanned image)

### CORS Issues
- The API is configured to accept requests from any origin
- For production, update `allow_origins` in the CORS middleware

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Google Gemini API key | `AIzaSy...` |

## Dependencies

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **langchain-google-genai**: Google Gemini integration
- **langchain**: LLM framework
- **PyPDF2**: PDF text extraction
- **python-dotenv**: Environment variable management
- **python-multipart**: Form data handling

## Model Used

- **Gemini 2.5 Flash**: Fast, efficient model for instant analysis

## Future Enhancements

- Support for multiple document formats (DOCX, TXT)
- Batch file processing
- Database integration for analysis history
- Advanced skill weight calculations
- User authentication and rates limiting
- Detailed skill mapping and recommendations

## License

This project is provided as-is for educational and professional use.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Verify your Google API key configuration
3. Review FastAPI documentation at [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
