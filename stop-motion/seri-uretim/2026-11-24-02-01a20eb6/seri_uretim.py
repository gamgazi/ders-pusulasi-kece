"""Offline serial ingestion and QA. Never calls a paid service or accepts art automatically."""
import argparse, hashlib, json, pathlib, shutil
import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

ROOT=pathlib.Path(__file__).resolve().parent
def write(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def measure(path):
    im=Image.open(path); im.load(); original_mode=im.mode
    a=np.asarray(im.convert('RGBA'))[:,:,3]
    counts={}; largest={}; tiny={}
    for threshold in [1,16,32,64,128,192,250]:
        lab,n=ndimage.label(a>=threshold,structure=np.ones((3,3)))
        areas=np.bincount(lab.ravel())[1:]
        counts[str(threshold)]=int(n)
        largest[str(threshold)]=int(areas.max()) if len(areas) else 0
        tiny[str(threshold)]=int(areas[areas<32].sum())
    bbox=im.convert('RGBA').getchannel('A').getbbox()
    return {'format':im.format,'mode':original_mode,'dimensions':list(im.size),'native_4k':im.size==(3840,2160),'alpha_min':int(a.min()),'alpha_max':int(a.max()),'zero_alpha_fraction':float((a==0).mean()),'opaque_fraction':float((a==255).mean()),'bbox':list(bbox) if bbox else None,'transparent_edges':not any([a[0].any(),a[-1].any(),a[:,0].any(),a[:,-1].any()]),'components_all_pixels':counts,'largest_component_pixels':largest,'tiny_component_pixels':tiny,'sha256':sha(path),'bytes':path.stat().st_size}
def previews(path,directory):
    im=Image.open(path).convert('RGBA')
    for name,color in [('yesil',(30,170,85,255)),('mor',(128,45,165,255)),('koyu',(25,30,40,255))]:
        bg=Image.new('RGBA',im.size,color); bg.alpha_composite(im)
        bg.convert('RGB').save(directory/f'{name}.jpg',quality=95)
        bbox=im.getchannel('A').getbbox()
        if bbox:
            crop=(max(0,bbox[0]-32),max(0,bbox[1]-32),min(im.width,bbox[2]+32),min(im.height,bbox[3]+32))
            bg.crop(crop).convert('RGB').save(directory/f'{name}_detay.jpg',quality=97)
    im.getchannel('A').save(directory/'alfa.png')
    alpha_preview=im.getchannel('A'); alpha_preview.thumbnail((960,540)); alpha_preview.save(directory/'alfa_onizleme.png')
def ingest(args):
    queue=json.loads((ROOT/'uretim_kuyrugu.json').read_text(encoding='utf-8'))
    item=next(x for x in queue['items'] if x['id']==args.id)
    if item['state'].startswith('BLOCKED') or item['state'] in ['REVIEW_POSSIBLE_EXISTING_ASSET','FINAL_ACCEPTED']: raise SystemExit('Dedup/reference gate blocks production')
    folder=ROOT/'adaylar'/args.id/args.revision
    folder.mkdir(parents=True,exist_ok=True)
    target=folder/f'{args.id}_{args.revision}.png'
    if target.exists(): raise SystemExit('Existing revision is immutable; use a new revision')
    shutil.copy2(args.source,target)
    metrics=measure(target)
    if args.origin_qa:
        origin=json.loads(pathlib.Path(args.origin_qa).read_text(encoding='utf-8'))
        metrics['original_generated_dimensions']=origin['metrics']['dimensions']
        metrics['native_4k']=origin['metrics'].get('native_4k',False)
        metrics['source_artwork_upscaled']=False
        metrics['source_revision']=origin['revision']
    history=json.loads((ROOT/'denetim/uretim_kayitlari_eslestirme.json').read_text(encoding='utf-8'))
    matches=[x['record'] for x in history if x['declared_final_sha256']==metrics['sha256']]
    metrics['duplicate_historical_sha256_matches']=matches
    metrics['technical_rgba_pass']=metrics['mode']=='RGBA' and metrics['alpha_min']==0 and metrics['alpha_max']==255 and metrics['transparent_edges'] and all(n==1 for n in metrics['components_all_pixels'].values()) and not matches
    metrics['master_canvas_target_pass']=metrics['dimensions']==[3840,2160]
    report={'id':args.id,'revision':args.revision,'status':'AWAITING_VISUAL_REVIEW','source':str(pathlib.Path(args.source).resolve()),'candidate_path':target.relative_to(ROOT).as_posix(),'metrics':metrics,'curriculum':item['source_evidence'],'felt_cards_preserved':item['felt_cards_preserved'],'final_accepted':False,'visual_review':None}
    write(folder/'qa.json',report); previews(target,folder)
    print(json.dumps(report,ensure_ascii=False))
def review(args):
    folder=ROOT/'adaylar'/args.id/args.revision
    report=json.loads((folder/'qa.json').read_text(encoding='utf-8'))
    notes=json.loads(pathlib.Path(args.notes).read_text(encoding='utf-8'))
    required=['one_object','object_identity','dense_marker_ink','childlike_irregular_lines','variable_white_scissor_border','physical_paper_curl_or_crease','no_embedded_backdrop','no_floating_shadow','reviewed_green_purple_and_alpha']
    if any(k not in notes for k in required): raise SystemExit('Missing visual criteria')
    art=all(notes[k] is True for k in required)
    report['visual_review']=notes
    report['artistic_accepted']=art
    full=art and report['metrics']['technical_rgba_pass'] and report['metrics']['master_canvas_target_pass']
    report['final_accepted']=full
    report['status']='FINAL_ACCEPTED' if full else ('NATIVE_ASSET_PASS_4K_TARGET_PENDING' if art and report['metrics']['technical_rgba_pass'] else 'REJECTED')
    if full:
        queue=json.loads((ROOT/'uretim_kuyrugu.json').read_text(encoding='utf-8'))
        item=next(x for x in queue['items'] if x['id']==args.id)
        final=ROOT/item['category']/(args.id+'.png'); final.parent.mkdir(parents=True,exist_ok=True)
        if final.exists(): raise SystemExit('Final file already exists; cannot overwrite')
        shutil.copy2(ROOT/report['candidate_path'],final)
        report['final_path']=final.relative_to(ROOT).as_posix()
        item['state']='FINAL_ACCEPTED'
        item['accepted_revision']=args.revision
        item['final_sha256']=report['metrics']['sha256']
        for waiting in queue['items']:
            if waiting['state']=='WAITING_PREVIOUS_POSE' and waiting.get('dependency','').startswith(args.id): waiting['state']='READY_REFERENCE_AVAILABLE'
        write(ROOT/'uretim_kuyrugu.json',queue)
    write(folder/'qa.json',report)
    write(ROOT/'uretim-kayitlari'/f'2026-11-24_{args.id}_{args.revision}.json',report)
    rebuild()
    print(json.dumps({'id':args.id,'revision':args.revision,'status':report['status'],'final_accepted':full},ensure_ascii=False))
def rebuild():
    reports=[json.loads(p.read_text(encoding='utf-8')) for p in sorted((ROOT/'adaylar').glob('*/*/qa.json'))]
    previous=json.loads((ROOT/'ilerleme_manifesti.json').read_text(encoding='utf-8')) if (ROOT/'ilerleme_manifesti.json').exists() else {}
    manifest={'schema_version':1,'date':'2026-11-24','workflow':'one object, one call, one PNG, technical QA, visual QA, immutable decision, hash, upload and readback','complete_library':False,'png_revisions':len(reports),'image_generation_calls':sum('source_revision' not in x['metrics'] for x in reports),'final_accepted':sum(x['final_accepted'] for x in reports),'rejected':sum(x['status']=='REJECTED' for x in reports),'native_asset_pass_4k_pending':sum(x['status']=='NATIVE_ASSET_PASS_4K_TARGET_PENDING' for x in reports),'assets':reports,'historical_recheck':{'cicek_solmus_001':'PNG_UNAVAILABLE_NOT_REVIEWED','yatak_mavi_yandan_001_r02':'PNG_UNAVAILABLE_NOT_REVIEWED'},'upload':previous.get('upload',{'status':'NOT_YET_ATTEMPTED'})}
    verified_count=sum(x['final_accepted'] and x.get('github_binary_uploaded',False) for x in reports)
    manifest['upload'].update(verified_png_count=verified_count,accepted_png_count=manifest['final_accepted'],status='ALL_CURRENT_PNGS_DOWNLOAD_VERIFIED' if verified_count==manifest['final_accepted'] and verified_count else 'CHECKPOINT_PARTIAL_OR_PENDING')
    write(ROOT/'ilerleme_manifesti.json',manifest)
    state_path=ROOT/'DEVAM_KAYDI.json'
    if state_path.exists():
        state=json.loads(state_path.read_text(encoding='utf-8'))
        queue=json.loads((ROOT/'uretim_kuyrugu.json').read_text(encoding='utf-8'))
        remaining=[x for x in queue['items'] if x['state']!='FINAL_ACCEPTED']
        state.update(state='SERIAL_PRODUCTION_ACTIVE',accepted_in_this_series=manifest['final_accepted'],total_accepted_in_work=state.get('first_batch_accepted',0)+manifest['final_accepted'],remaining_in_reviewed_queue=len(remaining),next_asset=remaining[0]['id'] if remaining else None)
        write(state_path,state)
    lines=[]
    for p in sorted(ROOT.rglob('*')):
        if p.is_file() and p.name!='SHA256SUMS.txt' and '__pycache__' not in p.parts: lines.append(f'{sha(p)}  {p.relative_to(ROOT).as_posix()}')
    (ROOT/'SHA256SUMS.txt').write_text('\n'.join(lines)+'\n',encoding='utf-8')
if __name__=='__main__':
    parser=argparse.ArgumentParser(); sub=parser.add_subparsers(dest='action',required=True)
    p=sub.add_parser('ingest');p.add_argument('--id',required=True);p.add_argument('--revision',required=True);p.add_argument('--source',required=True);p.add_argument('--origin-qa')
    p=sub.add_parser('review');p.add_argument('--id',required=True);p.add_argument('--revision',required=True);p.add_argument('--notes',required=True)
    sub.add_parser('rebuild');args=parser.parse_args()
    {'ingest':ingest,'review':review,'rebuild':lambda _:rebuild()}[args.action](args)
