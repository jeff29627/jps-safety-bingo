#!/usr/bin/env python3
"""Draw one unique bingo ball per Eastern calendar day, or manually reset."""
import argparse
import json
import os
import secrets
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

STATE = Path(__file__).with_name('state.json')
ET = ZoneInfo('America/New_York')

def label(n):
    return 'BINGO'[(n-1)//15] + '-' + str(n)

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--reset', action='store_true')
    p.add_argument('--force', action='store_true', help='Manual draw for testing; not used by scheduler')
    args = p.parse_args()
    now = datetime.now(ET)
    data = json.loads(STATE.read_text())
    if args.reset:
        data = {'game_id': data['game_id']+1, 'started_at': now.date().isoformat(), 'last_draw_date': None, 'draws': []}
        print('Reset game', data['game_id'])
    else:
        today = now.date().isoformat()
        if not args.force and now.hour != 0:
            print('Not midnight Eastern; no draw')
            return
        if data['last_draw_date'] == today:
            print('Already drew today')
            return
        used = {d['number'] for d in data['draws']}
        remaining = sorted(set(range(1, 76)) - used)
        if not remaining:
            print('All 75 balls drawn; manual reset required')
            return
        n = secrets.choice(remaining)
        data['draws'].append({'number': n, 'ball': label(n), 'date': today, 'drawn_at': now.isoformat()})
        data['last_draw_date'] = today
        print('Drew', label(n))
    STATE.write_text(json.dumps(data, indent=2) + '\n')

if __name__ == '__main__':
    main()
