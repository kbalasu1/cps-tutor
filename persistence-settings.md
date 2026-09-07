# Persistence Settings

## Decision

Use **Hugging Face Spaces Persistent Storage** (paid add-on) rather than an
external service like Google Drive. It requires zero extra code or
credentials — `app.py` already targets it correctly.

## Why

- The student's session data (chat threads, saved study notebook entries)
  should survive Space restarts/sleeps, not just last for one browsing
  session.
- A Google Drive sync was considered as a free alternative, but it needs a
  Google Cloud service account (project + Drive API + key management) and
  adds per-message upload latency for a single-user app. Not worth the
  operational overhead here.
- HF's free tier gives the Space container an ephemeral disk — anything
  written to it is wiped on restart/sleep. The Persistent Storage add-on
  mounts a real disk at `/data` that survives those cycles.

## How it works in this app

`app.py` already contains the routing logic:

```python
DB_DIR = "/data" if os.path.exists("/data") else "."
DB_PATH = os.path.join(DB_DIR, "tutor_data.db")
```

- If `/data` exists (Persistent Storage is enabled on the Space), the SQLite
  DB lives there and survives restarts.
- If `/data` doesn't exist (local dev, or a Space without the add-on), it
  falls back to the working directory — fine for local testing, but data
  will NOT survive a Space restart/sleep in that case.

## Setup steps (do this once per Space)

1. Go to your Space → **Settings** → **Persistent Storage**.
2. Pick a storage tier (check current HF pricing at the time you set this
   up — it's a small monthly cost, billed per Space).
3. Save. HF mounts the disk at `/data` automatically — no code change or
   redeploy needed.
4. Restart the Space once so `app.py` picks up `/data` on its next boot.

## Not doing right now

- Google Drive sync (service-account based) — revisit if the paid tier
  becomes a blocker.
- Any backup/export of the SQLite file — `/data` persists across
  restarts, but isn't itself backed up. Low priority for a single-student
  tool, but worth a manual export button later if the data starts to matter
  more.
