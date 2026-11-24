"""Append exact Fidan source evidence after canonical record/file reconciliation."""
import json,pathlib,hashlib,unicodedata,re,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
BASE=ROOT.parent.parent
REPO=BASE/'work/repository'
SOURCE='pusula/ders-pusulasi/4-6-fidan.json'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def write(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def norm(s):return re.sub('[^a-z0-9]+','_', ''.join(c for c in unicodedata.normalize('NFKD',s.casefold().replace('ı','i')) if not unicodedata.combining(c))).strip('_')
def matches(a,s):return ('_'+a+'_') in ('_'+norm(s)+'_')
def leaves(o,p=''):
    if isinstance(o,dict):
        for k,v in o.items():yield from leaves(v,p+'/'+k)
    elif isinstance(o,list):
        for k,v in enumerate(o):yield from leaves(v,p+'/'+str(k))
    else:yield p,o
specs=[
('yazici_tek_001','Yazıcı','teknoloji/yazici',1,'D3','yazıcı',['yazici','printer']),
('merdane_tek_001','Merdane','mutfak/merdane',3,'D3','merdane',['merdane']),
('valiz_kapali_001','Kapalı valiz','seyahat/valiz',5,'D6','valiz',['valiz','bavul']),
('karavan_yandan_001','Yandan karavan','ulasim/karavan',5,'D6','karavan',['karavan']),
('yumurta_saglam_001','Sağlam yumurta','yiyecek/yumurta',6,'D1','yumurta',['yumurta']),
('sut_kutusu_001','Kapalı süt kutusu','yiyecek/sut',6,'D1','süt',['sut']),
('kasa_market_001','Market kasası','alisveris/kasa',6,'D2','kasa',['kasa']),
('poset_market_001','Boş market poşeti','alisveris/poset',6,'D2','poşet',['poset']),
('bal_kavanozu_001','Kapalı bal kavanozu','yiyecek/bal',6,'D3','bal',['bal']),
('sunger_tek_001','Sünger','temizlik/sunger',6,'D3','sünger',['sunger']),
('armut_butun_001','Bütün armut','yiyecek/armut',6,'D4','armut',['armut']),
('portakal_butun_001','Bütün portakal','yiyecek/portakal',6,'D4','portakal',['portakal']),
('domates_butun_001','Bütün domates','yiyecek/domates',6,'D4','domates',['domates']),
('yastik_tek_001','Tek yastık','ev/yastik',9,'D4','yastık',['yastik']),
('kanepe_bos_001','Boş kanepe','ev/kanepe',9,'D5','kanepe',['kanepe','koltuk']),
('raf_bos_001','Boş raf','ev/raf',9,'D2','raf',['raf']),
('klavye_tek_001','Klavye','teknoloji/klavye',10,'D3','klavye',['klavye']),
('saat_akilli_001','Akıllı saat','teknoloji/akilli-saat',10,'D3','akıllı saat',['saat_akilli','akilli_saat']),
('tablet_tek_001','Tablet','teknoloji/tablet',10,'D7','tablet',['tablet']),
('hoparlor_tek_001','Hoparlör','teknoloji/hoparlor',10,'D7','hoparlör',['hoparlor']),
('bilgisayar_dizustu_001','Dizüstü bilgisayar','teknoloji/dizustu-bilgisayar',10,'D7','dizüstü bilgisayar',['bilgisayar','dizustu','laptop']),
('havlu_katli_001','Katlı havlu','bakim/havlu',11,'D2','havlu',['havlu']),
('firca_sac_001','Saç fırçası','bakim/sac-fircasi',11,'D3','saç fırçası',['sac_fircasi','firca_sac']),
('degnek_sihirli_001','Sihirli değnek','masal/sihirli-degnek',12,'D5','sihirli değnek',['degnek'])]
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/fidan_kuyruk_kaniti.json'
if all(s[0] in oldids for s in specs):
    print(json.dumps({'already_appended':True,'proof_preserved':proof.exists()}));raise SystemExit(0)
raw=(BASE/'work/source'/SOURCE).read_bytes()
blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
expected=subprocess.check_output(['git','rev-parse','HEAD:'+SOURCE],cwd=REPO,text=True).strip()
assert blob==expected, 'Source Git blob mismatch'
source=json.loads(raw);cards=read(BASE/'work/source/kartlar.json')
h=read(ROOT/'denetim/uretim_kayitlari_eslestirme.json');records={x['record'] for x in h}
for f in (REPO/'stop-motion/uretim-kayitlari').glob('*.json'):
    rel=f.relative_to(REPO).as_posix()
    if rel in records:continue
    j=read(f);p=REPO/'stop-motion'/j['final_path']
    valid=p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==j['metrics']['sha256']
    assert valid,'Canonical binary missing or changed: '+rel
    h.append({'record':rel,'asset_name':j['id'],'declared_final_sha256':j['metrics']['sha256'],'historical_status':j['status'],'binary_revalidated_this_session':valid});records.add(rel)
canonical=[p.relative_to(REPO).as_posix() for p in (REPO/'stop-motion/yardimci-nesneler').rglob('*.png')]
new=[]
for aid,title,cat,un,ln,term,aliases in specs:
    if aid in oldids:continue
    ui=next(i for i,u in enumerate(source['uniteler']) if u['no']==un);u=source['uniteler'][ui]
    di=next(i for i,d in enumerate(u['dersler']) if d['kod']==ln);d=u['dersler'][di]
    locs=[p for p,v in leaves(d) if v==term];assert locs,aid+' missing source evidence'
    historical=[x['record'] for x in h if any(matches(a,x.get('asset_name','')+' '+x['record']) for a in aliases)]
    existing=[x['id'] for x in q['items']+new if any(matches(a,x['id']) for a in aliases)]
    files=[x for x in canonical if any(matches(a,x) for a in aliases)]
    assert not historical and not existing and not files, (aid,historical,existing,files)
    new.append({'id':aid,'title':title,'category':'yardimci-nesneler/'+cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':SOURCE,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+locs[0]}],'felt_cards_preserved':[c['id'] for c in cards if matches(norm(term),c['ad'])],'role':'independent paper helper; existing felt cards remain canonical','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} canonical records, {len(canonical)} canonical PNGs, and {len(q["items"])} live queue items','semantic_review':'Akıllı kol saati mevcut çalar saatten farklı gövde ve kullanım; saç fırçası mevcut tarak, diş fırçası ve boya fırçasından farklı; bağımsız yastık yatağın tekrarı değil. Bal, balon ile eşleşmez. Süt kutusu ambalajı nesnenin kendisi; ayrı süt bardağı eklenmez. Eski erişilemeyen varlıklar tekrar üretilmez.'})
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blob_sha_verified':blob,'source':SOURCE,'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'historical_records':len(h),'canonical_pngs':len(canonical)}))
