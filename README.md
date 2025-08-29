# ⏏︎ Elevate — Your next level in learning

A **Streamlit**-based learning companion that tracks study sessions, analyzes strengths and weaknesses with light ML, gamifies progress with XP and levels, and exports a printable PDF progress report.

## Overview

Elevate is an end‑to‑end personal study hub: log sessions, visualize progress, receive ML‑guided recommendations, and earn XP and achievements for sustained habits.
Data is stored locally in CSV files per user, with a lightweight JSON file for authentication, enabling simple, offline‑friendly usage.

## Key features

- Account system with password hashing (SHA‑256) and per‑user data files.
- Session logging: date, subject, chapter, duration, confidence, notes, and timestamps.
- Analytics: weaknesses by topic, clustering, simple trend signals, and habit insights.
- Gamification: XP per session, levels, streak bonuses, and achievements.
- PDF export: executive summary, statistics, subject breakdown, trends, and session table.
- Streamlit UI with login/signup, dashboards, and sidebars for navigation.


## Architecture

- UI layer (Streamlit): main app entry in elevate.py orchestrates views, state, and navigation.
- Data layer (DataManager): file I/O, user auth JSON, CSV persistence, backup, and deletion.
- Analysis layer (MLAnalyzer): topic stats, weakness scoring, KMeans clustering, and trend heuristics.
- Engagement layer (GamificationSystem): XP math, level thresholds, achievements, and milestones.
- Reporting (PDFExporter): ReportLab templates and tables for exporting a polished PDF.
- Utilities (utils.py): streaks, time formatting, summaries, validation, and exports.


## Installation

- Dependencies are listed in requirements.txt; consider removing standard‑library entries (datetime, os, warnings) before installation.
- Streamlit apps are launched from the CLI using the streamlit run command.

```bash
# Recommended: create a fresh virtual environment first
pip install -r requirements.txt
```


## Quick start

- After installing dependencies, start the app with Streamlit’s CLI and open the local server in a browser.
- On first run, sign up to create a user; subsequent sessions can log in and proceed to the dashboard.

```bash
streamlit run elevate.py
```


## Data model

- Data directory: created automatically at runtime if missing (./data).
- Study data: <username>_study_data.csv with columns: date, subject, chapter, duration_minutes, confidence_rating, notes, timestamp.
- Auth data: data/user_auth.json stores username and password_hash.


## Security notes

- Passwords are hashed using SHA‑256 via hashlib before being saved to JSON.
- There is no salting or key‑stretching; for production consider salted hashes and a dedicated auth store.


## Gamification

- Session XP: base 2 XP/min with confidence multiplier and capped streak bonus; minimum 5 XP per session.
- Levels: predefined XP thresholds from Level 1 upward; progress indicators show XP to next level.
- Achievements: first session, 7‑day and 30‑day streaks, 100 hours, perfect week, quiz master, and subject expert.


## ML analytics

- Topic analysis aggregates confidence, time, session counts, consistency, and improvement trend per subject/chapter.
- Weakness identification combines low confidence, negative trends, and low consistency into a composite weakness score.
- Clustering uses KMeans on normalized features to group similar topics; prediction heuristics compute recent vs. older trends.


## PDF report

- Exports a multi‑section PDF: header, executive summary, statistics, subject breakdown, performance analysis, recommendations, and recent sessions.
- Built with ReportLab’s SimpleDocTemplate and Flowables for paragraphs and tables.


## Utilities

- Streak and consistency: rolling calculations for recent activity and study days.
- Recommendations: session length, consistency, confidence, diversity, weak topics, and recent activity prompts.
- CSV export: enhanced with formatted duration and star‑annotated confidence.


## File structure

- elevate.py — Streamlit app entry point and page configuration.
- data_manager.py — user creation/auth, CSV persistence, backup, deletion.
- gamification.py — XP math, level model, achievements, milestones, messages.
- ml_analyzer.py — topic stats, weakness scoring, clustering, trend predictions, study patterns.
- pdf_exporter.py — ReportLab templates and data‑driven PDF assembly.
- utils.py — streaks, summaries, validation, exports, and helpers.
- requirements.txt — Python dependencies (clean up standard‑library entries).


## Usage flow

- Create or log in to a profile in the app’s welcome page.
- Log study sessions with subject, chapter, duration, and confidence rating.
- Review dashboards for XP/level, streaks, weak topics, and tailored recommendations.
- Export a shareable progress report as a PDF.


## Configuration

- Data directory location is defaulted to ./data inside DataManager; adapt as needed for deployments.
- Level thresholds, XP multipliers, and achievements are centralized in GamificationSystem for tuning.


## Testing checklist

- Study logging: append and reload entries; validate date parsing and column preservation.
- Gamification: verify XP calculations across confidence levels and streak lengths.
- Analytics: ensure weak topic detection requires minimum sessions and handles small datasets.


## Known issues and fixes

- Several files appear truncated or contain formatting/syntax inconsistencies (e.g., missing brackets, ellipses), likely due to copy/paste; review and correct before running.
- requirements.txt includes Python standard‑library modules (datetime, os, warnings); remove them to avoid pip errors.


## Roadmap

- Harden authentication with salted hashing and a proper credential store (e.g., SQLite + passlib).
- Replace raw CSV writes with a transactional layer or a small database for concurrency safety.
- Add unit tests for XP math, streaks, topic analysis, and PDF generation.
- Improve error handling and input validation paths in the Streamlit UI and data layer.


## License

No license file was included in the provided source listing; add a LICENSE to clarify reuse and contributions.

## Run command (reference)

- Start the app with Streamlit’s CLI as shown below.

```bash
streamlit run elevate.py
```

<span style="display:none"></span>

<div style="text-align: center">⁂</div>

[^1]: data_manager.py

[^2]: elevate.py

[^3]: gamification.py

[^4]: ml_analyzer.py

[^5]: pdf_exporter.py

[^6]: requirements.txt

[^7]: utils.py

[^8]: https://docs.streamlit.io/develop/concepts/architecture/run-your-app

[^9]: https://docs.streamlit.io/develop/api-reference/cli

[^10]: https://docs.streamlit.io/develop/api-reference/cli/run

[^11]: https://bugs.python.org/file607/reference.pdf

[^12]: kagglelogo.jpg

[^13]: https://stackoverflow.com/questions/62760929/how-can-i-run-a-streamlit-app-from-within-a-python-script

[^14]: https://ploomber.io/blog/streamlit-from-python/

[^15]: https://mojoauth.com/hashing/sha-256-in-python/

[^16]: https://docs.kanaries.net/topics/Streamlit/how-to-run-streamlit

[^17]: https://stackoverflow.com/questions/28844370/two-different-pages-with-reportlab-simpledoctemplate-and-django

[^18]: https://unogeeks.com/python-sha256/

[^19]: https://docs.reportlab.com/reportlab/userguide/ch9_other_useful_flowables/

