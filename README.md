# PSD Quiz Trainer (Streamlit MCQ App)

Local MCQ revision app for the “Professional Software Development” (PSD) module.

This app uses:
- **Streamlit** (single-file UI + quiz engine)
- A **JSON question bank** (`questions.json`) generated from your lecture PDF notes

## Features
- Dashboard with topic buttons and a **Full Mock Exam**
- **Immediate feedback** loop:
  - Selecting an option instantly shows **Correct** / **Incorrect**
  - If incorrect, the UI highlights the **correct answer**
  - A short **Rationale** is displayed to reinforce learning
- **Progress bar** during the session
- **Final results screen** with:
  - total score
  - percentage
  - letter grade
- **Dark-mode friendly** styling (uses minimalist CSS and Streamlit-friendly components)

## What’s inside
- `app.py`  
  Streamlit app that renders:
  - Dashboard
  - Quiz UI (options + feedback + rationale)
  - Results UI
- `questions.json`  
  The question bank in a structured JSON format:
  - topics keyed by `topic_04`, `topic_05`, `topic_06`, `topic_07`
  - each topic contains an array of questions with:
    - `id`
    - `question`
    - `options` (4 options)
    - `correct` (0-based index into `options`)
    - `rationale`
- `requirements.txt`  
  Python dependencies (currently Streamlit)

## How to run (Windows / PowerShell)

### 1) Open PowerShell in the project folder
```powershell
cd "your path"
```

### 2) Install dependencies
```powershell
pip install -r requirements.txt
```

### 3) Start the app
```powershell
streamlit run app.py --server.headless true
```

### 4) Open the local URL
The terminal will print a local address such as:
- `http://localhost:XXXX`

Copy/paste it into your browser.

## Using the app
- Click one of the topic buttons (e.g., Maintenance & Documentation / Deployment / Software Testing / Configuration Management).
- Answer all questions in the session.
- Use **Next Question →** to continue.
- At the end, review your **percentage** and **letter grade**.
- Click **Retry** to start a new shuffled session for that same topic.

## Notes / Customization
- To add more questions or fix content:
  - Edit `questions.json`
  - Keep the `correct` field as a **0-based index** into the `options` array
- The UI loads questions from `questions.json` and shuffles them each session.
