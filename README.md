# AI Research Intelligence

A static, searchable archive of evidence-grounded AI and machine-learning research briefs.

## Public site

https://ygeszvain.github.io/ai-research-intelligence/

## Publishing model

The archive does **not** use a custom GitHub Actions rebuild workflow.

The 4:00 AM America/Chicago ChatGPT task is responsible for each complete publication transaction:

1. Generate and validate the standalone report HTML.
2. Publish it to `reports/YYYY-MM-DD.html` on the `gh-pages` branch.
3. Update `manifest.json` with the new report metadata and SHA-256 hash.
4. Update `latest.html`, `feed.xml`, `sitemap.xml`, and `robots.txt` as needed.
5. Verify the report URL and archive homepage.
6. Email the same validated HTML to `ygeszvain@gmail.com`.

`index.html` is manifest-driven. It reads `manifest.json` in the visitor’s browser and therefore does not need to be rewritten for each daily report.

See `CHATGPT_DAILY_PUBLISHING.md` for the required publication contract and failure boundaries.

The repository intentionally contains no `CNAME` file and uses the standard GitHub Pages project URL.