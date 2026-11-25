"""Reconcile ten specific states after full Tohum 13-15 reading and reference inspection."""
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
specs=json.loads('[["saat_calar_10_30_001", "Tek on buçuğu gösteren çalar saat", "yardimci-nesneler/esya/saat", "13-15-tohum", 4, "D6", "Saat on buçukta yatıyorum.", ["saat_calar_10_30", "saat_10_30", "saat_on_bucuk"], "saat_calar_10_00_001", "Aynı turkuaz gövdeli kırmızı çanlı saatte uzun yelkovan tam 6 yönünde, kısa akrep 10 ile 11 arasında. Tek saat; saniye kolu yok. 10.00 dosyası korunur."], ["menu_kafe_001", "Tek ders kafesinin örnek menüsü", "yardimci-nesneler/belgeler/menu", "13-15-tohum", 5, "D5", "Menüde tost, simit, pasta dilimi, ayran, limonata ve sıcak çikolata var.", ["menu_kafe", "kafe_menusu", "menu_sahil"], "menu_ornek_001", "Tek katlı kâğıt menüde dersin altı kalemi okunaklı yazılır. Mevcut menü yalnız Çorba/Tost/Ayran içeriyor; özel ders listesini karşılamıyor. Fiyat, gerçek işletme veya yiyecek kolajı eklenmez."], ["poster_basketbol_001", "Tek basketbol temalı poster", "yardimci-nesneler/okul/afis", "13-15-tohum", 10, "D5", "Bu benim favori basketbol takımım.", ["poster_basketbol", "basketbol_afisi", "takim_posteri"], "afis_tek_001", "Tek kâğıt posterde BASKETBOL başlığı ve mürekkeple çizilmiş bir turuncu basketbol topu. Takım adı, logo veya oyuncu kaynakta verilmedi; uydurulmaz. Bağımsız top PNG üretimi değil poster yüzeyinin çizimidir."], ["hali_mavi_duz_001", "Tek mavi düz halı", "yardimci-nesneler/ev/hali", "13-15-tohum", 10, "D9", "Halı mavi.", ["hali_mavi", "mavi_hali", "kilim_mavi"], "kilim_duz_001", "Mevcut kırmızı gövdeli üç baklava desenli kilim yerine tek düz mavi halı görünümü; yoğun mavi keçeli kalem taramaları, beyaz kâğıt payı. Halı dokusunu gerçek tekstil şeklinde üretmez; mevcut kilim korunur."], ["esofman_alti_siyah_001", "Tek siyah eşofman altı", "yardimci-nesneler/giyim/esofman", "13-15-tohum", 11, "D5", "güzel bir eşofman var ama siyah.", ["esofman_alti_siyah", "esofman_siyah", "siyah_esofman"], "esofman_alti_001", "Mevcut mavi eşofman altının aynı tek nesne biçiminde siyah sürümü; beyaz yan şeritleri kalır. Beden/kişiye oturma karşılaştırması iddiası yok. Tam iki parçalı eşofman takımı değil tek alt parça; üst parça eklenmez."], ["ayakkabi_spor_beyaz_tek_001", "Tek beyaz spor ayakkabı", "yardimci-nesneler/giysi/spor-ayakkabisi", "13-15-tohum", 11, "D5", "beyaz spor ayakkabılar", ["ayakkabi_spor_beyaz", "beyaz_spor_ayakkabi"], "ayakkabi_spor_tek_001", "Turuncu/turkuaz mevcut spor ayakkabıdan tek beyaz ayakkabı sürümü; beyaz iç yüzey, açık gri geniş işaretler, koyu lacivert hat/bağcık. Çift tek dosyada kolaj yapılmaz."], ["telefon_ekran_suresi_3_saat_001", "Tek üç saat ekran süreli telefon", "yardimci-nesneler/esya/telefon", "13-15-tohum", 13, "D4", "bugün: 3 saat", ["telefon_ekran_suresi_3_saat", "telefon_uc_saat"], "telefon_mobil_001", "Tek kırmızı telefonun ekranında EKRAN SÜRESİ / Bugün / 3 saat. Mevcut boş mavi ekran korunur; gerçek kullanıcı verisi, uygulama veya marka eklenmez."], ["telefon_ekran_suresi_4_saat_001", "Tek dört saat ekran süreli telefon", "yardimci-nesneler/esya/telefon", "13-15-tohum", 13, "D5", "günde dört saat!", ["telefon_ekran_suresi_4_saat", "telefon_dort_saat"], "telefon_mobil_001", "Aynı tek kırmızı telefonda EKRAN SÜRESİ / Günde / 4 saat. Öykünün dört saat verisi önceki testin üç saatiyle karıştırılmaz; ek grafik/uygulama/gerçek kullanıcı verisi yok."], ["telefon_sarj_bitmis_001", "Tek şarjı bitmiş telefon", "yardimci-nesneler/esya/telefon", "13-15-tohum", 13, "D1", "Şarjım bitti.", ["telefon_sarj_bitmis", "telefon_batarya_bos", "telefon_sarjsiz"], "telefon_mobil_001", "Tek telefon ekranında ŞARJ BİTTİ, boş pil simgesi ve 0%. Pil telefonu temsil eden aynı kâğıt yüzeyinin mürekkep çizimidir, ayrı nesne veya şarj kablosu yok."], ["telefon_sessiz_001", "Tek sessiz modda telefon", "yardimci-nesneler/esya/telefon", "13-15-tohum", 13, "D6", "Telefonun sessizde mi?", ["telefon_sessiz", "telefon_sessiz_mod"], "telefon_mobil_001", "Tek telefon ekranında SESSİZ yazısı ve üzeri çapraz çizilmiş zil simgesi. Simge tek kâğıt nesnenin yüzeyinde; ayrı zil veya titreşim çizgileri yok."]]')
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/tohum_13_15_on_kaniti.json'
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
