# Weekly run: exact steps

1. Attach and clone the repo:
   - Attach QuenWade44/drq-pins with push access.
   - Clone it with `git clone --depth 1 https://github.com/QuenWade44/drq-pins`.
   - Set git user to Claude / noreply@anthropic.com.
2. Work out N and the start date:
   - N = ((next Wednesday) − 2026-10-28) / 7 + 1.
   - START = next Wednesday (YYYY-MM-DD).
   - If week-NN/ already exists, stop and report that it already exists.
   - If N > 52, stop and tell Q the 52-week program is complete.
3. Read the inputs:
   - Read system/STRATEGY.md.
   - Read the newest files in data/, if there are any.
   - Read the last 2 plan files in plans/ so hooks don't repeat.
4. Research: run 3–5 web searches as described in STRATEGY.md §4, then write `plans/week-NN.json`.
5. Build the pins: run `python3 system/make_pins.py --week N --start START --plan plans/week-NN.json`.
6. Check the output:
   - There are 220 JPGs and 2 CSVs.
   - Each CSV has 200 or fewer rows.
   - No title is over 100 characters and no description is over 500.
   - Every board name matches catalog.json.
   - All publish dates fall in the future.
   - Open 6 random pins to check them visually.
7. Commit and push week-NN/ and plans/week-NN.json.
   - Then curl 3 random Media URLs and expect HTTP 200.
   - Note that raw.githubusercontent.com can take a minute to update.
8. Deliver to Q:
   - Send both CSV files.
   - Send a short report: the week's dates, focus boards and why (with sources), any data insights, and any listings flagged for fixes.
   - Remind Q to do Step 5: on desktop Pinterest, choose Create → Bulk create Pins, then upload file 1 and file 2.
