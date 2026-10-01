#!/usr/bin/env python3
"""Fetch season-specific ESPN rosters and emit AthleteAce-compatible seed files."""
import argparse
import concurrent.futures
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
LEAGUES = [('football', 'nfl', 32), ('basketball', 'nba', 30), ('hockey', 'nhl', 32)]
BASE = 'https://site.api.espn.com/apis/site/v2/sports'


def fetch(url):
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=30) as response:
                return json.load(response)
        except Exception:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def encoded(data):
    return json.dumps(data, ensure_ascii=False, indent=2) + '\n'


def collect(sport, league, team, year):
    season = year if league == 'nfl' else year + 1
    url = f'{BASE}/{sport}/{league}/teams/{team["id"]}/roster?season={season}'
    raw = fetch(url)
    if raw.get('status') != 'success' or raw.get('season', {}).get('year') != season:
        raise ValueError(f'Wrong season or failed response: {url}')
    athletes = raw['athletes']
    if athletes and 'items' in athletes[0]:
        athletes = [a for group in athletes for a in group['items']]
    if not athletes:
        raise ValueError(f'Empty roster: {url}')
    players, identities, seen = [], [], set()
    for athlete in athletes:
        aid = athlete['id']
        if aid in seen:
            raise ValueError(f'Duplicate athlete {aid}: {url}')
        seen.add(aid)
        first, last = athlete.get('firstName'), athlete.get('lastName')
        if not first or not last:
            raise ValueError(f'Missing name for {aid}: {url}')
        player = {'first_name': first, 'last_name': last, 'active': True}
        position = athlete.get('position', {}).get('displayName')
        if position:
            player['current_position'] = position
        birthdate = athlete.get('dateOfBirth')
        if birthdate:
            player['birthdate'] = dt.date.fromisoformat(birthdate[:10]).isoformat()
        photo = athlete.get('headshot', {}).get('href')
        if photo:
            player['photo_urls'] = [photo]
        # Do not infer debut/draft years from experience or invent biographies.
        players.append(player)
        identities.append({'source_id': aid, 'first_name': first, 'last_name': last,
                           'status': athlete.get('status'), 'jersey': athlete.get('jersey')})
    paired = sorted(zip(players, identities), key=lambda pair: (pair[0]['last_name'], pair[0]['first_name']))
    players, identities = map(list, zip(*paired))
    mascot = team['name']
    slug = mascot.lower().replace(' ', '_')
    path = f'sports/{sport}/USA/{league.upper()}/players/{slug}.json'
    content = encoded({'team_name': mascot, 'players': players})
    entry = {'league': league.upper(), 'team_name': mascot, 'source_team_id': team['id'],
             'file': path, 'source_url': url, 'source_timestamp': raw.get('timestamp'),
             'season': raw['season'], 'player_count': len(players),
             'sha256': hashlib.sha256(content.encode()).hexdigest(), 'players': identities}
    return path, content, entry, raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--year', type=int, default=2026, help='Season starting year')
    args = parser.parse_args()
    results = []
    for sport, league, expected in LEAGUES:
        teams = [t['team'] for t in fetch(f'{BASE}/{sport}/{league}/teams')['sports'][0]['leagues'][0]['teams']]
        if len(teams) != expected:
            raise ValueError(f'{league}: expected {expected} teams, got {len(teams)}')
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(collect, sport, league, team, args.year) for team in teams]
            league_results = [future.result() for future in futures]
        results.extend(league_results)
        print(f'{league.upper()}: {len(teams)} teams, {sum(r[2]["player_count"] for r in league_results)} players', flush=True)
    # Validate the complete fetch before replacing any seed files.
    for league in ('NFL', 'NBA', 'NHL'):
        ids = [p['source_id'] for r in results if r[2]['league'] == league for p in r[2]['players']]
        if len(ids) != len(set(ids)):
            raise ValueError(f'Player appears on multiple {league} rosters')
    snapshot = ROOT / 'snapshots' / f'{args.year}-{str(args.year + 1)[-2:]}'
    for path, content, entry, raw in results:
        target = ROOT / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content)
        raw_path = snapshot / 'sources' / entry['league'] / f'{entry["source_team_id"]}.json.gz'
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        raw_path.write_bytes(gzip.compress(encoded(raw).encode(), mtime=0))
    (ROOT / 'sports/football/USA/NFL/players/nfl_teams_json.json').unlink(missing_ok=True)
    manifest = {'season': f'{args.year}-{str(args.year + 1)[-2:]}',
                'fetched_at': dt.datetime.now(dt.timezone.utc).isoformat(),
                'scope': 'All players returned by ESPN season-specific team roster endpoints; includes reserve/injured/practice squad and preseason players where listed. active means roster membership, not injury or game eligibility.',
                'teams': [r[2] for r in results]}
    (snapshot / 'manifest.json').write_text(encoded(manifest))


if __name__ == '__main__':
    main()
