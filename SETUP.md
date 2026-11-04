# JPS Safety BINGO — Enplug TV setup

## What this does
- One **unique** B/I/N/G/O ball (1–75) per Eastern calendar day, checked by GitHub Actions near midnight.
- Shared TV webpage shows latest ball, master board, recent history and game number.
- Never resets itself. Only a GitHub workflow **reset** can start a new game.
- The TV page refreshes state every 60 seconds and reloads itself every 15 minutes.
- No winner detection, employee card tracking or prize awarding is included.

## 1. Publish the site (GitHub account required)
1. Create a **public** GitHub repository, for example `jps-safety-bingo`. Do not put private employee information in it. GitHub Pages sites are publicly accessible.
2. Upload the contents of this folder into the **root** of the repository, including `.github/workflows/midnight-bingo.yml`. On Windows, ensure hidden `.github` is included.
3. In repository **Settings → Pages**, select **Deploy from a branch**, branch **main**, folder **/(root)**, and Save.
4. Wait for Pages to publish. The TV URL is typically `https://YOUR-USERNAME.github.io/jps-safety-bingo/` (substitute your actual account/repository). Open it in a browser to verify.
5. In repository **Settings → Actions → General → Workflow permissions**, enable **Read and write permissions** for GITHUB_TOKEN, if your organization allows it. The scheduled workflow must be able to commit the updated `state.json`. If the setting is unavailable, ask your GitHub administrator.
6. In **Actions**, enable workflows if prompted. GitHub may disable scheduled workflows after 60 days of repository inactivity; check periodically.

## 2. Show it on Enplug
1. In Enplug / Spectrio digital signage dashboard, locate the **Web Page / Website** content app (names vary by plan).
2. Add the published HTTPS GitHub Pages URL. Assign it to the JPS TV display group and publish.
3. Set full-screen display if available. Verify the number and master board fit the TV.
4. Ensure the Enplug player can reach GitHub Pages over the internet and reloads the page when necessary.

## 3. Midnight draws
- The workflow checks every hour at minute 17 UTC, but draws **only during the 12:00–12:59 AM America/New_York hour**.
- This automatically adjusts for EST and EDT. The exact draw may occur **after** 12:17 AM Eastern because GitHub-hosted scheduled jobs can be delayed or occasionally skipped. **It does not guarantee a draw at exactly 12:00:00 AM.**
- If the job misses the midnight hour entirely, no number is drawn that day. Check the Actions history and run a manual recovery with technical assistance; do not use `--force` without verifying the date and state.
- Each successful day is saved in `state.json`; repeated workflow runs cannot draw twice for the same date.

## 4. Manual reset (authorized organizer only)
1. Open your GitHub repository → **Actions** → **JPS Safety BINGO midnight draw**.
2. Click **Run workflow**; choose action **reset**, then **Run workflow**.
3. Wait for the green check. The game number increments and all 75 numbers become available again. The TVs update within about a minute (subject to caching).
4. **Reset erases the active game history** in `state.json` (older games remain in Git history). Export/save history before resetting if you need a record.

## 5. Verification and troubleshooting
- In **Actions**, confirm the scheduled job ran and succeeded. If no draw appears, check the workflow log and GitHub Pages publication.
- A browser showing the page locally from a file will not provide scheduled draws. It must be hosted and the GitHub Actions workflow enabled.
- GitHub Pages and GitHub Actions must be permitted by your company IT/security team.
- GitHub Actions cron is **best-effort**, not an exact-time service. If an exact midnight draw is mandatory, replace the scheduler with a managed cron service plus authenticated storage.
- The public board does not include a public reset button, which prevents accidental TV-side resets.
