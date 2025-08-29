# Elevate

<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# This is project I made , Analyze it and write readme file for it .

Here is a polished README for the project, synthesized from the provided source files and aligned with how the app is structured and intended to run.[^1][^2][^3][^4][^5][^6][^7]

# ⏏︎ Elevate — Study Tracker

A **Streamlit**-based learning companion that tracks study sessions, analyzes strengths and weaknesses with light ML, gamifies progress with XP and levels, and exports a printable PDF progress report.[^2][^3][^4][^5][^1]

## Overview

Elevate is an end‑to‑end personal study hub: log sessions, visualize progress, receive ML‑guided recommendations, and earn XP and achievements for sustained habits.[^3][^4][^2]
Data is stored locally in CSV files per user, with a lightweight JSON file for authentication, enabling simple, offline‑friendly usage.[^1]

## Key features

- Account system with password hashing (SHA‑256) and per‑user data files.[^1]
- Session logging: date, subject, chapter, duration, confidence, notes, and timestamps.[^1]
- Analytics: weaknesses by topic, clustering, simple trend signals, and habit insights.[^4][^7]
- Gamification: XP per session, levels, streak bonuses, and achievements.[^3]
- PDF export: executive summary, statistics, subject breakdown, trends, and session table.[^5]
- Streamlit UI with login/signup, dashboards, and sidebars for navigation.[^2]


## Architecture

- UI layer (Streamlit): main app entry in elevate.py orchestrates views, state, and navigation.[^2]
- Data layer (DataManager): file I/O, user auth JSON, CSV persistence, backup, and deletion.[^1]
- Analysis layer (MLAnalyzer): topic stats, weakness scoring, KMeans clustering, and trend heuristics.[^4]
- Engagement layer (GamificationSystem): XP math, level thresholds, achievements, and milestones.[^3]
- Reporting (PDFExporter): ReportLab templates and tables for exporting a polished PDF.[^5]
- Utilities (utils.py): streaks, time formatting, summaries, validation, and exports.[^7]


## Installation

- Dependencies are listed in requirements.txt; consider removing standard‑library entries (datetime, os, warnings) before installation.[^6]
- Streamlit apps are launched from the CLI using the streamlit run command.[^8][^9]

```bash
# Recommended: create a fresh virtual environment first
pip install -r requirements.txt
```


## Quick start

- After installing dependencies, start the app with Streamlit’s CLI and open the local server in a browser.[^10][^8]
- On first run, sign up to create a user; subsequent sessions can log in and proceed to the dashboard.[^2][^1]

```bash
streamlit run elevate.py
```


## Data model

- Data directory: created automatically at runtime if missing (./data).[^1]
- Study data: <username>_study_data.csv with columns: date, subject, chapter, duration_minutes, confidence_rating, notes, timestamp.[^1]
- Auth data: data/user_auth.json stores username and password_hash.[^1]


## Security notes

- Passwords are hashed using SHA‑256 via hashlib before being saved to JSON.[^1]
- There is no salting or key‑stretching; for production consider salted hashes and a dedicated auth store.[^1]


## Gamification

- Session XP: base 2 XP/min with confidence multiplier and capped streak bonus; minimum 5 XP per session.[^3]
- Levels: predefined XP thresholds from Level 1 upward; progress indicators show XP to next level.[^3]
- Achievements: first session, 7‑day and 30‑day streaks, 100 hours, perfect week, quiz master, and subject expert.[^3]


## ML analytics

- Topic analysis aggregates confidence, time, session counts, consistency, and improvement trend per subject/chapter.[^4]
- Weakness identification combines low confidence, negative trends, and low consistency into a composite weakness score.[^4]
- Clustering uses KMeans on normalized features to group similar topics; prediction heuristics compute recent vs. older trends.[^4]


## PDF report

- Exports a multi‑section PDF: header, executive summary, statistics, subject breakdown, performance analysis, recommendations, and recent sessions.[^5]
- Built with ReportLab’s SimpleDocTemplate and Flowables for paragraphs and tables.[^11][^5]


## Utilities

- Streak and consistency: rolling calculations for recent activity and study days.[^7]
- Recommendations: session length, consistency, confidence, diversity, weak topics, and recent activity prompts.[^7]
- CSV export: enhanced with formatted duration and star‑annotated confidence.[^7]


## File structure

- elevate.py — Streamlit app entry point and page configuration.[^2]
- data_manager.py — user creation/auth, CSV persistence, backup, deletion.[^1]
- gamification.py — XP math, level model, achievements, milestones, messages.[^3]
- ml_analyzer.py — topic stats, weakness scoring, clustering, trend predictions, study patterns.[^4]
- pdf_exporter.py — ReportLab templates and data‑driven PDF assembly.[^5]
- utils.py — streaks, summaries, validation, exports, and helpers.[^7]
- requirements.txt — Python dependencies (clean up standard‑library entries).[^6]


## Usage flow

- Create or log in to a profile in the app’s welcome page.[^2][^1]
- Log study sessions with subject, chapter, duration, and confidence rating.[^2][^1]
- Review dashboards for XP/level, streaks, weak topics, and tailored recommendations.[^4][^2][^3]
- Export a shareable progress report as a PDF.[^5][^2]


## Configuration

- Data directory location is defaulted to ./data inside DataManager; adapt as needed for deployments.[^1]
- Level thresholds, XP multipliers, and achievements are centralized in GamificationSystem for tuning.[^3]


## Testing checklist

- Study logging: append and reload entries; validate date parsing and column preservation.[^1]
- Gamification: verify XP calculations across confidence levels and streak lengths.[^3]
- Analytics: ensure weak topic detection requires minimum sessions and handles small datasets.[^4]


## Known issues and fixes

- Several files appear truncated or contain formatting/syntax inconsistencies (e.g., missing brackets, ellipses), likely due to copy/paste; review and correct before running.[^5][^2][^4]
- requirements.txt includes Python standard‑library modules (datetime, os, warnings); remove them to avoid pip errors.[^6]


## Roadmap

- Harden authentication with salted hashing and a proper credential store (e.g., SQLite + passlib).[^1]
- Replace raw CSV writes with a transactional layer or a small database for concurrency safety.[^1]
- Add unit tests for XP math, streaks, topic analysis, and PDF generation.[^7][^5][^4][^3]
- Improve error handling and input validation paths in the Streamlit UI and data layer.[^2][^1]


## License

No license file was included in the provided source listing; add a LICENSE to clarify reuse and contributions.[^6][^5][^7][^2][^4][^3][^1]

## Run command (reference)

- Start the app with Streamlit’s CLI as shown below.[^9][^8]

```bash
streamlit run elevate.py
```

<span style="display:none">[^12][^13][^14][^15][^16][^17][^18][^19]</span>

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

