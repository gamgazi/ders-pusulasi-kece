"""Reconcile fourteen specific states after full Kok 13-15 reading and reference inspection."""
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
specs=json.loads('[["mont_kirmizi_001", "Tek kırmızı mont", "yardimci-nesneler/giyim/mont", "13-15-kok", 4, "D1", "Kırmızı bir mont giymiş.", ["mont_kirmizi", "kirmizi_mont"], "mont_mavi_001", "Mavi montun kırmızı sürümü; aynı tek giysi, turuncu fermuar ve beyaz kâğıt kesimi korunur."], ["elbise_mor_duz_001", "Tek düz mor elbise", "yardimci-nesneler/giyim/elbise", "13-15-kok", 4, "D5", "düz renk, mor bir elbise giymiş.", ["elbise_mor", "mor_elbise"], "elbise_tek_001", "Mevcut mavi elbise yerine düz mor; turuncu bel bandı da mor olur. Tek elbise, kişi veya aksesuar eklenmez."], ["hirka_turuncu_001", "Tek turuncu hırka", "yardimci-nesneler/giysi/hirka", "13-15-kok", 4, "D8", "Turuncu bir hırka giymiş.", ["hirka_turuncu", "turuncu_hirka"], "hirka_kapali_001", "Mevcut yeşil kapalı düğmeli hırkanın turuncu gövdeli sürümü. Tek giysi, koyu hat ve bağlı düğme çizimleri; gerçek örgü değil marker kâğıt."], ["kazak_kahverengi_001", "Tek kahverengi kazak", "yardimci-nesneler/giyim/kazak", "13-15-kok", 4, "D8", "kahverengi", ["kazak_kahverengi", "kahverengi_kazak"], "kazak_tek_001", "Aynı sorudaki Bu ___ kazak sana çok yakışmış cümlesinin doğru kahverengi yanıtına bağlı sürüm. Turuncu temel kazak korunur."], ["kazak_cizgili_001", "Tek çizgili kazak", "yardimci-nesneler/giyim/kazak", "13-15-kok", 4, "D6", "Eylül çizgili bir kazak giymiş.", ["kazak_cizgili", "cizgili_kazak"], "kazak_tek_001", "Tek kazağın gövde ve kollarında geniş yatay turuncu/lacivert şeritler; kaynak şerit rengini belirtmediği için renk tasarım tercihi olarak kaydedilir."], ["tisort_kolsuz_001", "Tek kolsuz tişört", "yardimci-nesneler/giyim/tisort", "13-15-kok", 4, "D6", "Kolsuz tişört giymiş.", ["tisort_kolsuz", "kolsuz_tisort"], "tisort_tek_001", "Sarı temel tişörtün kolsuz sürümü; kol çıkıntıları kaldırılır, iki omuz askısı ve kol oyuklarında beyaz makas payı olur. Tek giysi."], ["telefon_sinyal_yok_001", "Tek sinyal olmayan telefon", "yardimci-nesneler/esya/telefon", "13-15-kok", 12, "D3", "Telefon çekmiyor.", ["telefon_sinyal_yok", "telefon_cekmiyor"], "telefon_mobil_001", "Tek kırmızı telefon ekranında SİNYAL YOK ve üstü çizilmiş sinyal çubukları. Gerçek cihaz/operatör veya bağlantı iddiası yok."], ["telefon_ucak_modu_001", "Tek uçak modunda telefon", "yardimci-nesneler/esya/telefon", "13-15-kok", 12, "D6", "uçak modu", ["telefon_ucak_modu", "telefon_ucus_modu"], "telefon_mobil_001", "Tek kırmızı telefon ekranında UÇAK MODU ve tek uçak simgesi; uçak aynı ekranın mürekkep çizimi, ayrı taşıt PNG değil."], ["telefon_cevapsiz_3_001", "Tek üç cevapsız aramalı telefon", "yardimci-nesneler/esya/telefon", "13-15-kok", 12, "D4", "Telefonumda üç cevapsız arama var.", ["telefon_cevapsiz_3", "telefon_uc_cevapsiz"], "telefon_mobil_001", "Tek ekran metni 3 / CEVAPSIZ / ARAMA; isim, numara veya ayrı çağrı satırları eklenmez."], ["telefon_cevapsiz_1_001", "Tek bir cevapsız aramalı telefon", "yardimci-nesneler/esya/telefon", "13-15-kok", 12, "D5", "bir cevapsız arama var.", ["telefon_cevapsiz_1", "telefon_bir_cevapsiz"], "telefon_mobil_001", "Öyküdeki bir arama ayrı durum: 1 / CEVAPSIZ / ARAMA. Üç aramalı testle karıştırılmaz; gerçek kişi veya numara yok."], ["geri_donusum_plastik_kutusu_001", "Tek plastik geri dönüşüm kutusu", "yardimci-nesneler/cevre/geri-donusum-kutusu", "13-15-kok", 15, "D5", "plastik, kâğıt ve cam için farklı kutular var.", ["geri_donusum_plastik", "plastik_geri_donusum", "plastik_kutusu"], "geri_donusum_kutusu_001", "Mevcut KÂĞIT kutusu korunur; PLASTİK yazısı ve yüzeye çizilmiş şişe simgesi taşıyan tek sarı kutu. Renk resmî kod/standart iddiası taşımaz."], ["geri_donusum_cam_kutusu_001", "Tek cam geri dönüşüm kutusu", "yardimci-nesneler/cevre/geri-donusum-kutusu", "13-15-kok", 15, "D5", "plastik, kâğıt ve cam için farklı kutular var.", ["geri_donusum_cam", "cam_geri_donusum", "cam_kutusu"], "geri_donusum_kutusu_001", "Tek yeşil kutuda CAM ve yüzeye çizilmiş şişe simgesi; kâğıt kutusundan farklı ders nesnesi. Renk resmî kod/standart iddiası taşımaz."], ["atik_pil_kutusu_001", "Tek atık pil kutusu", "yardimci-nesneler/cevre/atik-pil-kutusu", "13-15-kok", 15, "D5", "atık pil kutusu", ["atik_pil_kutusu", "pil_toplama_kutusu", "pil_atik_kutusu"], "geri_donusum_kutusu_001", "Tek turuncu kutuda ATIK PİL ve pil simgesi, tümü kutunun yüzeyinde. Ek pil/parça, marka veya bertaraf talimatı eklenmez."], ["musluk_uyari_notu_001", "Tek musluk uyarı notu", "yardimci-nesneler/belgeler/not", "13-15-kok", 15, "D5", "Musluğu açık bırakmamalıyız!", ["musluk_uyari_notu", "musluk_acik_birakma_notu"], "not_karti_tek_001", "Tek sarı kâğıt notta dersin Musluğu açık bırakmamalıyız! cümlesi. Mevcut sunum notu metni değiştirilmiş yeni durum; ayrı musluk nesnesi yok."]]')
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/kok_13_15_on_dort_kaniti.json'
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
