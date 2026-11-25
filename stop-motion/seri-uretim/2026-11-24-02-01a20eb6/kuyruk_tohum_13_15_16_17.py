"""Reconcile fourteen curriculum needs against canonical records, files and live queue."""
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
specs=json.loads("[[\"ders_programi_ornek_001\",\"Tek örnek ders programı\",\"yardimci-nesneler/okul/ders-programi\",\"13-15-tohum\",3,\"D6\",\"ders programı\",[\"ders_programi\"],null,\"Tek krem çizelge, DERS PROGRAMI / ÖRNEK, basılı üç sütun Gün / Saat / Ders ve üç boş satır. Tek belge üzerindeki çizelge nesne kolajı değil; tarih/gerçek okul/kişi yok.\"],[\"sicak_cikolata_fincani_001\",\"Tek sıcak çikolata fincanı\",\"yardimci-nesneler/yiyecek/sicak-cikolata\",\"13-15-tohum\",5,\"D6\",\"sıcak çikolata\",[\"sicak_cikolata\"],null,\"Tek turuncu kulplu fincanda kahverengi sıcak çikolata; fincanda SICAK ÇİKOLATA yazısı. Kulp deliği gerçek alfa, beyaz iç pay. Buhar, tabak, kaşık, krema süsü veya ikinci nesne yok.\"],[\"pasta_dilimi_cikolatali_001\",\"Tek çikolatalı pasta dilimi\",\"yardimci-nesneler/yiyecek/cikolatali-pasta-dilimi\",\"13-15-tohum\",5,\"D6\",\"çikolatalı\",[\"pasta_dilimi\",\"pasta_dilim\",\"cikolatali_pasta\"],null,\"Kaynakta çikolatalı pasta dilimi istenir. Tek üçgen katlı çikolatalı pasta dilimi, iki koyu kahverengi kek katı ve arada krem şerit, kahverengi üst kaplama. Mevcut sade kek diliminden ve bütün pembe pastadan farklı yiyecek; tabak/mum/çilek yok.\"],[\"menu_ornek_001\",\"Tek örnek menü\",\"yardimci-nesneler/belgeler/menu\",\"13-15-tohum\",5,\"D7\",\"Menüye bakabilir miyim?\",[\"menu\"],null,\"Tek hafif açık katlı menü kartı, MENÜ / ÖRNEK ve Çorba / Tost / Ayran yazıları. Fiyat/marka/ikinci kart/masa yok. Kafe menüsü bağımsız belge işlevi.\"],[\"ananas_butun_001\",\"Tek bütün ananas\",\"yardimci-nesneler/yiyecek/ananas\",\"13-15-tohum\",6,\"D6\",\"ananas\",[\"ananas\"],null,\"Tek sarı oker oval ananas, bağlı yeşil sivri yaprak tacı ve koyu kabuk bölmeleri. Desen meyve yüzeyinde çizili, nesne grid değil. Ayrı yaprak/dilim yok.\"],[\"patlican_butun_001\",\"Tek bütün patlıcan\",\"yardimci-nesneler/yiyecek/patlican\",\"13-15-tohum\",6,\"D7\",\"patlıcan\",[\"patlican\"],null,\"Tek parlak mor uzun patlıcan, üstte bağlı yeşil çanak ve kısa sap. Yoğun marker mürekkebi, fotogerçek parlama değil. Ayrı dilim/yaprak/tabak yok.\"],[\"misir_kocani_001\",\"Tek mısır koçanı\",\"yardimci-nesneler/yiyecek/misir\",\"13-15-tohum\",6,\"D7\",\"mısır\",[\"misir\"],null,\"Tek sarı mısır koçanı, altından bağlı iki yeşil kabuk yaprağı yana kıvrılmış. Taneler tek koçanın yüzeyinde çizili; ayrı tane, püskül, tabak veya ikinci koçan yok.\"],[\"tenis_raketi_tek_001\",\"Tek tenis raketi\",\"yardimci-nesneler/spor/tenis-raketi\",\"13-15-tohum\",9,\"D1\",\"Raketle oynanan spor hangisi?\",[\"tenis_raketi\",\"tenis_raket\"],null,\"Kaynak testi raketle tenis bağlantısını açık verir. Tek turuncu oval çerçeveli tenis raketi, mavi sap; ip ağı opak krem kâğıt yatağına çizilmiş. Büyük üçgen boğaz açıklığı gerçek alfa ve beyaz iç paylı. Top/insan yok.\"],[\"masa_tenisi_raketi_tek_001\",\"Tek masa tenisi raketi\",\"yardimci-nesneler/spor/masa-tenisi-raketi\",\"13-15-tohum\",9,\"D3\",\"masa tenisi\",[\"masa_tenisi_raketi\",\"masa_tenisi_raket\"],null,\"Masa tenisi etkinliğinden çıkarılan tek kısa saplı yuvarlak raket. Kırmızı opak yüz ve kısa ahşap renkli bağlı sap; top/masa/insan yok. Ekipman çıkarımı açık kaydedilir.\"],[\"yoga_mati_001\",\"Tek yoga matı\",\"yardimci-nesneler/spor/yoga-mati\",\"13-15-tohum\",9,\"D3\",\"yoga\",[\"yoga_mati\",\"yoga_mat\"],null,\"Yoga etkinliğinden çıkarılan tek mor uzun mat, bir kısa ucu kendi üzerine az kıvrılmış. Spor matı nesnesi kâğıt çizim; insan/zemin/ikinci mat yok. Ekipman çıkarımı açık.\"],[\"trenckot_kapali_001\",\"Tek kapalı trençkot\",\"yardimci-nesneler/giysi/trenckot\",\"16-17-tohum\",8,\"D7\",\"trençkot\",[\"trenckot\"],null,\"Tek uzun bej trençkot önden, iki kol, devrik yaka, iki sıra üçer düğme ve gövdeye bağlı bağlanmış bel kemeri. Kişi/askı/ayrı kemer yok. Kısa mont ve yağmurluktan uzun yaka/kemer biçimi farklı.\"],[\"sigorta_karti_ornek_001\",\"Tek örnek sigorta kartı\",\"yardimci-nesneler/belgeler/sigorta-karti\",\"16-17-tohum\",12,\"D4\",\"sigorta kartı\",[\"sigorta_karti\"],null,\"Tek hayali turkuaz kart, SİGORTA KARTI / ÖRNEK ve Ad için boş çizgi. Sağlık erişimi bağlamında eğitim nesnesi; gerçek kurum/poliçe/numara/kişisel veri/çip/barkod yok.\"],[\"saglik_raporu_ornek_001\",\"Tek örnek sağlık raporu\",\"yardimci-nesneler/belgeler/saglik-raporu\",\"16-17-tohum\",12,\"D7\",\"rapor\",[\"saglik_raporu\"],null,\"Sağlık dersi bağlamında tek krem örnek belge; SAĞLIK RAPORU / ÖRNEK ve boş Ad / Tarih alanları. Tanı/tedavi/gerçek hekim/imza/mühür yok; reçeteden farklı belge.\"],[\"kabul_mektubu_ornek_001\",\"Tek örnek kabul mektubu\",\"yardimci-nesneler/belgeler/kabul-mektubu\",\"16-17-tohum\",16,\"D4\",\"kabul mektubu\",[\"kabul_mektubu\"],null,\"Tek krem örnek kabul mektubu, KABUL MEKTUBU / ÖRNEK ve boş Ad alanı, üç kısa lacivert yer tutucu çizgi. Kaynak başvuru bağlamının belgesi; gerçek kurum/kişi/karar/imza/mühür yok. Mevcut kişisel mektuptan işlev farklı.\"]]")
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/tohum_13_15_16_17_kuyruk_kaniti.json'
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
    item={'id':aid,'title':title,'category':cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':rel,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+pointer,'match':'exact_json_leaf' if value==term else 'substring_of_exact_json_leaf','leaf_sha256':hashlib.sha256(value.encode()).hexdigest()}],'felt_cards_preserved':cardids,'role':'missing pose of existing paper helper' if baseid else 'independent missing paper helper','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} records, {len(canonical)} canonical PNGs, {len(q["items"])} queue items','source_is_action_inference':aid in {'masa_tenisi_raketi_tek_001','yoga_mati_001'},'semantic_review':semantic+' Seçilen tam mevcut ders alanı okundu. Mevcut R/K kartlar ve temel yardımcı nesne dosyaları korunur. Üretim sonrası her PNG için ayrı teknik ve üç görünümde sanatsal QA gerekir; poz hizası/animasyon henüz doğrulanmış değildir. Tüm müfredat ayrıştırması bitmedi.'}
    if reference:item['pose_reference']=reference
    new.append(item)
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blobs_sha_verified':{k:v[1] for k,v in sources.items()},'base_references':[x['pose_reference'] for x in new if 'pose_reference' in x],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'records':len(h),'pngs':len(canonical)}))
