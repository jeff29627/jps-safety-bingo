
#!/usr/bin/env python3
"""Draw one unique BSAFE ball per eligible Eastern calendar day, or manually reset."""

import argparse
import json
import secrets
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

STATE = Path(__file__).with_name('state.json')
HOLIDAYS = Path(__file__).with_name('holidays.json')
ET = ZoneInfo('America/New_York')


def label(n):
    return 'BSAFE'[(n - 1) // 15] + '-' + str(n)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--reset', action='store_true')
    p.add_argument(
        '--force',
        action='store_true',
        help='Manual test draw; bypasses schedule and holidays'
    )
    args = p.parse_args()

    now = datetime.now(ET)
    today = now.date().isoformat()

    data = json.loads(STATE.read_text())

    # Manual reset always works, including weekends and holidays.
    if args.reset:
        data = {
            'game_id': data['game_id'] + 1,
            'started_at': today,
            'last_draw_date': None,
            'draws': []
        }
        print('Reset game', data['game_id'])

    else:
        # Automatic draws only occur at midnight Eastern.
        if not args.force and now.hour != 0:
            print('Not midnight Eastern; no draw')
            return

        # Skip weekends and company holidays for automatic draws.
        if not args.force:
            if now.weekday() >= 5:
                print('Weekend; no BSAFE drawing')
                return

            holiday_data = json.loads(HOLIDAYS.read_text())
            holidays = set(holiday_data['holidays'])

            if today in holidays:
                print('JPS Anderson holiday; no BSAFE drawing')
                return

        # Never draw twice on the same Eastern calendar day.
        if data['last_draw_date'] == today:
            print('Already drew today')
            return

        used = {d['number'] for d in data['draws']}
        remaining = sorted(set(range(1, 76)) - used)

        if not remaining:
            print('All 75 balls drawn; manual reset required')
            return

        n = secrets.choice(remaining)

        data['draws'].append({
            'number': n,
            'ball': label(n),
            'date': today,
            'drawn_at': now.isoformat()
        })

        data['last_draw_date'] = today
        print('Drew', label(n))

    STATE.write_text(json.dumps(data, indent=2) + '\n')


if __name__ == '__main__':
    main()
