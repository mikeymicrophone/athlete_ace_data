---
name: sports-seed-sources
description: Capture and verify public sports roster, historical NBA participant, NHL schedule, and team visual sources for the AthleteAce seed catalog. Use for source refresh or catalog coverage work, not live scores or unsourced roster generation.
---

# Sports seed sources

Locate the AthleteAce checkout and its data repository at `db/seeds/athlete_ace_data`. Use the checkout's pinned Ruby and bundle for the scripts. Inspect the current target seasons before fetching; the installed scripts currently target 2026 calendar seasons and 2026/27 split-year seasons. A capture date does not select a season.

Read `sources/coverage_2026/README.md` in the data repository for the source meanings and known failures. Read the application's `docs/seed-library-2026.md` before importing or applying schedule changes. If these resources are absent, locate the actual checkout before prescribing commands.

## Choose the source by the claim

- NHL season rosters use `https://api-web.nhle.com/v1/roster/{CLUB}/{YYYYYYYY}`. Full schedules use `/v1/club-schedule-season/{CLUB}/{YYYYYYYY}`. Fetch all 32 clubs, select regular-season game type 2, and deduplicate by NHL game ID. For 2026/27, require 84 games per club, 1,344 distinct games, and two agreeing copies of each game. Do not carry that count to another season without checking its format.
- MLB uses `https://statsapi.mlb.com/api/v1/teams?sportId=1&season={YEAR}` and `/api/v1/teams/{ID}/roster?rosterType=fullSeason&season={YEAR}&hydrate=person`. The full-season inventory includes departed players and does not establish current active status or dates of number use.
- ESPN uses `https://site.api.espn.com/apis/site/v2/sports/{SPORT}/{LEAGUE}/teams?limit=100&season={YEAR}` and `/teams/{ID}/roster?season={YEAR}`. NBA uses the ending year; current soccer competitions use the starting year. Confirm the returned season. NFL athletes are grouped under `items`; soccer players can have one name. Preserve stable provider IDs and do not fabricate surnames.
- Historical NBA participant unions use Basketball Reference's `/leagues/NBA_{ENDING_YEAR}_per_game.html`. Inspect both `per_game_stats` and `per_game_stats_post`. Retain team-specific rows and exclude aggregate `TOT` or multi-team rows. Check the HTML structure before relying on these selectors after a site change. These are appearance unions, not complete contracts or inventories of players who never appeared.
- Use official club brand and kit-launch pages for visual evidence. Record the exact page and image URL, date, checksum, and representation type. The Blues brand page supplies several concurrent marks and uniform reference images. The Arsenal kit gallery supplies the 2026/27 home reference. ESPN team feeds expose logo URLs. Keep authored schematic SVG and 3D files labeled as illustrative.

## Avoid demonstrated source mistakes

ESPN's historical site roster returned an empty list, and an old-season core team-athlete collection returned current players. An echoed year or a season-shaped URL is insufficient. Check a known historical player or transfer. NBA Stats reset or timed out during the 2026 capture. LockerVision's uniform API returned unauthorized, and NBA Store pages blocked direct capture. Do not bypass those controls or treat those sources as exercised downloads.

Soccer club abbreviations collide: Bayern Munich and Manchester United can both be `MUN`. Reuse EPL and Champions League clubs by their shared ESPN club IDs. Preserve the two NHL players named Elias Pettersson by their official IDs. Inspect identity bindings and resolve ambiguous people before import.

## Capture, regenerate, and verify

Use `scripts/capture_2026.rb` for explicit network capture and `scripts/build_2026.rb` for offline generation. Pass the actual observation date with the required `--as-of` option. `--leagues` limits capture scope. `--refresh` replaces HTTP cache entries. Keep cache files outside importable manifests. The scripts use browser-style public request headers and fail on HTTP errors, missing rosters, and wrong team or season counts.

Run the builder with `--check` to detect missing or differing generated files. A nonzero exit means regeneration does not match. Run Rails `seeds:validate` before import, check that it reports positive file and record counts, and inspect imported coverage afterward. Same-capture replay must create zero records and report zero conflicts.

Current captured numbers belong to player/team periods. A later same-number capture can reuse a covering period while preserving its original date. Changed numbers require an explicit period boundary. Do not infer historical number periods from MLB inventories or NBA appearance tables. Capture disagreements generate no assignment.

NHL date, venue, start-time, and state updates use the explicit `seeds:refresh_nhl_schedule` task after review. Ordinary seed replay preserves existing values. Game identity remains the provider game ID when a date changes. Scheduled fixtures do not manufacture scores, lineups, or appearances.
