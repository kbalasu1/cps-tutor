# Persistence Settings

## Current decision: Turso (hosted libSQL)

Superseded an earlier HF-only plan (see "History" below) once we actually
deployed to Streamlit Community Cloud, which has no paid-disk equivalent
to HF's Persistent Storage add-on at all - its filesystem is ephemeral,
full stop.

Turso is a free-tier hosted libSQL database (SQLite-compatible, network
accessible). `app.py` connects to it via the `libsql` Python package,
which mirrors the stdlib `sqlite3` API closely enough that the rest of
the code (cursors, `.execute()`, `.fetchall()`, `.commit()`) didn't need
to change - only `get_db_connection()` did.

## Why this over the alternatives

- **HF Persistent Storage (the old plan):** works, but only on HF Spaces,
  costs money, and we're not currently deploying there (HF account is
  still pending quota/verification).
- **Google Drive sync:** considered early on, rejected - needs a service
  account, adds per-message upload latency, and this solves the same
  problem for free without any of that.
- **Accept ephemeral storage:** simplest, but the whole point of the
  Study Notebook is to keep explanations around to review later - losing
  it on every redeploy/sleep defeats that.
- **Turso:** free tier, works identically across local dev, Streamlit
  Cloud, and HF Spaces (if we ever go back), no per-message latency
  concerns for a single low-traffic user, minimal code change.

## How it works in this app

`app.py`'s `get_db_connection()`:
- If `TURSO_DATABASE_URL` and `TURSO_AUTH_TOKEN` are both set (via
  `st.secrets` or env vars, same pattern as `GEMINI_API_KEY`), connects
  directly to the remote Turso database - every query goes over the
  network, no local file involved.
- Otherwise, falls back to a local SQLite file (`/data/tutor_data.db` if
  `/data` exists - i.e. HF Persistent Storage is mounted - else
  `./tutor_data.db` in the working directory). This fallback does NOT
  survive redeploys/sleep on Streamlit Cloud or an HF Space without the
  paid storage add-on.

## Setup steps (one-time)

1. Create a free account at [turso.tech](https://turso.tech).
2. Create a database: `turso db create balu-thatha`
3. Get the URL: `turso db show balu-thatha --url`
4. Create an auth token: `turso db tokens create balu-thatha`
5. Add both as secrets (see `.streamlit/secrets.toml.example` for the
   exact keys) - locally in `.streamlit/secrets.toml`, and in Streamlit
   Community Cloud's app Settings -> Secrets for production.

## History: the original HF-only plan

Before this app was live anywhere, the plan was to rely on HF Spaces'
paid Persistent Storage add-on, mounting a disk at `/data`. That's still
what the `/data` fallback check in `get_db_connection()` is for, in case
we ever deploy there without Turso configured - but it's no longer the
primary plan now that Turso covers every deployment target uniformly.
