"""Reconcile twelve curriculum needs against canonical records, files and live queue."""
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
specs=json.loads("[[\"hazine_sandigi_acik_bos_001\",\"Hazine sandığının açık boş pozu\",\"yardimci-nesneler/masal/hazine-sandigi\",\"4-6-cinar\",20,\"D1\",\"resim: hazine sandığını açan kahramanlar\",[\"hazine_sandigi_acik\",\"acik_hazine_sandigi\"],\"hazine_sandigi_kapali_001\",\"Mevcut turuncu/mavi/sarı sandığın bağlı kapağı yukarı açık; iç boşluk koyu kahverengi opak kâğıt yüzeyi. Eylemden açık poz çıkarımı. Hazine içeriği ayrı sahne varlıkları olacağı için boş tutulur; para, mücevher, kahraman veya ikinci sandık yok.\"],[\"musluk_acik_akan_001\",\"Açık ve su akan musluk\",\"yardimci-nesneler/ev/musluk\",\"4-6-cinar\",12,\"D3\",\"resim: musluğu açık bırakan Pingucan\",[\"musluk_acik\",\"musluk_akan\"],\"musluk_kapali_001\",\"Mevcut gri gövde ve kırmızı vanalı musluğun açık hali; çıkışına bağlı kısa tek mavi su akışı aynı kâğıt siluetinde. Ayrı damla, lavabo, su birikintisi, kişi veya dış mekân yok. Eylemden açık vana ve akan su pozu çıkarılır.\"],[\"kurabiye_yarim_001\",\"Tek yarım kurabiye\",\"yardimci-nesneler/yiyecek/kurabiye\",\"4-6-kok\",18,\"D5\",\"resim: kurabiyesini ikiye bölen çocuk\",[\"kurabiye_yarim\",\"yarim_kurabiye\"],\"kurabiye_tek_001\",\"Mevcut altın turuncu ve kahverengi parçacıklı kurabiyenin tek yarım parçası; bir kavisli dış kenar, bir düzensiz kırılmış kesit kenarı. Eylemden yarım poz çıkarımı. İkinci yarı, kırıntı, tabak veya çocuk yok.\"],[\"harita_hava_durumu_001\",\"Güneş ve bulut işaretli hava haritası\",\"yardimci-nesneler/esya/harita\",\"4-6-orman\",5,\"D2\",\"resim: güneş ve bulut işaretli harita\",[\"harita_hava_durumu\",\"hava_durumu_haritasi\"],\"harita_acik_001\",\"Mevcut üç katlı kâğıt haritanın üstüne çizilmiş sarı güneş ve gri-mavi bulut işaretleri; kırmızı X kaldırılır. Simgeler aynı opak harita yüzeyine mürekkeple çizilir, bağımsız nesne sayılmaz. Yer/ülke/gerçek tahmin veya sıcaklık iddiası yok.\"],[\"yaya_isigi_yesil_001\",\"Yeşil yaya sinyali\",\"yardimci-nesneler/guvenlik/yaya-isigi\",\"4-6-fidan\",19,\"D5\",\"resim: yaya için yeşil ışık\",[\"yaya_isigi\",\"yaya_lambasi\",\"yaya_sinyali\"],null,\"Tek yaya trafik sinyali; koyu dik gövde içinde üstte sönük koyu duran insan simgesi, altta yeşil yürüyen insan simgesi. Simgeler lamba yüzeyine çizili; kişi veya sahne değildir. Araçlar için üç renkli mevcut trafik lambasından farklı nesne. Direk/zemin/geçit/araba yok.\"],[\"robot_bozuk_sonuk_001\",\"Işığı sönük bozuk robot\",\"yardimci-nesneler/hayal/robot\",\"4-6-orman\",19,\"D1\",\"resim: ışığı sönük bozuk robot\",[\"robot_bozuk\",\"robot_sonuk\"],\"robot_tek_001\",\"Mevcut mavi başlı turuncu gövdeli oyuncak robotun sönük hali: gözler/anten/gövde göstergeleri koyu gri, baş hafif eğik, kollar aşağı, düz ağız. Tüm parçalar bağlı; kıvılcım/duman/kırık parça/metin yok.\"],[\"robot_dans_isikli_001\",\"Işıklı dans eden robot\",\"yardimci-nesneler/hayal/robot\",\"4-6-orman\",19,\"D1\",\"resim: ışıklı dans eden robot\",[\"robot_dans\",\"robot_isikli\"],\"robot_tek_001\",\"Aynı mavi/turuncu robot bir kolu yukarı ve bir ayağı yana kaldırılmış dans pozunda; göz/anten/göstergeler parlak sarı iç mürekkep vurgulu. Işık gövde üzerinde çizili, dışta ışın/yıldız/gölge/nota yok. Bağlı tek siluet ve kollar/bacaklar arası gerçek alfa, dar beyaz iç pay.\"],[\"oyuncak_araba_teker_eksik_001\",\"Bir tekeri eksik oyuncak araba\",\"yardimci-nesneler/oyun/oyuncak-araba\",\"4-6-orman\",19,\"D7\",\"resim: tekerleği çıkmış bozuk araba\",[\"oyuncak_araba_teker_eksik\",\"oyuncak_araba_bozuk\"],\"oyuncak_araba_001\",\"Mevcut kırmızı sağa bakan oyuncak arabanın sağ ön tekeri eksik; soldaki arka teker bağlı kalır, sağ ön teker yerinde boş kavis ve küçük bağlı aks ucu görünür. Kopmuş teker ikinci nesne olarak PNGye konmaz. Camlar opak kâğıt; zemin veya kişi yok.\"],[\"ev_maketi_karton_001\",\"Küçük karton ev maketi\",\"yardimci-nesneler/sanat/ev-maketi\",\"7-9-agac\",2,\"D2\",\"resim: kartondan küçük ev maketi\",[\"ev_maketi\",\"maket_ev\",\"karton_ev\"],null,\"Tek küçük karton ev modeli çizimi: kırmızı eğimli çatı, krem/okra duvar, üzerine çizili kapı ve iki pencere, bir köşede karton kat izi. Hafif üç çeyrek açı; maketin tabanı/çatı aynı bağlı nesne. Çocuk, masa, bahçe, güneş, ev sahnesi veya gerçek mimari arka plan yok.\"],[\"atletizm_engeli_001\",\"Tek atletizm atlama engeli\",\"yardimci-nesneler/spor/atletizm-engeli\",\"7-9-cinar\",1,\"D2\",\"resim: koşu yolunda atlanacak çubuk\",[\"atletizm_engeli\",\"atlama_engeli\",\"kosu_engeli\"],null,\"Tek atletizm engeli: iki mavi dik ayağa bağlı yatay beyaz/kırmızı çubuk ve iki kısa taban ayağı. Ortadaki büyük açıklık gerçek alfa ve dar beyaz kâğıt kesim paylı. Yol, koşucu, ikinci engel, madalya veya zemin yok.\"]]")
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/uzun_tarif_on_nesne_poz_kaniti.json'
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
    item={'id':aid,'title':title,'category':cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':rel,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+pointer,'match':'exact_json_leaf' if value==term else 'substring_of_exact_json_leaf','leaf_sha256':hashlib.sha256(value.encode()).hexdigest()}],'felt_cards_preserved':cardids,'role':'missing pose of existing paper helper' if baseid else 'independent missing paper helper','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} records, {len(canonical)} canonical PNGs, {len(q["items"])} queue items','source_is_action_inference':aid in {'hazine_sandigi_acik_bos_001','musluk_acik_akan_001','kurabiye_yarim_001'},'semantic_review':semantic+' Seçilen tam mevcut ders alanı okundu. Mevcut R/K kartlar ve temel yardımcı nesne dosyaları korunur. Üretim sonrası her PNG için ayrı teknik ve üç görünümde sanatsal QA gerekir; poz hizası/animasyon henüz doğrulanmış değildir. Tüm müfredat ayrıştırması bitmedi.'}
    if reference:item['pose_reference']=reference
    new.append(item)
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blobs_sha_verified':{k:v[1] for k,v in sources.items()},'base_references':[x['pose_reference'] for x in new if 'pose_reference' in x],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'records':len(h),'pngs':len(canonical)}))
