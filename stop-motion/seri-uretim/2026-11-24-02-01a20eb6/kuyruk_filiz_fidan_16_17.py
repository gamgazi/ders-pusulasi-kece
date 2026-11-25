"""Reconcile fifteen curriculum needs against canonical records, files and live queue."""
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
specs=json.loads("[[\"yaka_karti_001\",\"Tek boş yaka kartı\",\"yardimci-nesneler/kirtasiye/yaka-karti\",\"16-17-filiz\",4,\"D4\",\"yaka kartı\",[\"yaka_karti\"],null,\"İş yerindeki yaka kartı için tek klipsi gövdesine bağlı kartlık. GÖREVLİ ve ÖRNEK başlığı, boş Ad alanı; kişi fotoğrafı, kişisel veri, marka veya resmi kimlik yok. Boyun ipi eklenmez.\"],[\"bone_mutfak_001\",\"Tek boş mutfak bonesi\",\"yardimci-nesneler/giyim/mutfak-bonesi\",\"16-17-filiz\",4,\"D4\",\"Mutfakta çalışırken bone takmalısın.\",[\"bone\"],null,\"Mutfak hijyeni bağlamında tek boş yuvarlak büzgülü mavi bone. Baş, saç, kişi, şef şapkası veya tekstil fotoğrafı yok; kâğıda marker çizimidir. Koruyuculuk veya kullanım talimatı verilmez.\"],[\"fatura_ornek_001\",\"Tek boş örnek fatura\",\"yardimci-nesneler/kirtasiye/fatura\",\"16-17-filiz\",9,\"D4\",\"fatura\",[\"fatura\"],null,\"Elektrik/su/internet ev gideri bağlamında FATURA / ÖRNEK, boş Dönem ve Tutar alanlı tek sahne kâğıdı. Gerçek hesap, adres, borç, ödeme kodu, firma veya tutar yok; alışveriş fişi ile karıştırılmaz.\"],[\"kar_lastigi_tek_001\",\"Tek otomobil kar lastiği\",\"yardimci-nesneler/ulasim/kar-lastigi\",\"16-17-filiz\",11,\"D6\",\"kar lastiği\",[\"kar_lastigi\",\"kis_lastigi\"],null,\"Tek jantsız şişkin siyah-lacivert otomobil dış lastiği, derin blok dişleri ve ince kısa lamel çizgileri. İç lastik/yama farklı nesnelerdir. Model, ölçü, sertifika sembolü veya güvenlik performansı iddiası yok.\"],[\"menemen_tava_001\",\"Tek tavada menemen\",\"yardimci-nesneler/yiyecek/menemen\",\"16-17-filiz\",14,\"D4\",\"Menemeni domates, biber ve yumurtadan yaparız.\",[\"menemen\"],null,\"Domates, yeşil biber ve yumurtalı menemen tek küçük sahanın içinde birleştirilmiş yemek nesnesi. Ayrı malzemeler, tabaklar, ekmek veya set yok. Boş tavadan farklı dolu yemek durumu; belirli bölgesel reçete/ölçü iddiası yok.\"],[\"hurma_tek_001\",\"Tek bütün hurma\",\"yardimci-nesneler/yiyecek/hurma\",\"16-17-filiz\",14,\"D4\",\"Ramazanda orucu hurmayla açarız.\",[\"hurma\"],null,\"Tek kahverengi oval buruşuk bütün hurma meyvesi, bir uçta küçük sap izi; açık çekirdek veya dal/salkım yok. Kaynak aile geleneği tüm insanların kuralı gibi sunulmaz; tür/çeşit teşhis iddiası yok.\"],[\"cezve_bos_001\",\"Tek boş cezve\",\"yardimci-nesneler/mutfak/cezve\",\"16-17-filiz\",14,\"D6\",\"Türk kahvesini cezvede pişiririz.\",[\"cezve\"],null,\"Tek bakır renkli boş açık cezve, geniş alt gövde, dar ağızda küçük dökme dudağı ve uzun bağlı sap. Fincan, kahve paketi, ocak, ateş yok. Kazan/tencereden biçim ve işlevi farklı.\"],[\"kombi_kapali_001\",\"Tek kapalı kombi\",\"yardimci-nesneler/ev/kombi\",\"16-17-filiz\",15,\"D4\",\"Ev sahibi 'Kombiyi yarın tamir ettiririm' dedi.\",[\"kombi\"],null,\"Tek kapalı duvar tipi kombi cihazı dış gövdesi; küçük ekran ve iki düğme. Duvar, tesisat bağlantı şeması, gaz hattı, açık iç parçalar veya tamir talimatı yok. Markasız genel sahne aksesuarı.\"],[\"ilk_yardim_cantasi_001\",\"Tek kapalı ilk yardım çantası\",\"yardimci-nesneler/saglik/ilk-yardim-cantasi\",\"16-17-fidan\",1,\"D6\",\"ilk yardım çantası\",[\"ilk_yardim\"],null,\"Tek kapalı turuncu sert çanta, bağlı üst kulp, önünde İLK YARDIM yazısı. İçerik listesi, ilaç, ayrı malzeme, Kızılhaç/Kızılay logosu veya müdahale talimatı yok.\"],[\"sira_numarasi_fisi_001\",\"Tek sıra numarası fişi\",\"yardimci-nesneler/kirtasiye/sira-numarasi\",\"16-17-fidan\",4,\"D1\",\"Sıra numarasını nereden alıyorum?\",[\"sira_numarasi\",\"sira_fisi\"],null,\"Hizmet bekleme salonu için tek küçük kâğıt fiş, SIRA ve 12 yazısı. Nesne, sorudan çıkarılmış sahne desteğidir; kaynakta gerçek numara belirtilmez. Kurum, gerçek sıra zamanı veya kişisel veri yok; alışveriş fişi farklı işlevdedir.\"],[\"kulak_tikaci_tek_001\",\"Tek kulak tıkacı\",\"yardimci-nesneler/saglik/kulak-tikaci\",\"16-17-fidan\",7,\"D3\",\"kulak tıkacı\",[\"kulak_tikaci\"],null,\"Tek turuncu yumuşak köpük biçimli kısa konik kulak tıkacı; yuvarlak uç, geniş düz taban. İkinci tıkaç/kutu/kulak/baş/bağ ipi yok. Tıbbi öneri veya ses azaltma değeri iddiası yok.\"],[\"yazici_uc_boyutlu_001\",\"Tek boş üç boyutlu yazıcı\",\"yardimci-nesneler/teknoloji/uc-boyutlu-yazici\",\"16-17-fidan\",9,\"D6\",\"üç boyutlu yazıcı\",[\"uc_boyutlu_yazici\",\"yazici_uc_boyutlu\"],null,\"Tek masaüstü açık çerçeveli 3B yazıcı; taban, iki dikme, üst köprü, hareket kafası ve boş baskı tablası birbirine bağlı. Ayrı basılmış nesne/filament makarası yok. Normal belge yazıcısından farklıdır; işlevsel makine planı değildir.\"],[\"protez_el_001\",\"Tek genel protez el\",\"yardimci-nesneler/teknoloji/protez-el\",\"16-17-fidan\",9,\"D6\",\"protez el\",[\"protez_el\"],null,\"Tek mekanik el aksesuarı: dört parmak ve karşı yanda tek başparmak, avuç ve kısa bilek bağlantısı bir nesne. Robot kol tabanından farklı; gerçek kişi/anatomik kesik/kan yok. Genel öğretim temsili; kişiye uygunluk, tıbbi veya mekanik üretim şeması iddiası yok.\"],[\"bot_yuruyus_tek_001\",\"Tek yürüyüş botu\",\"yardimci-nesneler/giyim/yuruyus-botu\",\"16-17-fidan\",11,\"D6\",\"yürüyüş botu\",[\"yuruyus_botu\",\"bot_yuruyus\"],null,\"Tek kahverengi yüksek bilekli bağcıklı yürüyüş botu, kalın dişli taban. Tek spor ayakkabısı, sarı yağmur çizmesi ve dans ayakkabısından farklı; çift, bacak, çamur veya manzara yok.\"],[\"yardim_kolisi_kapali_001\",\"Tek kapalı yardım kolisi\",\"yardimci-nesneler/cevre/yardim-kolisi\",\"16-17-fidan\",12,\"D3\",\"yardım kolisi\",[\"yardim_kolisi\"],null,\"Tek kapalı kahverengi karton kutu, bağlı kapaklar üzerindeki bant ve YARDIM etiketi. Bağış toplama kutusu değil dağıtıma hazır koli; içindekiler ayrı gösterilmez. Kurum, gerçek kampanya/yararlanıcı veya logo yok.\"]]")
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/filiz_fidan_16_17_kuyruk_kaniti.json'
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
    item={'id':aid,'title':title,'category':cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':rel,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+pointer,'match':'exact_json_leaf' if value==term else 'substring_of_exact_json_leaf','leaf_sha256':hashlib.sha256(value.encode()).hexdigest()}],'felt_cards_preserved':cardids,'role':'missing pose of existing paper helper' if baseid else 'independent missing paper helper','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} records, {len(canonical)} canonical PNGs, {len(q["items"])} queue items','source_is_action_inference':aid in {'sira_numarasi_fisi_001'},'semantic_review':semantic+' Seçilen tam mevcut ders alanı okundu. Mevcut R/K kartlar ve temel yardımcı nesne dosyaları korunur. Üretim sonrası her PNG için ayrı teknik ve üç görünümde sanatsal QA gerekir; poz hizası/animasyon henüz doğrulanmış değildir. Tüm müfredat ayrıştırması bitmedi.'}
    if reference:item['pose_reference']=reference
    new.append(item)
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blobs_sha_verified':{k:v[1] for k,v in sources.items()},'base_references':[x['pose_reference'] for x in new if 'pose_reference' in x],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'records':len(h),'pngs':len(canonical)}))
