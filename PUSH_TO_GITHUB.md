# Quick Guide to Push to GitHub

Your code is committed and ready! Follow these steps:

## Option 1: Create Repository via GitHub Website (Recommended)

1. **Go to GitHub:** https://github.com/new
2. **Repository name:** `ai-oral-exam-grader`
3. **Visibility:** Choose Public or Private
4. **DO NOT** check "Add a README file" (we already have one)
5. **Click "Create repository"**

6. **Then run these commands:**

```powershell
# Add the remote (GitHub will show you the exact URL)
git remote add origin https://github.com/Kyle-Eberhart/ai-oral-exam-grader.git

# Push your code
git branch -M main
git push -u origin main
```

## Option 2: Use Cursor's GitHub Integration

If Cursor has GitHub integration built-in:
1. Look for a "Source Control" panel in Cursor
2. Look for a "Publish to GitHub" button
3. Or check Cursor's menu for GitHub options

---

## After Pushing

Once pushed, share this URL with your team:
`https://github.com/Kyle-Eberhart/ai-oral-exam-grader`

They can then:
```bash
git clone https://github.com/Kyle-Eberhart/ai-oral-exam-grader.git
cd ai-oral-exam-grader
.\setup.ps1  # Windows
# or
./setup.sh   # Mac/Linux
```

---

**Your code is ready to push! ✅**

