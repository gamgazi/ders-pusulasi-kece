"""Reconcile seven narrative objects and phone states with exact source leaves and prior records."""
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
specs=json.loads('[["anahtar_pasli_001", "Tek paslı anahtar", "yardimci-nesneler/ev/anahtar", "16-17-cinar", 12, "D5", "paslı, ağır bir anahtar", ["anahtar_pasli", "pasli_anahtar"], "anahtar_tek_001", "Yuvarlak delikli, sağa uzanan üç dişli sarı/turuncu anahtarın ham çizimi gerçekten incelendi. Kaynakta pas açıkça var; koyu kahverengi pas yamaları çizilir, ağırlık ayrı nesne değildir. Kesilmiş öykünün eksik sonu uydurulmaz."], ["anahtar_islak_001", "Tek ıslak anahtar", "yardimci-nesneler/ev/anahtar", "16-17-orman", 11, "D5", "anahtarı aldığımda ıslaktı", ["anahtar_islak", "islak_anahtar"], "anahtar_tek_001", "Islak Anahtar öyküsünde ıslaklık açık. Aynı anahtar üzerinde belirgin mavi/turkuaz su damlası çizimleri kullanılır; ayrı yağmur damlası veya su birikintisi eklenmez. Bu bir anlatı yardımcı nesnesidir."], ["ceket_kahverengi_deri_001", "Tek kahverengi deri ceket çizimi", "yardimci-nesneler/giysi/ceket", "16-17-kok", 4, "D8", "kahverengi deri ceket, 38 beden, çok temiz", ["ceket_kahverengi_deri", "deri_ceket_kahverengi", "ceket_deri_kahverengi"], "ceket_tek_001", "Mor ceket ham çizimi incelendi. Kaynakta kahverengi deri ceket açık; biçim korunan kahverengi yüzey ve kısa açık kahve parlamalarla deri çizimi yapılır. Gerçek deri dokusu veya yeni38etiketi gerekmez."], ["telefon_beklemede_001", "Tek beklemede arama ekranlı telefon", "yardimci-nesneler/teknoloji/telefon", "16-17-kok", 12, "D4", "Hattı biraz bekler misiniz?", ["telefon_beklemede", "telefon_hatta_bekleme", "telefon_bekleyen_arama"], "telefon_mobil_001", "Hatta bekletme kaynakta açık; ekran temsili sanatsal çıkarım. Cevapsız arama, sessiz mod ve sesli mesaj mevcutlarıyla aynı durum değildir. Gerçek arama yapılmaz."], ["telefon_dahili_214_001", "Tek214dahili numara ekranlı telefon", "yardimci-nesneler/teknoloji/telefon", "16-17-kok", 12, "D4", "dahili numara 214", ["telefon_dahili_214", "telefon_214_dahili", "dahili_214_telefon"], "telefon_mobil_001", "Kaynakta insan kaynakları için214ü tuşlamak var. Yalnız kaynak numarası ve genel arama simgesi gösterilir; tam gerçek telefon numarası veya gerçek şirket yok."], ["telefon_sarj_1_001", "Tekyüzde1şarj ekranlı telefon", "yardimci-nesneler/teknoloji/telefon", "16-17-kok", 12, "D2", "Telefonun şarjı yüzde bir.", ["telefon_sarj_1", "telefon_yuzde_1", "telefon_pil_1"], "telefon_mobil_001", "Şarjı bitmiş telefon ile yüzde1aynı durum değildir; kaynak yüzde biri açıkça söylüyor. Ekranda düşük pil gösterilir; çizgi doluluk nicel ölçek olarak sunulmaz."], ["bulmaca_alti_bos_001", "Tekaltıboşkarelibulmaca kâğıdı", "yardimci-nesneler/egitim/bulmaca", "16-17-orman", 11, "D5", "Boş bıraktığı kareleri saydım. Altı tane.", ["bulmaca_alti_bos", "bulmaca_alti_kare", "bulmaca_6_bos"], "", "Kesilmiş öyküde Unutmamak ipucu ve altı boş kare açık. Tek kâğıt yüzeyinde bu giriş temsil edilir; bilinmeyen çözüm veya öykü sonu üretilmez. Altı kutu asset grid değildir, bulmaca kâğıdının üzerindeki hücrelerdir."]]')
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/anlati_telefon_yedi_kaniti.json'
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
