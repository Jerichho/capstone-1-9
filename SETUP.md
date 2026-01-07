# Setup Guide for Team Members

This guide will help you get the AI Oral Exam Grader running on your machine in minutes.

## Quick Start (5 Minutes)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd ai-oral-exam-grader
```

### Step 2: Install Dependencies
```bash
pip install -e .
```

**Note:** If you get permission errors, use:
- Windows: `pip install -e . --user`
- Mac/Linux: `pip install -e . --user` or use `sudo` (not recommended)

### Step 3: Initialize Database
```bash
python -m app.db.init_db
```

You should see:
```
INFO - Creating database tables...
INFO - Database tables created successfully!
```

### Step 4: Run the Application
```bash
python run.py
```

You should see output like:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### Step 5: Open in Browser
Open your browser and go to: **http://localhost:8000**

That's it! 🎉

---

## Detailed Setup Instructions

### Prerequisites

Make sure you have:
- **Python 3.9 or higher** (check with `python --version`)
- **pip** (usually comes with Python)
- **Git** (for cloning)

#### Check Your Python Version
```bash
python --version
# Should show Python 3.9.x or higher
```

If you don't have Python 3.9+, download from [python.org](https://www.python.org/downloads/)

### Platform-Specific Instructions

#### Windows
1. Open PowerShell or Command Prompt
2. Navigate to project directory
3. Run the setup steps above

#### Mac/Linux
1. Open Terminal
2. Navigate to project directory
3. Run the setup steps above

---

## Using the Application

### Demo Mode (Default)
The app works **without any API key** in demo mode:
- Uses 3 pre-written questions
- Basic grading based on answer length
- Perfect for testing and demos

### AI Mode (Optional)
To enable AI-generated questions and AI grading:
1. Get a free API key from [together.ai](https://together.ai)
2. Set it as an environment variable:
   
   **Windows PowerShell:**
   ```powershell
   $env:TOGETHER_API_KEY="your_api_key_here"
   ```
   
   **Mac/Linux:**
   ```bash
   export TOGETHER_API_KEY="your_api_key_here"
   ```
   
   **Or create a `.env` file:**
   ```
   TOGETHER_API_KEY=your_api_key_here
   DATABASE_URL=sqlite:///./exam_grader.db
   ```
3. Restart the server

See `API_KEY_GUIDE.md` for more details.

---

## Testing the Application

### Basic Test Flow
1. Open http://localhost:8000
2. Enter a username (e.g., "test_student")
3. Click "Start Exam"
4. Answer Question 1 (about data structures)
5. Submit your answer
6. Continue to Question 2 (Big O notation)
7. Continue to Question 3 (Recursion)
8. View your final grade and feedback

### What You Should See
- ✅ Clean, modern UI
- ✅ Progress bar showing question number
- ✅ Different questions for each step
- ✅ Grading feedback after each answer
- ✅ Final grade summary at the end

---

## Troubleshooting

### "Module not found" or Import Errors
**Solution:** Make sure you installed dependencies:
```bash
pip install -e .
```

### Port 8000 Already in Use
**Solution 1:** Stop the other application using port 8000

**Solution 2:** Run on a different port:
```bash
uvicorn app.main:app --port 8001
```
Then access at http://localhost:8001

### Database Errors
**Solution:** Delete the database and reinitialize:
```bash
# Delete the database file
rm exam_grader.db  # Mac/Linux
del exam_grader.db  # Windows

# Reinitialize
python -m app.db.init_db
```

### "Command not found: python"
**Solution:** Try `python3` instead:
```bash
python3 -m app.db.init_db
python3 run.py
```

### Server Won't Start
**Check:**
1. Are you in the correct directory?
2. Did you install dependencies? (`pip install -e .`)
3. Check for error messages in the terminal

### Questions Look the Same
**This is normal in demo mode!** Each question IS different:
- Question 1: Data Structures
- Question 2: Algorithm Complexity  
- Question 3: Recursion

If you want AI-generated unique questions, see `API_KEY_GUIDE.md`.

---

## Project Structure

```
ai-oral-exam-grader/
├── app/              # Main application code
├── prompts/          # LLM prompt templates
├── run.py           # Quick start script
├── pyproject.toml   # Dependencies
└── README.md        # Project overview
```

---

## Development Tips

### Running with Auto-Reload
The server automatically reloads when you change code:
```bash
python run.py
# Or explicitly:
uvicorn app.main:app --reload
```

### Viewing Logs
Check the terminal where you ran `python run.py` for logs and errors.

### Database Location
The SQLite database is at: `exam_grader.db` (in project root)

### Making Changes
1. Edit code files
2. Server auto-reloads (if using `--reload`)
3. Refresh browser to see changes

---

## Getting Help

If you run into issues:
1. Check this guide first
2. Check `API_KEY_GUIDE.md` for API key questions
3. Check the main `README.md` for project overview
4. Ask your team members!

---

## Next Steps

Once you have it running:
- Try the full exam workflow
- Check out the code structure
- Read `README.md` for project architecture
- Review `API_KEY_GUIDE.md` if you want AI features

Happy coding! 🚀
