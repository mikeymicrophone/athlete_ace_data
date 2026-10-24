# Pseudo leagues

This bundle contains fictional basketball, hockey, and soccer leagues for developing seasonal play and game participation. All names, dates, contracts, results, and titles are generated. They make no historical sports claims. Shared Sport, Country, and Year codes reuse the sourced catalog's identities; all other codes begin with `PSEUDO-`.

The `pseudo` Git branch contains this bundle alongside the unchanged sourced library in `yaml/`. The normal seed task still selects `yaml/`. Select `pseudo/` explicitly to import these leagues.

## Coverage

Each league has eight teams, two conferences, four divisions, and three calendar-year seasons, 2022 through 2024. The same team identities continue across seasons. Each Campaign records its conference and division; this bundle does not create current Team Membership rows.

| League | Abbreviation | Players per team | Regular games per season | Playoff games per season |
| --- | --- | ---: | ---: | ---: |
| Horizon Basketball League | HBL | 12 | 56 | 9 |
| Northern Ice League | NIL | 24 | 56 | 9 |
| Riverside Football League | RFL | 23 | 56 | 3 |

There are 24 Teams, 472 Players, 72 Campaigns, 1,416 Contracts, 1,416 Activations, 1,416 Stints, and 567 Games. Each team has a club Organization and affiliation. Each season has a regular-season Contest and playoff Contest, with separate table and playoff titles.

Each player has one calendar-year contract, Activation, and Stint per season. The first two roster slots move to the next team each offseason. These moves preserve the Player identity and position, and give 48 players a three-team history. Contract values are fictional USD amounts. No movement Transactions, roster observations, or injury records are generated. `Player.team` stays unset; assignments come from dated participation records.

The regular schedule is a complete double round robin over 14 weekly matchdays, starting February 5. Every pair meets once at each team's venue, with no team booked twice on the same date. All three fictional leagues award three table points for a win and one for a draw. Basketball and hockey games have no draws. Ties in table points use ascending team code.

The top four teams enter June playoffs, seeded first versus fourth and second versus third. Basketball and hockey use three-game semifinal and final series, each ending 2–1. Soccer uses single games. Scores and home or away roles live in each Game Contestant's `tiebreakers` object. Table Contestants store points there and use `placing` for rank. A Game's ContestGame membership records its matchweek or playoff round, series, and game number.

No Appearance records exist in this bundle. An Activation or Stint supplies a candidate player's assignment, not proof that the player appeared in any Game. Appearance selection, starters, substitutes, minutes, and statistics remain the next design step.

## Regenerate and check

Run these commands from the data repository. The generator uses Ruby's standard library and overwrites only its named manifests and copied sequence registry in `pseudo/`. To change generated data, edit [the generator](../scripts/build_pseudo.rb) and regenerate.

```sh
ruby scripts/build_pseudo.rb
ruby scripts/build_pseudo.rb --check
python -m unittest discover -s tools -p 'test_*.py'
python tools/validate_seeds.py pseudo --registry pseudo/entity_sequences.yaml
```

Use a Python environment installed with `tools/requirements.txt`, as described in [Contributing seed data](../CONTRIBUTING.md). Generation prints record counts. `--check` exits nonzero if any generated file differs or is missing. Unit checks must report 12 tests and `OK`; failures return nonzero. Schema validation must report 13 manifests and zero failures. Schema validation does not resolve references or exercise database constraints.

From the AthleteAce application checkout, validate and import this bundle with:

```sh
SEED_LIBRARY_ROOT="$PWD/db/seeds/athlete_ace_data/pseudo" mise exec -- ruby -S bundle exec rails seeds:validate
SEED_LIBRARY_ROOT="$PWD/db/seeds/athlete_ace_data/pseudo" mise exec -- ruby -S bundle exec rails seeds:import
```

Both commands return nonzero on failure. Preflight must report 7,313 records, 7,313 codes, and 13 files. Import creates missing records and preserves existing values. Its report must have zero conflicts for an unedited bundle. Repeating the import must create zero records with zero conflicts. Selecting this bundle does not clear existing catalog data. Use `seeds:import` directly to exercise the library without running the default `db:seed` orchestration.
