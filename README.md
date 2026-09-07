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
4. **Stay zero-friction** — runs in the browser, no student login
   required.

## Local development

```bash
pip install -r requirements.txt
mkdir -p .streamlit
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# edit .streamlit/secrets.toml and set GEMINI_API_KEY
# (TURSO_DATABASE_URL / TURSO_AUTH_TOKEN are optional - see persistence-settings.md)
streamlit run app.py
```

## Deployment

**Live at:** [balu-thatha.streamlit.app](https://balu-thatha.streamlit.app/)
(Streamlit Community Cloud). A Hugging Face Space also exists as a backup
target - both deploy from this same repo.

1. Push to GitHub - the repo must stay **public** for Streamlit Community
   Cloud's free tier to deploy from it.
2. On [share.streamlit.io](https://share.streamlit.io), deploy from this
   repo/`main`/`app.py`.
3. In the app's **Settings → Secrets**, add `GEMINI_API_KEY` (and, for
   persistence across redeploys, `TURSO_DATABASE_URL` /
   `TURSO_AUTH_TOKEN` — see `persistence-settings.md`).

Any push to `main` auto-redeploys the Streamlit Cloud app.

## Project layout

- `app.py` — Streamlit UI, libSQL/SQLite persistence, Gemini call loop.
- `prompts.py` — the tutor's pedagogical system instruction (Socratic
  method, homework-image handling, i-Ready domain mapping, topic
  boundaries, opening greeting).
- `secret_retrieval.py` — reads `GEMINI_API_KEY` and the optional Turso
  credentials from Streamlit secrets or environment variables.
- `persistence-settings.md` — the storage decision and rationale.
- `spec.md` — original project specification.
