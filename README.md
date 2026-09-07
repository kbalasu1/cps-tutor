---
title: Balu Thatha - CPS Tutor
emoji: 👴
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.35.0
app_file: app.py
pinned: false
---

# Balu Thatha — CPS 7th Grade Academic & Selective Enrollment Prep Tutor

Named after a real grandfather, "Balu Thatha" ("Thatha" = grandfather) is
an interactive, multimodal Streamlit tutor for a 7th-grade Chicago Public
Schools (CPS) student, built to:

1. **Protect core grades** — Math, English/Reading, Science, and Social
   Science mastery support (7th-grade grades are 50% of the CPS Selective
   Enrollment composite score).
2. **Build admissions-test readiness** — progressive skill-building for the
   PreACT 9 Secure exam taken in early 8th grade.
3. **Remediate from real work** — upload photos of handwritten homework,
   math worksheets, or i-Ready diagnostic reports for targeted feedback.
4. **Stay zero-friction** — runs on Hugging Face Spaces, no student login
   required.

## Local development

```bash
pip install -r requirements.txt
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edit .streamlit/secrets.toml and set GEMINI_API_KEY
streamlit run app.py
```

## Deployment (Hugging Face Spaces)

1. Push this repo to a Space with SDK = `streamlit` (already configured via
   the frontmatter above).
2. In the Space's **Settings → Repository secrets**, add `GEMINI_API_KEY`.
3. (Recommended) Enable **Persistent Storage** so chat history and the
   study notebook survive restarts — see `persistence-settings.md` for
   details.

## Project layout

- `app.py` — Streamlit UI, SQLite persistence, Gemini call loop.
- `prompts.py` — the tutor's pedagogical system instruction (Socratic
  method, homework-image handling, i-Ready domain mapping).
- `secret_retrieval.py` — reads `GEMINI_API_KEY` from Streamlit secrets or
  environment variables.
- `persistence-settings.md` — the storage-tier decision and rationale.
- `spec.md` — original project specification.
