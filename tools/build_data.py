import json, os, glob
import sys
B = (sys.argv[1] if len(sys.argv) > 1 else 'mhdb-wilds-data/output/merged').rstrip('/') + '/'
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data.json')
L = lambda f: json.load(open(B + f + '.json'))
def ko(o): return ((o or {}).get('ko') or '').replace('\r\n', '\n').strip()
def en(o): return ((o or {}).get('en') or '').replace('\r\n', '\n').strip()

D = {'ver': '2026-04-14'}
D['st'] = {str(s['game_id']): ko(s['names']) for s in L('Stage')}
D['spc'] = {s['kind']: ko(s['names']) for s in L('Species')}
D['pn'] = {p['part']: (ko(p['names']) or p['part']) for p in L('PartNames')}
D['pn']['hide'] = '외피'

mons = []
for m in L('LargeMonsters'):
    mons.append({
        'id': m['game_id'], 'ko': ko(m['names']), 'en': en(m['names']), 'sp': m['species'],
        'd': ko(m.get('descriptions')), 'f': ko(m.get('features')), 't': ko(m.get('tips')),
        'v': [[v['kind'], ko(v['names'])] for v in m.get('variants', [])],
        'hp': m.get('base_health'), 'loc': m.get('locations', []),
        'sz': [round(m['size'][k]) for k in ('mini', 'base', 'silver', 'gold')] if m.get('size') else None,
        'wk': [[w['kind'], w.get('element') or w.get('status') or w.get('effect'), w.get('level'), ko(w.get('condition'))] for w in m.get('weaknesses', [])],
        'rs': [[r['kind'], r.get('element') or r.get('status') or r.get('effect'), ko(r.get('condition'))] for r in m.get('resistances', [])],
        'pt': [[p['part'], p.get('base_health'), p.get('kinsect_essence'),
                [p['multipliers'][k] for k in ('slash', 'blunt', 'pierce', 'fire', 'water', 'thunder', 'ice', 'dragon', 'stun')]] for p in m.get('parts', [])],
        'rw': [[r['rank'], r['kind'], r['item_id'], r['amount'], r['chance'], r.get('part')] for r in m.get('rewards', [])],
    })
D['m'] = mons

WT = ['GreatSword', 'LongSword', 'SwordShield', 'DualBlades', 'Hammer', 'HuntingHorn', 'Lance', 'Gunlance',
      'SwitchAxe', 'ChargeBlade', 'InsectGlaive', 'Bow', 'LightBowgun', 'HeavyBowgun']
ws = []
for f in WT:
    for w in L('weapons/' + f):
        c = w.get('crafting') or {}
        ex = {}
        for k in ('phial', 'shell', 'shell_level', 'coatings', 'ammo', 'special_ammo', 'kinsect_level', 'melody_id', 'echo_wave_id', 'echo_bubble_id'):
            if w.get(k) is not None: ex[k] = w[k]
        if 'ammo' in ex: ex['ammo'] = [[a['kind'], a['level'], a['capacity'], 1 if a.get('rapid') else 0] for a in ex['ammo']]
        sh = w.get('sharpness')
        ws.append({
            'id': w['game_id'], 't': w['kind'], 'ko': ko(w['names']), 'en': en(w['names']), 'd': ko(w.get('descriptions')),
            'r': w['rarity'], 'atk': w['attack_raw'], 'aff': w['affinity'], 'df': w.get('defense', 0), 'sl': w.get('slots', []),
            'sp': [[s['kind'], s.get('element') or s.get('status'), s['raw'], 1 if s.get('hidden') else 0] for s in w.get('specials', [])],
            'sk': w.get('skills', {}),
            'sh': [sh[k] for k in ('red', 'orange', 'yellow', 'green', 'blue', 'white', 'purple')] if sh else None,
            'hc': w.get('handicraft'),
            'z': c.get('zenny_cost'), 'in': c.get('inputs', {}), 'pv': c.get('previous_id'), 'br': c.get('branches', []),
            'col': c.get('column'), 'row': c.get('row'), 'se': w.get('series_id'), 'ex': ex,
        })
