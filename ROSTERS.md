# 2026–27 roster snapshot

Fetched October 1, 2026 from ESPN's season-specific team roster API for all 32 NFL, 30 NBA and 32 NHL teams. NFL uses the 2026 season; NBA and NHL use the 2027 API season, labeled 2026–27.

The existing `sports/[sport]/USA/[league]/players/*.json` files contain one team per file, with attributes supported by AthleteAce's `SeedPlayers` importer. The malformed concatenated NFL file has been replaced with 32 individual files. Utah Mammoth has a team definition and Central Division membership; the empty historical Coyotes file remains.

## Scope

These are the complete rosters returned by ESPN at fetch time, not final opening-night or NFL 53-player lists. NBA rosters are preseason lists. NFL and NHL responses can include reserves, injured players, practice-squad players, or other roster designations. `active: true` means included on the source roster, not healthy or eligible for a game. Original status and jersey numbers are retained in the manifest and source snapshots rather than passed as unsupported Player attributes.

No draft/debut years or biographies are inferred. Birthdates, positions and headshots are included only when returned by the source. This is an ESPN snapshot, not an independently certified official league roster.

## Refresh and validate

Requires Python 3 and internet access; no third-party packages or API key:

```sh
python scripts/generate_rosters.py --year 2026
python scripts/validate_rosters.py
```

The generator checks team counts, season labels, nonempty rosters and duplicate source IDs before writing seed files. The validator checks JSON, team relationships, supported attributes, dates, duplicates, source coverage and SHA-256 hashes.

`snapshots/2026-27/manifest.json` records per-team URLs, source timestamps, season labels, player identities, statuses and file hashes. `snapshots/2026-27/sources/` contains compressed original responses. These are outside the application's player seed glob.

## Import behavior

AthleteAce loads these files through its existing `sports/**/players/*.json` seed glob. Its importer matches players by first name, last name and team. Reseeding adds or updates these records, but does not remove former players or reconcile transfers across existing records. Importing into an existing database therefore does not by itself produce a clean current-roster database. No application database was modified during generation.
