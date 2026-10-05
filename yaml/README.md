# YAML seasonal catalog pilot

This is a sourced sample for `micharisma-seeds/v1`, namespace `MIC`, catalog `ALA`. It adds new YAML files alongside the existing JSON library. It is not a complete roster catalog or an assertion that all four leagues are ready for launch.

The ten completed main-league seasons are NBA, NHL, and EPL `2016_2017` through `2025_2026`, plus NFL `2016` through `2025`. One additional Championship season supports Fulham's promotion example. `Season.label` preserves the complete label. Its `year` reference is the starting calendar year; an NFL label uses that season's designated year. Calendar dates are omitted rather than inferred.

## Coverage

| Records | Count | Coverage |
| --- | ---: | --- |
| Country | 2 | United States and United Kingdom jurisdiction anchors |
| Sport | 4 | Basketball, Football, Hockey, Soccer |
| League | 5 | NBA, NFL, NHL, EPL, and the secondary EFL Championship |
| Year | 10 | 2016 through 2025 |
| Season | 41 | Ten per main league; Championship 2021_2022 |
| Team | 8 | Two NBA, three NFL, two NHL, one English football club |
| Player | 3 | Josh Hart, Emmanuel Sanders, Nick Leddy |
| Campaign | 10 | Annual team attributes for the examples below |
| Activation | 6 | Two same-season memberships for each sampled traded player |
| Total catalog definitions | 89 | Samples only; no complete team roster is claimed |

NBA Hart `2022_2023`: Portland and New York. NFL Sanders `2019`: Denver and San Francisco. NHL Leddy `2021_2022`: Detroit and St. Louis. Raiders city history: Oakland in `2019`, Las Vegas in `2020`. Fulham league history: Championship `2021_2022`, EPL `2022_2023`.

An Activation asserts membership in that team's season, even when the player departed before the season ended. Both trade-side memberships remain. It does not assert membership for every day, opening-day presence, a particular game appearance, or a contract's terms. These files supply six membership observations; they do not enumerate the complete full-season unions for the sampled teams. Further roster captures must add the omitted people.

## Files and scopes

`foundation.yaml`, `years.yaml`, `seasons_*.yaml`, `teams.yaml`, and `players.yaml` define shared anchors. The five named sample files define Campaigns and membership observations. The importer indexes definitions across the selected files before resolving dependencies; filename order must not determine identity.

Each catalog file declares `format`, `namespace`, `catalog`, `source`, `scope`, and `groups`. Each group declares a scope and records. A record declares `type`, a full catalog-relative `code`, an `attributes` mapping, and a `references` mapping. It may additionally declare aliases or override its inherited source. There are no local database IDs in these references.

File scope and group scope provide relationship context; a group's explicit value replaces the corresponding inherited value. Records remain individually coded. For example:

```yaml
scope:
  sport: SPORT-BKT
  league: BKT-LEAGUE-NBA
  year: YEAR-2022
groups:
  - scope:
      team: BKT-NBA-TEAM-POR
    records:
      - type: Activation
        code: BKT-NBA-SEASON_2022_2023-TEAM-POR-PLAYER-HART_JOSH
        attributes: {}
        references:
          player: BKT-NBA-LAL-2017-HART_JOSH
```

The adapter derives Campaign team and Season from team/league/year context, and derives an Activation's Campaign from the same context. It resolves the explicit Player code, which is defined once in `players.yaml`. Player groups carry independent Sport context and no current team assignment. A debut-team component in a Player code is a historical identity anchor, not a request to overwrite `Player.team`.

Annual display name, territory, mascot, and abbreviation belong to Campaign. The Raiders' `FTB-NFL-TEAM-RAIDERS` identity has OAK and LV aliases and two separate annual snapshots. Fulham's `SOC-EPL-TEAM-FUL` remains one club when its Campaign league changes. The EPL component in that issued Team code is its catalog qualification; a Championship Campaign must not create a duplicate Team or rewrite its current league association.

Country jurisdiction references follow the current JSON catalog's United States/United Kingdom scope. They do not assert exclusive participation geography or conflate the English football pyramid with all UK football. No stadium, city, division, conference, logo, or contract facts have been invented to fill missing fields.

`entity_sequences.yaml` keeps numeric recipes in exactly two levels. Its string keys `"01"`/`"10"` form external sequence `01_10`; zero padding is preserved. Optional `terminology` names the numbers: family `athletes` is 5 and member `season_roster` is 22, so the named pair resolves to `05_22`. Member names are scoped to their family. The initial sequence is `[Sport, League, Conference, Division, Year, Team]`, with smaller profiles added for optional scoped lookup. Canonical definition codes are issued references and are not pure positional sequence strings, so this pilot does not apply `entity_sequence` annotations to them. Underscores stay inside components such as `HART_JOSH` and `SEASON_2022_2023`; dashes separate components.

For subsequent manifests, `entity_sequence: "05_22"`, `[5, 22]`, and `[athletes, season_roster]` select the same lookup. Alternatively set a family at file scope (`entity_sequence: athletes`) and members in groups (`entity_sequence: season_roster`). A member must be selected before records are defined. Names do not change the issued code or recipe meaning.

## Evidence and replay boundary

Every record inherits an official source URL or carries its own. Known publication dates are strings under `source.published_on`; undated pages omit that field. Source notes identify the sample and season-union meaning. Primary sources include the [NBA season index](https://www.nba.com/news/history-season-recaps-index), [NFL historical standings](https://www.nfl.com/standings/league/2025/REG), [NHL records](https://records.nhl.com/standings/all-time-standings), and [Premier League season history](https://www.premierleague.com/en/premier-league-explained).

The membership examples cite the [Knicks Hart announcement](https://www.nba.com/knicks/news/new-york-knicks-acquire-josh-hart), [Broncos Sanders announcement](https://www.denverbroncos.com/news/broncos-agree-trade-emmanuel-sanders-to-49ers-draft-picks), and [Blues Leddy announcement](https://www.nhl.com/blues/news/blues-acquire-leddy-witkowski-from-red-wings-332085830). The separate annual histories cite the [official Raiders relocation announcement](https://www.raiders.com/news/las-vegas-raiders-silver-and-black-officially-welcomed-to-the-silver-state) and [Fulham promotion announcement](https://www.premierleague.com/en/news/2567479).

Ordinary replay must create missing records, retain existing values and memberships, add conflict-free aliases, and report differences. An omitted player is not a deletion instruction. The source-backed files support a preservation-oriented importer; the data alone does not make the legacy JSON seeders preservation-safe, reconcile duplicate live franchises, or alter existing database associations.

The AthleteAce integration tests import this whole pilot into the test database and verify replay, file relocation, preserved edits, missing-row reconstruction with changed numeric IDs, and the sample seasonal relationships. The development and deployed databases are not altered by those tests. See AthleteAce's `docs/yaml-seed-library.md` for import commands and remaining launch work.
