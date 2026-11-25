"""Persist an explicit human/model visual review; never auto-accept a candidate."""
import argparse
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('--json', required=True)
a = p.parse_args()
payload = json.loads(a.json)
entry, notes = payload['entry'], payload['notes']
asset_id = entry['id']
assert asset_id.replace('_', '').isalnum(), 'invalid asset id'
assert isinstance(notes.get('decision_notes'), (str, list)), 'explicit notes required'
queue = json.loads((ROOT / 'uretim_kuyrugu.json').read_text(encoding='utf8'))
assert any(x['id'] == asset_id for x in queue['items']), 'id not queued'

def write(path, value):
    tmp = path.with_suffix(path.suffix + '.tmp')
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')
    tmp.replace(path)

write(ROOT / 'inceleme-notlari' / (asset_id + '.json'), notes)
path = ROOT / 'uretim_prompts.json'
prompts = json.loads(path.read_text(encoding='utf8'))
if not any(x['id'] == asset_id and x['prompt'] == entry['prompt'] for x in prompts['prompts']):
    prompts['prompts'].append(entry)
write(path, prompts)
print(json.dumps({'saved': True, 'id': asset_id, 'accepted_by_this_script': False}))
