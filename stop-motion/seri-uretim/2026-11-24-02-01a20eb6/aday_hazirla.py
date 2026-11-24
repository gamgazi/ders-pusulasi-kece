"""Prepare exactly one candidate; never generate or give automatic artistic approval."""
import argparse,importlib.util,json,pathlib,subprocess,sys,shutil
root=pathlib.Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--id',required=True);p.add_argument('--source',required=True);p.add_argument('--raw-revision',default='r01');p.add_argument('--final-revision',default='r02');a=p.parse_args()
def call(script,*args):
    result=subprocess.run([sys.executable,'-X','utf8',str(root/script),*args],capture_output=True,text=True,encoding='utf-8')
    if result.returncode:
        print(result.stdout);print(result.stderr);raise SystemExit(result.returncode)
call('seri_uretim.py','ingest','--id',a.id,'--revision',a.raw_revision,'--source',a.source)
rawdir=root/'adaylar'/a.id/a.raw_revision;raw=json.loads((rawdir/'qa.json').read_text(encoding='utf8'))
raw['status']='REJECTED' if not raw['metrics']['technical_rgba_pass'] or not raw['metrics']['master_canvas_target_pass'] else 'AWAITING_VISUAL_REVIEW'
raw['visual_review']={'state':'NOT_FINAL_REVIEWED','notes':'Generated view inspected for subject; technical input fails delivery gate. Final corrected PNG must be visually inspected on both colored backgrounds.'}
(rawdir/'qa.json').write_text(json.dumps(raw,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
record=root/'uretim-kayitlari'/f'2026-11-24_{a.id}_{a.raw_revision}.json';record.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(rawdir/'qa.json',record)
processed=root/'teknik-islem'/f'{a.id}_{a.final_revision}.png'
call('teknik_duzeltme.py',str(rawdir/f'{a.id}_{a.raw_revision}.png'),str(processed))
call('seri_uretim.py','ingest','--id',a.id,'--revision',a.final_revision,'--source',str(processed),'--origin-qa',str(rawdir/'qa.json'))
report=json.loads((root/'adaylar'/a.id/a.final_revision/'qa.json').read_text(encoding='utf8'))
print(json.dumps({'id':a.id,'raw_status':raw['status'],'final_candidate':report['metrics'],'visual_review':'REQUIRED'},ensure_ascii=False))
