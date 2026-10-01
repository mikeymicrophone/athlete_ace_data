#!/usr/bin/env python3
"""Validate generated rosters against source responses and seed relationships."""
import datetime as dt
import gzip
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOT = ROOT / 'snapshots/2026-27'
manifest = json.loads((SNAPSHOT / 'manifest.json').read_text())
allowed = {'first_name', 'last_name', 'current_position', 'birthdate', 'active', 'photo_urls'}
for league, expected in [('NFL', 32), ('NBA', 30), ('NHL', 32)]:
    entries = [t for t in manifest['teams'] if t['league'] == league]
    assert len(entries) == expected, (league, len(entries))
    assert len({e['file'] for e in entries}) == expected
    ids = set()
    for entry in entries:
        path = ROOT / entry['file']
        content = path.read_bytes()
        assert hashlib.sha256(content).hexdigest() == entry['sha256'], path
        data = json.loads(content)
        assert data['team_name'] == entry['team_name']
        teams = json.loads((path.parent.parent / 'teams.json').read_text())['teams']
        assert data['team_name'] in {t['mascot'] for t in teams}, path
        assert len(data['players']) == entry['player_count'] > 0
        assert len({(p['first_name'], p['last_name']) for p in data['players']}) == len(data['players']), path
        source = json.loads(gzip.decompress((SNAPSHOT / 'sources' / league / f'{entry["source_team_id"]}.json.gz').read_bytes()))
        athletes = source['athletes']
        if athletes and 'items' in athletes[0]:
            athletes = [a for group in athletes for a in group['items']]
        assert {a['id'] for a in athletes} == {p['source_id'] for p in entry['players']}
        for player, identity in zip(data['players'], entry['players']):
            assert player.keys() <= allowed
            assert player['first_name'] and player['last_name'] and player['active'] is True
            assert (player['first_name'], player['last_name']) == (identity['first_name'], identity['last_name'])
            assert identity['source_id'] not in ids, identity
            ids.add(identity['source_id'])
            if 'birthdate' in player:
                dt.date.fromisoformat(player['birthdate'])
    print(f'{league}: validated {len(entries)} teams, {len(ids)} players')
for sport, league in [('football', 'NFL'), ('basketball', 'NBA'), ('hockey', 'NHL')]:
    for path in (ROOT / 'sports' / sport / 'USA' / league / 'players').glob('*.json'):
        json.loads(path.read_text())
print('All roster JSON parses; seed attributes, relationships, source coverage, hashes, and duplicates checked.')
