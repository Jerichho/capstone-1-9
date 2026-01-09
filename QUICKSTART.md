# Quick Start Guide

## Prerequisites

- Python 3.9 or higher
- pip package manager

## Setup Instructions

1. **Install dependencies:**
   ```bash
   pip install -e .
   pip install together
   ```

2. **Set up environment variables (Optional):**
   - **Note:** The app works perfectly without an API key! It will use pre-written fallback questions and basic grading.
   - If you want AI-generated questions and AI grading, set up a Together.ai API key:
     - Copy `.env.example` to `.env` (if you can create it)
     - Or set environment variables directly:
       ```bash
       # Windows PowerShell
       $env:TOGETHER_API_KEY="your_api_key_here"
       $env:DATABASE_URL="sqlite:///./exam_grader.db"
       
       # Linux/Mac
       export TOGETHER_API_KEY="your_api_key_here"
       export DATABASE_URL="sqlite:///./exam_grader.db"
       ```
   - See `API_KEY_GUIDE.md` for more details about API keys (optional)

3. **Initialize the database:**
   ```bash
   python -m app.db.init_db
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```
   Or:
   ```bash
   uvicorn app.main:app --reload
   ```

5. **Access the application:**
   - Open your browser to `http://localhost:8000`
   - Enter a username to start an exam
   - Answer the generated questions
   - View your final grade at the end

## Important Notes

- **No API key required!** The app runs and works perfectly without one, using fallback questions and basic grading
- If you want AI features, set a `TOGETHER_API_KEY` environment variable (see `API_KEY_GUIDE.md`)
- The database file (`exam_grader.db`) will be created automatically in the project root
- All prompt templates are in the `prompts/` directory
- The application generates 3 questions by default (configurable in settings)

## Troubleshooting

- If you get import errors, make sure you've installed the dependencies with `pip install -e .`
- If the LLM API fails (only relevant if using an API key), check that your API key is correct and that you have API credits - the app will automatically use fallback questions/grading if the LLM is unavailable
- **App crashes on startup?** → This was fixed! The app now starts successfully without an API key. If you still have issues, check that all dependencies are installed correctly.

