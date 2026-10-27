# Weekly prompt (paste into a new Claude chat, or use it as a scheduled task)

Run my weekly Pinterest pin build for School Templates By Dr. Q.

1. Attach the GitHub repo QuenWade44/drq-pins with push access and clone it. Set the git author to Claude <noreply@anthropic.com>.
2. Read system/RUNBOOK.md and system/STRATEGY.md and follow them exactly. Build the week that starts this coming Wednesday. Week N starts on 2026-10-28 + 7×(N−1) days.
3. Research with 3–5 live web searches:
   - what's happening in US K–12 schools that week
   - education news that drives demand
   - any reachable Pinterest education trends
   Also use any exports in data/. Use what you find to write plans/week-NN.json, with a source for each research note.
4. Build the pins:
   - Run python3 system/make_pins.py --week N --start YYYY-MM-DD --plan plans/week-NN.json and run every check in the runbook.
   - Push week-NN/ and the plan to main.
   - Confirm that 3 image links load.
5. Send me:
   - both CSV files (file A for Wednesday, file B for Saturday; 100 pins each)
   - a short report: publish dates, focus boards and why (with sources), data insights, and listings to fix
   - the upload reminder: Wednesday before 2 pm upload file A; Saturday before 2 pm upload file B. Path: Pinterest desktop → profile menu (down-arrow, top right) → Settings → Import content → Upload .csv. Never both on the same day (100 scheduled-pin limit).

Stop and tell me if:
- that week's folder already exists
- the week number is over 52
- anything fails

Never post to Pinterest yourself. Never use Psych Report Assistant branding.