D['w'] = ws
D['wse'] = {str(s['game_id']): ko(s['names']) for s in L('WeaponSeries')}
D['hh'] = {
    'songs': {}, 'mel': {str(m['game_id']): [m['notes'], m['songs']] for m in L('weapons/HuntingHornMelodies')},
    'wave': {str(x['game_id']): ko(x['names']) for x in L('weapons/HuntingHornEchoWaves')},
    'bub': {str(x['game_id']): ko(x['names']) for x in L('weapons/HuntingHornEchoBubbles')},
}
for s in L('weapons/HuntingHornSongs'):
    D['hh']['songs'].setdefault(str(s['effect_id']), ko(s['names']))

arm = []
for a in L('Armor'):
    def bonus(b):
        return [b['skill_id'], [[r['pieces'], r['skill_level']] for r in b['ranks']]] if b else None
    arm.append({
        'id': a['game_id'], 'ko': ko(a['names']), 'en': en(a['names']), 'r': a['rarity'],
        'sb': bonus(a.get('set_bonus')), 'gb': bonus(a.get('group_bonus')),
        'p': [{'k': p['kind'], 'ko': ko(p['names']), 'en': en(p['names']), 'd': ko(p.get('descriptions')),
               'df': [p['defense']['base'], p['defense']['max']],
               'rs': [p['resistances'][k] for k in ('fire', 'water', 'thunder', 'ice', 'dragon')],
               'sl': p.get('slots', []), 'sk': p.get('skills', {}),
               'pr': (p.get('crafting') or {}).get('price'), 'in': (p.get('crafting') or {}).get('inputs', {})} for p in a['pieces']],
    })
D['a'] = arm

D['sk'] = [{'id': s['game_id'], 'ko': ko(s['names']), 'en': en(s['names']), 'd': ko(s.get('descriptions')), 'k': s['kind'], 'ic': s.get('icon'),
            'rk': [[r['level'], ko(r.get('names')), ko(r.get('descriptions')), r.get('set_pieces_required')] for r in s.get('ranks', [])]}
           for s in L('Skill')]
D['j'] = [{'id': j['game_id'], 'ko': ko(j['names']), 'en': en(j['names']), 'd': ko(j.get('descriptions')), 'r': j['rarity'],
           'lv': j['level'], 'on': j['allowed_on'], 'sk': j.get('skills', {}), 'pr': j.get('price'), 'c': j.get('icon_color')} for j in L('Accessory')]
D['am'] = [{'id': x['game_id'], 'rand': 1 if x.get('is_random') else 0,
            'rk': [{'ko': ko(r['names']), 'en': en(r['names']), 'd': ko(r.get('descriptions')), 'r': r.get('rarity'), 'lv': r.get('level'),
                    'pr': r.get('price'), 'sk': r.get('skills', {}), 'in': (r.get('recipe') or {}).get('inputs', {})} for r in x['ranks']]}
           for x in L('Amulet')]
D['it'] = [{'id': i['game_id'], 'ko': ko(i['names']), 'en': en(i['names']), 'd': ko(i.get('descriptions')), 'k': i['kind'], 'r': i.get('rarity'),
            'mx': i.get('max_count'), 'sell': i.get('sell_price'), 'buy': i.get('buy_price'),
            'rc': [[r['amount'], r['inputs']] for r in i.get('recipes', [])], 'ic': i.get('icon'), 'icc': i.get('icon_color')} for i in L('Item')]

# drop empties
for k in ('w', 'a', 'sk', 'j', 'it'):
    before = len(D[k]); D[k] = [x for x in D[k] if x['ko']]
    if before != len(D[k]): print('dropped unnamed', k, before - len(D[k]))
D['am'] = [x for x in D['am'] if x['rk'] and x['rk'][0]['ko']]
s = json.dumps(D, ensure_ascii=False, separators=(',', ':'))
s = s.replace('</', '<\\/')
open(OUT, 'w', encoding='utf-8').write(s)
print('bytes', len(s.encode()), {k: len(v) for k, v in D.items() if isinstance(v, list)})
