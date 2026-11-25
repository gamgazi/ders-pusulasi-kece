"""Reconcile timer10, dripping faucet and two television content states; reuse existing timer05."""
import hashlib,json,pathlib,re,subprocess,unicodedata
ROOT=pathlib.Path(__file__).resolve().parent
BASE=ROOT.parent.parent
REPO=BASE/'work/repository'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def write(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def norm(s):return re.sub('[^a-z0-9]+','_', ''.join(c for c in unicodedata.normalize('NFKD',s.casefold().replace('ı','i')) if not unicodedata.combining(c))).strip('_')
def matches(a,s):return ('_'+a+'_') in ('_'+norm(s)+'_')
def leaves(o,p=''):
    if isinstance(o,dict):
        for k,v in o.items():yield from leaves(v,p+'/'+k)
    elif isinstance(o,list):
        for k,v in enumerate(o):yield from leaves(v,p+'/'+str(k))
    else:yield p,o
specs=json.loads('[["zamanlayici_on_dakika_001", "Tek on dakikaya ayarlı zamanlayıcı", "yardimci-nesneler/esya/zamanlayici", "7-9-agac", 18, "D4", "Önce sen on dakika oyna, sonra ben.", ["zamanlayici_on_dakika", "zamanlayici_10", "on_dakika_zamanlayici", "sayac_10_dakika"], "zamanlayici_001", "Mevcut zamanlayıcı ham PNG gerçekten görüldü: 05:00, turkuaz gövde, iki turuncu düğme, sağ üst kâğıt kıvrımı. Beş dakika gereksinimi mevcut dosyaya eşleşir ve tekrar üretilmez. Yalnız on dakikalık süre 10:00 olur; duvar saatinin saat10 pozu değildir."], ["musluk_damlayan_001", "Tek ucunda damla oluşan musluk", "yardimci-nesneler/ev/musluk", "7-9-agac", 12, "D4", "Sorunu buldum! Musluk damlıyor.", ["musluk_damlayan", "damlayan_musluk", "musluk_damla", "musluk_sizdiran"], "musluk_kapali_001", "Kapalı musluğun kırmızı vana, gri gövde, solda duvar bağlantısı, sağ aşağı ağız ve sol üst kıvrımı görüldü. Ağızdan ayrılmak üzere oluşmuş TEK bağlı damla eklenir; akan sürekli su ve tamamen kuru kapalı durumdan ayrıdır. Ayrık damla/su birikintisi eklenmez."], ["televizyon_haber_001", "Tek haber yayını gösteren televizyon", "yardimci-nesneler/teknoloji/televizyon", "4-6-orman", 5, "D1", "resim: televizyonda haber", ["televizyon_haber", "haber_televizyon", "tv_haber", "haberler_televizyon"], "televizyon_tek_001", "Mevcut mavi televizyonun turuncu alt bandı, sarı düğmesi, iki ayağı ve sağ üst kıvrımı korunur. Ekran yüzeyinde HABERLER başlığı ve soyut yayın küresi kullanılır; gerçek haber veya coğrafi doğruluk iddiası yok. Yeni R/K spiker karakteri çizilmez. Mevcut altyazı/siyah beyaz durumla aynı değildir."], ["televizyon_cizgi_film_001", "Tek çizgi film gösteren televizyon", "yardimci-nesneler/teknoloji/televizyon", "4-6-orman", 5, "D1", "resim: çizgi film", ["televizyon_cizgi_film", "cizgi_film_televizyon", "tv_cizgi_film", "televizyon_animasyon"], "televizyon_tek_001", "Televizyonun aynı gövdesinde yalnız ekranın çizgi film içeriği değişir. Ekran içine çizilmiş neşeli yüzlü uçan kalem özgün kurgu motifidir; R/K karakter kopyası veya bağımsız kalem asseti değildir. Ekran dışı nesne yok."]]')
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/ekran_sure_dort_kaniti.json'
if all(s[0] in oldids for s in specs):
    print(json.dumps({'already_appended':True,'proof_preserved':proof.exists()}));raise SystemExit(0)
sources={}
for tag in {s[3] for s in specs}:
    rel='pusula/ders-pusulasi/'+tag+'.json';raw=(BASE/'work/source'/rel).read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    assert blob==subprocess.check_output(['git','rev-parse','HEAD:'+rel],cwd=REPO,text=True).strip(),rel
    sources[tag]=(rel,blob,json.loads(raw))
h=read(ROOT/'denetim/uretim_kayitlari_eslestirme.json');seen={x['record'] for x in h};canonical_records={}
for f in (REPO/'stop-motion/uretim-kayitlari').glob('*.json'):
    j=read(f);rel=f.relative_to(REPO).as_posix()
    if j.get('final_accepted'):
        assert sha(REPO/'stop-motion'/j['final_path'])==j['metrics']['sha256'],rel
        canonical_records[j['id']]=j
    if rel not in seen:
        assert j.get('final_accepted') and j['id'] in canonical_records
        h.append({'record':rel,'asset_name':j['id'],'declared_final_sha256':j['metrics']['sha256'],'historical_status':j['status'],'binary_revalidated_this_session':True});seen.add(rel)
canonical=[p.relative_to(REPO).as_posix() for p in (REPO/'stop-motion').rglob('*.png') if 'seri-uretim' not in p.parts]
cards=read(BASE/'work/source/kartlar.json');new=[]
for aid,title,cat,tag,un,ln,term,aliases,baseid,semantic in specs:
    if aid in oldids:continue
    rel,blob,s=sources[tag];ui=next(i for i,u in enumerate(s['uniteler']) if u['no']==un);u=s['uniteler'][ui]
    di=next(i for i,d in enumerate(u['dersler']) if d['kod']==ln);d=u['dersler'][di]
    hits=[(p,v) for p,v in leaves(d) if isinstance(v,str) and term in v];assert hits,aid
    pointer,value=hits[0]
    historical=[x['record'] for x in h if any(matches(a,x.get('asset_name','')+' '+x['record']) for a in aliases)]
    existing=[x['id'] for x in q['items']+new if any(matches(a,x['id']) for a in aliases)]
    files=[x for x in canonical if any(matches(a,x) for a in aliases)]
    assert not historical and not existing and not files,(aid,historical,existing,files)
    reference=None;cardids=[c['id'] for c in cards if any(matches(a,c['ad']) for a in aliases)]
    if baseid:
        b=canonical_records[baseid];cardids=b.get('felt_cards_preserved',[])
        reference={'base_id':baseid,'base_revision':b['revision'],'canonical_png':'stop-motion/'+b['final_path'],'sha256':sha(REPO/'stop-motion'/b['final_path']),'base_preserved':True}
        srcsha=b['technical_processing']['source_sha256']
        for f in (REPO/b['batch_path']/'adaylar'/baseid).glob('*/qa.json'):
            r=read(f)
            if r['metrics']['sha256']==srcsha:
                rp=REPO/b['batch_path']/r['candidate_path'];assert sha(rp)==srcsha
                reference.update(native_reference_png=rp.relative_to(REPO).as_posix(),native_reference_sha256=srcsha)
        assert reference.get('native_reference_png'),baseid
    item={'id':aid,'title':title,'category':cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':rel,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+pointer,'match':'exact_json_leaf' if value==term else 'substring_of_exact_json_leaf','leaf_sha256':hashlib.sha256(value.encode()).hexdigest()}],'felt_cards_preserved':cardids,'role':'missing pose of existing paper helper' if baseid else 'independent missing paper helper','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} records, {len(canonical)} canonical PNGs, {len(q["items"])} queue items','source_is_action_inference':True,'semantic_review':semantic+' Seçilen tam mevcut ders alanı okundu. Mevcut R/K kartlar ve temel yardımcı nesne dosyaları korunur. Üretim sonrası her PNG için ayrı teknik ve üç görünümde sanatsal QA gerekir; poz hizası/animasyon henüz doğrulanmış değildir. Tüm müfredat ayrıştırması bitmedi.'}
    if reference:item['pose_reference']=reference
    new.append(item)
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blobs_sha_verified':{k:v[1] for k,v in sources.items()},'base_references':[x['pose_reference'] for x in new if 'pose_reference' in x],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'records':len(h),'pngs':len(canonical)}))
