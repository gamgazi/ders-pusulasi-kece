"""Export reviewed assets, verify native RGB and optionally download pinned GitHub PNGs.
Never generates art, grants artistic approval, commits or pushes automatically.
"""
import argparse,hashlib,json,pathlib,shutil,subprocess,sys,urllib.request
from datetime import datetime, timezone, timedelta
import numpy as np
from PIL import Image
from scipy import ndimage
ROOT=pathlib.Path(__file__).resolve().parent
BATCH='stop-motion/seri-uretim/2026-11-24-02-01a20eb6'
def load(p):return json.loads(p.read_text(encoding='utf8'))
def save(p,j):
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def public(j):
    if isinstance(j,dict):return {k:public(v) for k,v in j.items()}
    if isinstance(j,list):return [public(v) for v in j]
    if isinstance(j,str) and (j.startswith('C:\\') or j.startswith('C:/')):return pathlib.PureWindowsPath(j).name
    return j
def main():
    p=argparse.ArgumentParser();p.add_argument('--repo',required=True);p.add_argument('--verify-commit');p.add_argument('--verify-only',action='store_true');a=p.parse_args()
    repo=pathlib.Path(a.repo).resolve();dest=repo/BATCH
    reports=[load(p) for p in sorted((ROOT/'adaylar').glob('*/*/qa.json'))]
    accepted=[r for r in reports if r['final_accepted']]
    if len({r['id'] for r in accepted})!=len(accepted):raise SystemExit('Duplicate accepted ID')
    if len({r['metrics']['sha256'] for r in accepted})!=len(accepted):raise SystemExit('Duplicate accepted PNG')
    bysha={r['metrics']['sha256']:r for r in reports}
    proof_path=ROOT/'AKTARIM_KANITI.json'
    proof=load(proof_path) if proof_path.exists() else {'checkpoints':[]}
    if a.verify_commit:
        checkpoint={'commit':a.verify_commit,'assets':[],'errors':[],'later_assets_not_in_checkpoint':[]}
        published=set(subprocess.check_output(['git','ls-tree','-r','--name-only',a.verify_commit,'--','stop-motion'],cwd=repo,text=True,encoding='utf8').splitlines())
        known_hashes={x['sha256'] for c in proof['checkpoints'] for x in c['assets']}
        for r in accepted:
            if r['metrics']['sha256'] in known_hashes:continue
            if 'stop-motion/'+r['final_path'] not in published:
                checkpoint['later_assets_not_in_checkpoint'].append(r['id']);continue
            rel='stop-motion/'+r['final_path'];url='https://raw.githubusercontent.com/gamgazi/ders-pusulasi-kece/'+a.verify_commit+'/'+rel
            try:
                data=urllib.request.urlopen(url,timeout=45).read();digest=hashlib.sha256(data).hexdigest()
                if digest!=r['metrics']['sha256']:raise ValueError('Downloaded SHA-256 mismatch')
                checkpoint['assets'].append({'id':r['id'],'path':rel,'sha256':digest,'bytes':len(data),'downloaded_and_verified':True})
            except Exception as e:checkpoint['errors'].append({'id':r['id'],'error':str(e)})
        proof['checkpoints'].append(checkpoint);save(proof_path,proof)
        if checkpoint['errors']:raise SystemExit(json.dumps(checkpoint['errors'],ensure_ascii=False))
        if a.verify_only:
            print(json.dumps({'new_pngs_download_verified':len(checkpoint['assets']),'commit':a.verify_commit}));return
    verified={}
    for c in proof['checkpoints']:
        for x in c['assets']:verified[x['sha256']]=c['commit']
    validation=[]
    for r in reports:
        processing=ROOT/'teknik-islem'/f"{r['id']}_{r['revision']}.processing.json"
        if processing.exists():r['technical_processing']=load(processing)
        r['generation_type']='Digital simulation of marker on white paper; not physically photographed craft'
        r['approval_authority']='Assistant per-image QA under user-delegated routine artistic acceptance'
        r['master_blob_sha']='2e4ce3827c240d26085ea5d08116b8785cb21fbe'
        if r['final_accepted']:
            m=r['metrics'];proc=r['technical_processing'];raw=bysha[proc['source_sha256']]
            original=np.array(Image.open(ROOT/raw['candidate_path']))
            final=np.array(Image.open(ROOT/r['final_path']))
            bb=proc.get('source_crop_bbox')
            if bb is None:
                labs,n=ndimage.label(original[:,:,3]>=proc.get('alpha_threshold',16),structure=np.ones((3,3)))
                sizes=np.bincount(labs.ravel());sizes[0]=0;yy,xx=np.where(labs==sizes.argmax());bb=[xx.min(),yy.min(),xx.max()+1,yy.max()+1]
            x,y,X,Y=bb;fx,fy,fX,fY=m['bbox']
            same=bool(np.array_equal(original[y:Y,x:X,:3],final[fy:fY,fx:fX,:3]))
            if not same or sha(ROOT/r['final_path'])!=m['sha256']:raise SystemExit('Native RGB or file hash changed: '+r['id'])
            r['repository_png_path']='stop-motion/'+r['final_path']
            r['source_artwork_use_limit']='Native size or smaller; transparent 4K canvas is not native 4K detail'
            r['github_binary_uploaded']=m['sha256'] in verified
            if r['github_binary_uploaded']:r['upload_verified_commit']=verified[m['sha256']]
            validation.append({'id':r['id'],'sha256':m['sha256'],'native_rgb_preserved':same,'github_download_sha256_match':r['github_binary_uploaded']})
            target=repo/r['repository_png_path'];target.parent.mkdir(parents=True,exist_ok=True)
            if target.exists() and sha(target)!=m['sha256']:raise SystemExit('Refusing canonical overwrite '+str(target))
            if not target.exists():shutil.copy2(ROOT/r['final_path'],target)
            record=public(r);record['status']='ARTISTIC_ACCEPTED';record['batch_path']=BATCH
            record_path=repo/'stop-motion/uretim-kayitlari'/f"2026-11-24_{r['id']}.json"
            if record_path.exists() and load(record_path).get('batch_path')!=BATCH:raise SystemExit('Record belongs to another batch')
            save(record_path,record)
        save(ROOT/'adaylar'/r['id']/r['revision']/'qa.json',r)
        save(ROOT/'uretim-kayitlari'/f"2026-11-24_{r['id']}_{r['revision']}.json",r)
    save(ROOT/'denetim/son_dogrulama.json',{'accepted':len(accepted),'checks':validation})
    count=len(accepted);remote=sum(x['github_download_sha256_match'] for x in validation)
    text=f'''ROOTS & TALKS — SERİ ÜRETİM 02 / ARA KALİTE RAPORU
Seri başlangıcı: 24 Kasım 2026. Rapor: {datetime.now(timezone(timedelta(hours=3))).isoformat(timespec='seconds')}.

Bu seri: {count} kabul edilmiş ayrı PNG. Önceki değişmez seriyle toplam: {count+6}.
GitHub'dan indirilerek SHA-256 eşleştirilen bu seri PNG sayısı: {remote}.
Kütüphanenin tamamı bitmedi; bu kayıt üretimi durduran bir teslim değildir.

Her kabul, gerçek son PNG'nin yeşil/mor fon ve alfa denetimine dayanır.
Tek nesne, yoğun keçeli kalem, düzensiz çocuk çizgisi, değişken beyaz makas
payı ve kâğıt kıvrımı/kat izi için ayrı gerekçe inceleme-notlari içindedir.
Alfa dışı sıfırdır; yedi eşikte nesne tek bağlantılıdır. Retler saklanır.
Çizimler fiziksel kâğıdın dijital simülasyonudur.

Kaynak boyutları dosya bazında kayıttadır; çoğunluğu 1672×941 pikseldir.
Kullanıcının yetkisiyle alfa temizlenir,
özgün RGB pikselleri büyütülmeden 3840×2160 şeffaf tuvale yerleştirilir.
Bu özgün 4K ayrıntı değildir; nesneler doğal boyutunda veya küçük kullanılır.
RGB korunumu her kabul edilmiş dosyada yeniden karşılaştırıldı.

Kaynak denetimi 4158 benzersiz R/K kartı doğruladı (R3434/K724); mevcut
keçe kartları tekrar üretilmedi. {len(load(ROOT/'uretim_kuyrugu.json')['items'])} öğelik bu sıra JSON konumlarıyla doğrulandı.
35 Ders Pusulası kaynağındaki bütün derslerin sahne ayrıştırması bitmedi.
Tarihsel Solmuş Çiçek ve Yatak R02 PNG'leri erişilemedi; yeniden üretilmedi
ve bu oturumda görsel kontrol edilmiş sayılmadı. Arka plan envanteri taslaktır.

Canlı kabul/ret, sıradaki nesne ve aktarım kanıtı ayrı JSON kayıtlarındadır.
'''
    (ROOT/'KALITE_RAPORU.txt').write_text(text,encoding='utf8')
    (ROOT/'.gitattributes').write_text('* -text\n',encoding='utf8')
    manifest=load(ROOT/'ilerleme_manifesti.json');manifest['upload']={'status':'ALL_CURRENT_PNGS_DOWNLOAD_VERIFIED' if remote==count else 'CHECKPOINT_PARTIAL_OR_PENDING','verified_png_count':remote,'accepted_png_count':count,'batch_path':BATCH};save(ROOT/'ilerleme_manifesti.json',manifest)
    subprocess.run([sys.executable,'-X','utf8',str(ROOT/'seri_uretim.py'),'rebuild'],check=True)
    for source in ROOT.rglob('*'):
        if not source.is_file() or '__pycache__' in source.parts or source.name=='SHA256SUMS.txt':continue
        target=dest/source.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True)
        if source.suffix=='.json':save(target,public(load(source)))
        elif source.suffix in ['.png','.jpg']:
            if target.exists() and sha(target)!=sha(source):raise SystemExit('Immutable image differs '+str(target))
            if not target.exists():shutil.copy2(source,target)
        else:shutil.copy2(source,target)
    lines=[sha(p)+'  '+p.relative_to(dest).as_posix() for p in sorted(dest.rglob('*')) if p.is_file() and p.name!='SHA256SUMS.txt']
    (dest/'SHA256SUMS.txt').write_text('\n'.join(lines)+'\n',encoding='utf8')
    print(json.dumps({'accepted':count,'verified_remote':remote,'exported_files':len(lines),'batch':BATCH}))
if __name__=='__main__':main()
