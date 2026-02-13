# 100 Apps Challenge

## Overview
Multi-app project for a 100 apps vibecoding challenge using Replit and Claude Code.

## Current State
Currently serving `apps/004-password-generator` — a password generator and strength checker app.

## Project Architecture
- `index.html` — Root landing page
- `server.py` — Python HTTP server (port 5000, host 0.0.0.0, no-cache headers), serves the active app directory
- `apps/003-move-countdown/index.html` — Move countdown app (plain HTML/CSS/JS) with milestone tracker (checkable items, localStorage persistence, collapsible groups, progress bar)
- `.gitignore` — Python-focused gitignore

## Running
The project runs via the "Start application" workflow which executes `python server.py`. The server currently serves from `apps/003-move-countdown`.

## User Preferences
- Prefers plain HTML/CSS/JS for simple apps
- Apps are organized under `apps/` directory with numbered naming convention
