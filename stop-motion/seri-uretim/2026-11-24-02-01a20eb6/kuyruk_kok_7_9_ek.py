"""Reconcile thirteen curriculum needs against canonical records, files and live queue."""
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
specs=json.loads("[[\"boya_kalemi_tek_001\",\"Tek renkli boya kalemi\",\"yardimci-nesneler/okul/boya-kalemi\",\"7-9-kok\",3,\"D2\",\"boya kalemi\",[\"boya_kalemi\",\"renkli_kalem\"],null,\"Tek kırmızı ahşap gövdeli boya kalemi, sivri ahşap koni ve kırmızı renkli uç. Resmedilen nesne boya kalemidir; resmin malzemesi yoğun keçeli kalemdir, kuru boya dokusu değil. Grafit kurşun kalemden ayrı.\"],[\"kalem_kutusu_kapali_001\",\"Tek kapalı kalem kutusu\",\"yardimci-nesneler/okul/kalem-kutusu\",\"7-9-kok\",3,\"D4\",\"kalem kutusu\",[\"kalem_kutusu\"],null,\"Tek turkuaz yatay kapalı sert kalem kutusu, bağlı turuncu küçük mandal ve kapak ayrım çizgisi. Kalem/silgi/ikinci nesne yok; basit kutu ama kırtasiye ölçeğinde.\"],[\"meyve_suyu_bardagi_001\",\"Tek bardak portakal suyu\",\"yardimci-nesneler/yiyecek/meyve-suyu\",\"7-9-kok\",5,\"D1\",\"portakal suyu bardağı\",[\"meyve_suyu\",\"portakal_suyu\"],null,\"Kaynak test seçeneğinde portakal suyu bardağı açıkça var. Tek düz bardakta turuncu meyve suyu; ince mavi cam kenarı, opak kâğıt yüzey. Pipet/portakal dilimi/ayrı meyve/kapak yok.\"],[\"pilav_tabagi_001\",\"Tek tabakta pilav\",\"yardimci-nesneler/yiyecek/pilav\",\"7-9-kok\",5,\"D2\",\"pilav\",[\"pilav\"],null,\"Tek mavi tabakta bir porsiyon beyaz pirinç pilavı; taneler kısa açık oker çizgiler, pirinç opak beyaz kâğıt. Tabak ve yiyecek bir yemek nesnesi; garnitür/kaşık/et yok.\"],[\"makarna_tabagi_001\",\"Tek tabakta makarna\",\"yardimci-nesneler/yiyecek/makarna\",\"7-9-kok\",5,\"D2\",\"makarna\",[\"makarna\"],null,\"Tek mavi tabakta sade sarı kısa boru makarna porsiyonu; boru ağızları opak koyu çizim, alfa deliği değil. Ayrı çatal/peynir/tencere/garnitür yok; tüm yemek aynı tabak üzerinde bağlı.\"],[\"salata_kasesi_001\",\"Tek kâsede salata\",\"yardimci-nesneler/yiyecek/salata\",\"7-9-kok\",5,\"D3\",\"salata\",[\"salata\"],null,\"Tek turuncu kâsede yeşil marul, birkaç domates ve salatalık dilimiyle bütünleşik salata. Malzemeler tek yemek içinde üst üste/bağlı; ayrı sebze/çatal yok.\"],[\"borek_dilim_001\",\"Tek börek dilimi\",\"yardimci-nesneler/yiyecek/borek\",\"7-9-kok\",5,\"D5\",\"börek\",[\"borek\"],null,\"Tek dikdörtgen katlı peynirli tepsi böreği dilimi; altın kahverengi üst, yufka katları ve açık beyaz peynir içi. Baklava gibi şerbet/fıstık yok; tabak ve ayrı kırıntı yok.\"],[\"ayran_bardagi_001\",\"Tek bardak ayran\",\"yardimci-nesneler/yiyecek/ayran\",\"7-9-kok\",5,\"D5\",\"ayran\",[\"ayran\"],null,\"Tek düz bardakta opak beyaz ayran; üstte birkaç bütünleşik köpük kabarcığı çizgisi, turkuaz ince cam kenarı. AYRAN küçük yazısı kimliği ayırır; pipet/şişe/yoğurt kâsesi/ayrı nesne yok.\"],[\"sandalet_tek_001\",\"Tek sandalet\",\"yardimci-nesneler/giyim/sandalet\",\"7-9-kok\",9,\"D2\",\"sandalet\",[\"sandalet\"],null,\"Tek açık burunlu sandalet, turuncu taban ve turkuaz iki ön kayış ile bağlı topuk kayışı; üç çeyrek görünüm. Ayak/ikinci sandalet yok. Taban üzerinde iç yüzey opak, dış kayış boşlukları alfa ve beyaz iç kenarlı.\"],[\"salatalik_butun_001\",\"Tek bütün salatalık\",\"yardimci-nesneler/yiyecek/salatalik\",\"7-9-kok\",11,\"D1\",\"salatalık\",[\"salatalik\"],null,\"Tek uzun hafif eğri yeşil salatalık; yuvarlak uçlar, bir küçük bağlı sap ucu ve koyu kısa kabuk çizgileri. Dilim/çiçek/yaprak/ikinci sebze yok.\"],[\"biber_yesil_butun_001\",\"Tek bütün yeşil biber\",\"yardimci-nesneler/yiyecek/biber\",\"7-9-kok\",11,\"D2\",\"biber\",[\"biber\"],null,\"Tek uzun sivri yeşil biber, hafif kıvrık gövde ve bağlı kısa koyu yeşil sap; dilim/tohum/yaprak/ikinci sebze yok. Doldurulmuş dolmadan ayrı çiğ sebze.\"],[\"sogan_butun_001\",\"Tek bütün kuru soğan\",\"yardimci-nesneler/yiyecek/sogan\",\"7-9-kok\",11,\"D2\",\"soğan\",[\"sogan\"],null,\"Tek yuvarlak altın kahverengi kuru soğan; dikey kabuk çizgileri, üstte kısa kuru boyun, altta küçük bağlı kök püskülü. Ayrı kabuk/dilim/yeşil sürgün yok.\"],[\"patates_butun_001\",\"Tek bütün patates\",\"yardimci-nesneler/yiyecek/patates\",\"7-9-kok\",11,\"D2\",\"patates\",[\"patates\"],null,\"Tek düzensiz oval oker kahverengi bütün patates, birkaç koyu küçük göz izi. Filiz/yaprak/dilim/kızartma veya ikinci patates yok.\"]]")
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/kok_7_9_ek_kuyruk_kaniti.json'
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
        b=canonical_records[baseid];cat=pathlib.PurePosixPath(b['final_path']).parent.as_posix();cardids=b.get('felt_cards_preserved',[])
        reference={'base_id':baseid,'base_revision':b['revision'],'canonical_png':'stop-motion/'+b['final_path'],'sha256':sha(REPO/'stop-motion'/b['final_path']),'base_preserved':True}
        srcsha=b['technical_processing']['source_sha256']
        for f in (REPO/b['batch_path']/'adaylar'/baseid).glob('*/qa.json'):
            r=read(f)
            if r['metrics']['sha256']==srcsha:
                rp=REPO/b['batch_path']/r['candidate_path'];assert sha(rp)==srcsha
                reference.update(native_reference_png=rp.relative_to(REPO).as_posix(),native_reference_sha256=srcsha)
        assert reference.get('native_reference_png'),baseid
    item={'id':aid,'title':title,'category':cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':rel,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+pointer,'match':'exact_json_leaf' if value==term else 'substring_of_exact_json_leaf','leaf_sha256':hashlib.sha256(value.encode()).hexdigest()}],'felt_cards_preserved':cardids,'role':'missing pose of existing paper helper' if baseid else 'independent missing paper helper','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} records, {len(canonical)} canonical PNGs, {len(q["items"])} queue items','source_is_action_inference':aid in set(),'semantic_review':semantic+' Seçilen tam mevcut ders alanı okundu. Mevcut R/K kartlar ve temel yardımcı nesne dosyaları korunur. Üretim sonrası her PNG için ayrı teknik ve üç görünümde sanatsal QA gerekir; poz hizası/animasyon henüz doğrulanmış değildir. Tüm müfredat ayrıştırması bitmedi.'}
    if reference:item['pose_reference']=reference
    new.append(item)
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blobs_sha_verified':{k:v[1] for k,v in sources.items()},'base_references':[x['pose_reference'] for x in new if 'pose_reference' in x],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'records':len(h),'pngs':len(canonical)}))
