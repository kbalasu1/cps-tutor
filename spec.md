# Project Specification: CPS 7th Grade Academic & Selective Enrollment Prep Tutor

## 1. Overview & Objective
Build an interactive, multimodal web application designed for a 7th-grade Chicago Public Schools (CPS) student, deployable on **Hugging Face Spaces**.

### Strategic Objectives
1. **Curriculum Mastery & Grade Protection:** Maintain straight As in 7th-grade core subjects (Math, English/Reading, Science, Social Science). Under CPS Selective Enrollment criteria, 7th-grade final core grades account for exactly 50% (320 of 640 total composite points).
2. **Admissions Test Preparation:** Progressively build foundational skills, test stamina, and strategic competence for the CPS Selective Enrollment Admissions Exam taken in early 8th grade (**PreACT 9 Secure** format).
3. **Multimodal Remediation:** Ingest photos and screenshots of handwritten homework assignments, math worksheets, and i-Ready Diagnostic score reports to pinpoint learning gaps and provide targeted remediation.
4. **Zero-Friction Access:** Hosted on Hugging Face Spaces so the student can access the tutor via browser or tablet without needing to log in to personal or parent Google accounts.

---

## 2. Tech Stack & Environment Architecture

- **Language & Runtime:** Python 3.10+
- **Frontend Framework:** Streamlit (`streamlit>=1.35.0`)
- **Deployment Target:** **Hugging Face Spaces** (SDK: `streamlit`)
- **LLM Engine & SDK:** Google GenAI SDK (`google-genai>=0.1.1`) using model `gemini-2.5-flash`
- **Multimodal Image Processing:** Pillow (`pillow>=10.0.0`)
- **State & Data Persistence:** SQLite (`sqlite3` standard library)
- **Secrets Management:**
  - **Local Development:** `.streamlit/secrets.toml` or environment variables via `.env`
  - **Hugging Face Spaces:** Repository Secrets via Space Settings (`GEMINI_API_KEY`)

---

## 3. Hugging Face Spaces Deployment Configuration

Hugging Face Spaces natively supports Streamlit applications. The repository must adhere to the following configuration requirements:

### 3.1 Space Metadata (`README.md` Frontmatter)
The root `README.md` must begin with YAML frontmatter specifying the Space runtime:

```yaml
---
title: CPS 7th Grade Tutor
emoji: 🎓
colorFrom: blue
colorTo: indigo
sdk: streamlit
sdk_version: 1.35.0
app_file: app.py
pinned: false
---