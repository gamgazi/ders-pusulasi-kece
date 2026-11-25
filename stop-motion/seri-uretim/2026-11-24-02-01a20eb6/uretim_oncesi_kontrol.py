"""Read-only guard: run before every paid/plan image generation call."""
import argparse, json
from pathlib import Path
p = argparse.ArgumentParser()
p.add_argument('--id', required=True)
a = p.parse_args()
root = Path(__file__).resolve().parent
q = json.loads((root / 'uretim_kuyrugu.json').read_text(encoding='utf-8'))
matches = [x for x in q['items'] if x['id'] == a.id]
if len(matches) != 1:
    raise SystemExit('BLOCK: queue identity missing or ambiguous')
item = matches[0]
if item['state'].startswith('BLOCKED') or item['state'] in ('REVIEW_POSSIBLE_EXISTING_ASSET', 'FINAL_ACCEPTED'):
    raise SystemExit('BLOCK: existing or held asset: ' + a.id)
manifest = json.loads((root / 'ilerleme_manifesti.json').read_text(encoding='utf-8'))
if any(x.get('id') == a.id and x.get('final_accepted') for x in manifest['assets']):
    raise SystemExit('BLOCK: accepted manifest asset: ' + a.id)
print(json.dumps({'id': a.id, 'state': item['state'], 'generation_allowed': True}))
