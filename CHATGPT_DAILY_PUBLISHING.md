# ChatGPT Daily Publishing Contract

This contract is intended to be appended to the enabled **AI Research Intelligence** task that runs daily at 4:00 AM America/Chicago.

## Required publication transaction

After the research brief and standalone HTML pass all existing evidence, citation, responsive-layout, UTF-8, offline-dependency, and MIME validation checks, perform the following steps directly. Do not rely on a custom GitHub Actions rebuild workflow.

1. **Publish the report**
   - Repository: `ygeszvain/ai-research-intelligence`
   - Branch: `gh-pages`
   - Path: `reports/YYYY-MM-DD.html`
   - Content: the exact validated standalone HTML that is delivered in ChatGPT and by email.
   - Use one date-scoped commit message: `Publish AI Research Intelligence brief — YYYY-MM-DD`.

2. **Update the manifest**
   - Fetch the current `manifest.json` from `gh-pages` before writing.
   - Preserve all prior report records.
   - Add or replace only the current date’s record.
   - Sort reports newest first.
   - Update `site.generated_at_utc`, `site.report_count`, and `site.latest_report`.
   - Include: date, display date, title, concise evidence-grounded excerpt, topics, repository path, public URL, byte size, and SHA-256 hash.
   - Write valid UTF-8 JSON and parse it successfully before publishing.

3. **Update navigation artifacts**
   - `latest.html`: redirect and link to the newest report.
   - `feed.xml`: valid RSS 2.0 containing the newest reports.
   - `sitemap.xml`: valid XML containing the homepage and every report URL.
   - `robots.txt`: keep the sitemap URL current.
   - Do not rewrite `index.html` during ordinary daily publishing. It is manifest-driven and reads `manifest.json` in the browser.

4. **Verify web publication**
   - Confirm the repository file exists on `gh-pages`.
   - Confirm GitHub Pages deployment completes successfully.
   - Confirm both URLs resolve:
     - `https://ygeszvain.github.io/ai-research-intelligence/`
     - `https://ygeszvain.github.io/ai-research-intelligence/reports/YYYY-MM-DD.html`
   - Never claim successful publication based only on a successful commit.

5. **Email delivery remains required**
   - Email the same validated HTML file to `ygeszvain@gmail.com`.
   - Preserve the existing subject and email-body requirements.
   - Web publication and email are independent delivery checks. Report each outcome separately if only one succeeds.

## Anti-duplication and quality boundary

- Do not publish or email a duplicate when the existing research rules determine that no genuinely new or materially updated qualifying work exists.
- Do not publish when HTML validation fails.
- Do not overwrite a different date’s report.
- Do not delete or alter historical reports.
- Do not modify unrelated repository files, GitHub Pages configuration, credentials, permissions, billing settings, custom domains, or repository visibility.
- Do not force-push, rewrite history, or use destructive Git operations.
- If a same-date report already exists, compare it first. Replace it only when correcting or materially improving the same validated briefing, and disclose the replacement.
- If GitHub write access is unavailable, leave the repository unchanged, complete any independently valid email delivery, and state the exact web-publication failure.
- If email delivery fails, leave any valid web publication intact and state the exact email failure.
- Stop rather than guess when a SHA, branch, path, current manifest state, or delivery result cannot be verified.

## Minimal-change principle

Every daily run should change only:

- `reports/YYYY-MM-DD.html`
- `manifest.json`
- `latest.html`
- `feed.xml`
- `sitemap.xml`
- `robots.txt` only when needed

The user-friendly homepage remains stable and updates from the manifest at runtime.