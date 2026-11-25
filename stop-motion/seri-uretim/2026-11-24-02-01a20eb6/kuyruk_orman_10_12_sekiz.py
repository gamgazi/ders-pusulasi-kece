"""Reconcile eight specific objects after full Orman reading and reference inspection."""
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
specs=json.loads('[["gazete_yagmur_duygusal_001", "Tek duygusal başlıklı örnek gazete", "yardimci-nesneler/esya/gazete", "10-12-orman", 3, "D5", "Yağmur şehri felç etti! Halk dehşet içinde!", ["gazete_yagmur_duygusal", "gazete_duygusal_baslik", "yagmur_felc_gazete"], "gazete_acik_001", "Tek açık gazetenin sol sayfasına dersin duygusal başlığı yazılır. Kurmaca okuma örneği; gerçek haber iddiası yok. Mevcut genel gazete bu başlığı taşımıyor."], ["gazete_yagmur_nesnel_001", "Tek nesnel başlıklı örnek gazete", "yardimci-nesneler/esya/gazete", "10-12-orman", 3, "D5", "Yoğun yağmur nedeniyle üç yol kapandı.", ["gazete_yagmur_nesnel", "gazete_nesnel_baslik", "uc_yol_gazete"], "gazete_acik_001", "Tek açık gazetenin sol sayfasına aynı kurmaca olayı daha nesnel anlatan tam ders başlığı yazılır. Duygusal gazete ayrı dosyada; tek PNG içinde iki gazete yok."], ["mercan_beyazlasmis_001", "Tek beyazlaşmış mercan kolonisi", "yardimci-nesneler/doga/mercan", "10-12-orman", 5, "D6", "Deniz suyu ısınınca mercanlar beyazlaşıyor.", ["mercan_beyazlasmis", "beyaz_mercan", "mercan_agarmis"], "mercan_kolonisi_001", "Mevcut beş ana dallı koloninin biçimi korunur; kırmızı/turuncu iç yüzey beyaz-krem, çok hafif soğuk gri keçeli kalem taraması olur. Beyaz makas payı lacivert çizginin dışında ayrı okunur. NOAA beyazlaşmanın tek başına ölüm olmadığını doğruluyor; ölü mercan, belirli tür ya da anatomik model iddiası yok."], ["bahce_paylasim_programi_001", "Tek bahçe paylaşım programı", "yardimci-nesneler/belgeler/bahce-programi", "10-12-orman", 6, "D8", "Futbol: pazartesi–çarşamba. Basketbol: salı–perşembe. Resim: her gün gölgeli köşe. Cuma: herkes için serbest.", ["bahce_paylasim_programi", "bahce_programi", "oyun_alani_programi"], "ders_programi_ornek_001", "Dersin dört kuralını taşıyan tek kâğıt: futbol pazartesi/çarşamba, basketbol salı/perşembe, resim her gün gölgeli köşe, cuma herkese serbest. Genel boş ders programı korunur. Bir kâğıt üzerindeki çizelge varlık kolajı değildir."], ["olay_orgusu_sayfasi_001", "Tek olay örgüsü planı kâğıdı", "yardimci-nesneler/belgeler/olay-orgusu", "10-12-orman", 11, "D5", "Defne olay örgüsünü önce bir kâğıda çizdi: başlangıç, sorun, dönüm noktası ve son.", ["olay_orgusu_sayfasi", "hikaye_plani", "oyku_plani", "olay_orgusu_plani"], "gorev_listesi_001", "Tek kâğıda dört aşama yukarıdan aşağıya yazılır: Başlangıç, Sorun, Dönüm noktası, Son. Ardışık üç aşağı ok aynı yüzeyin mürekkep çizimidir. Hikâye sahneleri veya ayrı kutu kartları üretilmez."], ["kaynakca_sayfasi_ornek_001", "Tek boş örnek kaynakça sayfası", "yardimci-nesneler/belgeler/kaynakca", "10-12-orman", 12, "D6", "Ödevin sonunda kullandığın kaynakları sıraladığın listeye ne denir?", ["kaynakca_sayfasi", "kaynakca_ornek", "kaynak_listesi"], "basvuru_formu_ornek_001", "KAYNAKÇA ve ÖRNEK başlıklı tek boş doldurma kâğıdı. Kitap, Dergi, Site alanları boş kalır. Önceki D5 dersinde bu kaynak türleri geçer. Gerçek eser, yazar, yayın tarihi, URL veya uydurma atıf yazılmaz; tamamlanmış bibliyografya değildir."], ["okuma_listesi_001", "Tek boş okuma listesi kâğıdı", "yardimci-nesneler/belgeler/okuma-listesi", "10-12-orman", 14, "D3", "okuma listesi", ["okuma_listesi", "okunacaklar_listesi"], "gorev_listesi_001", "OKUMA LİSTESİ başlıklı tek kâğıtta 1, 2, 3 numaralı üç boş yazma satırı. Kaynakta gerçek kitap adları yok; ad uydurulmaz. Mevcut görev/alışveriş/soru listeleri farklı yazıları taşır ve korunur."], ["kelime_defteri_kapali_001", "Tek kapalı kelime defteri", "yardimci-nesneler/kagit/not-defteri", "10-12-orman", 14, "D3", "kelime defteri", ["kelime_defteri", "sozcuk_defteri"], "not_defteri_001", "Mevcut turuncu kapalı not defterinin kapağında KELİME DEFTERİ iki satırda yazılır. Tek defter, aynı sırt/sayfa bloğu/kâğıt kıvrımı; kalem veya ayrı harf parçaları yok. NOTLAR etiketli genel defter korunur."]]')
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/orman_10_12_sekiz_kaniti.json'
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
