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
specs=json.loads("[[\"kup_oyuncak_tek_001\",\"Tek oyuncak küp\",\"yardimci-nesneler/oyun/oyuncak-kup\",\"4-6-tohum\",4,\"D2\",\"küp\",[\"kup_oyuncak\",\"oyuncak_kup\"],null,\"Tek sade oyuncak küp; üç görünen eş kare yüz perspektifte, turuncu ön/turkuaz yan/sarı üst. Nokta, sayı, harf, kalp veya ikinci blok yok. Zar başka nesnedir; geometrik ölçüm şeması değil genel küp oyuncağı.\"],[\"boncuk_tek_001\",\"Tek delikli boncuk\",\"yardimci-nesneler/oyun/boncuk\",\"4-6-tohum\",4,\"D5\",\"boncuk\",[\"boncuk_tek\",\"boncuk_delikli\"],null,\"Tek iri turkuaz yuvarlak boncuk, merkezde gerçek alfa ip geçirme deliği ve beyaz iç makas payı. İp, kolye, başka boncuk veya yüz yok. Nazar boncuğu farklı motif/işlev; sahnede küçük ölçeklenecek.\"],[\"yogurt_kasesi_001\",\"Tek kâsede sade yoğurt\",\"yardimci-nesneler/yiyecek/yogurt\",\"4-6-tohum\",9,\"D4\",\"bir kase yoğurt\",[\"yogurt\"],null,\"Tek mavi kâse içinde sade beyaz yoğurt, yüzeyde hafif kaşık girdabı çizgisi. İçerik ve kâse bir yemek nesnesi; ayrı kaşık, meyve veya ek yiyecek yok. Beyaz yoğurt opak kâğıt, pastel mavi dolgu değil.\"],[\"besik_bos_001\",\"Tek boş beşik\",\"yardimci-nesneler/ev/besik\",\"4-6-tohum\",10,\"D2\",\"beşik\",[\"besik\"],null,\"Tek boş ahşap renkli bebek beşiği; gövdeye bağlı iki kavisli sallanma ayağı, baş/ayak uçları ve parmaklıklı uzun yan. İçte sade mavi yatak yüzeyi; bebek, yastık, oyuncak veya örtü yok. Genel anlatı aksesuarı; gerçek ürün/güvenli uyku tasarımı iddiası yok.\"],[\"bere_tek_001\",\"Tek bere\",\"yardimci-nesneler/giyim/bere\",\"4-6-tohum\",13,\"D5\",\"bere\",[\"bere_tek\",\"bere\"],null,\"Tek yuvarlak kış beresi, katlı alt kenar ve bağlı küçük ponpon. Tekstil örgü fotoğrafı/dokusuyla değil yoğun keçeli kalem çizimi; baş/kişi yok. Mutfak bonesi ve siperli/parti şapkasından farklı.\"],[\"taksi_yandan_001\",\"Tek taksi\",\"yardimci-nesneler/ulasim/taksi\",\"4-6-tohum\",15,\"D4\",\"taksi\",[\"taksi\"],null,\"Tek sarı sedan taksi yandan, iki görünür tekerlek, üstte gövdeye bağlı TAKSİ levhası ve boş mavi camlar. Oyuncak arabadan araç işlevi farklı; gerçek plaka/firma/ücret/yolcu/şoför yok.\"],[\"helikopter_yandan_001\",\"Tek helikopter\",\"yardimci-nesneler/ulasim/helikopter\",\"4-6-tohum\",15,\"D4\",\"helikopter\",[\"helikopter\"],null,\"Tek yandan helikopter; kabin, kuyruk, gövdeye bağlı ana rotor direği ve kanatları, kuyruk rotoru, bağlı iniş kızakları. Dönüş çizgisi/ayrı pervane/hava sahnesi yok. Genel biçim; mühendislik veya belirli model kopyası değil.\"],[\"itfaiye_araci_yandan_001\",\"Tek itfaiye aracı\",\"yardimci-nesneler/ulasim/itfaiye-araci\",\"4-6-tohum\",15,\"D5\",\"itfaiye\",[\"itfaiye\"],null,\"Tek kırmızı itfaiye aracı; kapalı kabin, bağlı üst katlı merdiven, yan bölme kapakları ve iki görünür tekerlek. Ateş, hortumdan su, insan veya ayrı alet yok; kurum/numara/işlevsel kurtarma şeması yok.\"],[\"ambulans_yandan_001\",\"Tek ambulans\",\"yardimci-nesneler/ulasim/ambulans\",\"4-6-tohum\",15,\"D5\",\"ambulans\",[\"ambulans\"],null,\"Tek krem/turuncu ambulans minibüsü, mavi camlar, kapalı arka bölüm, iki görünür tekerlek ve bağlı mavi tavan lambası. AMBULANS yazısı; kişi/yaralı/kan yok. Kızılhaç/Kızılay logosu veya gerçek hizmet numarası kullanılmaz.\"],[\"gozluk_optik_001\",\"Tek gündelik gözlük\",\"yardimci-nesneler/giyim/gozluk\",\"4-6-tohum\",16,\"D1\",\"gözlük\",[\"gozluk_optik\",\"gozluk_gundelik\"],null,\"Tek iki yuvarlak camlı gündelik gözlük, bağlı burun köprüsü ve iki yana uzanan saplar. Koruyucu gözlükten farklı ince çerçeve; camların içi kâğıt çizimi olarak opak açık mavi, dış ara boşluklar alfa. Baş/kişi/ölçü/tıbbi numara yok.\"],[\"terlik_tek_001\",\"Tek ev terliği\",\"yardimci-nesneler/giyim/terlik\",\"4-6-tohum\",16,\"D5\",\"terlik\",[\"terlik\"],null,\"Tek önü kapalı arkası açık ev terliği, üstten üç çeyrek görünümde turuncu üst ve mavi iç taban. İkinci terlik/ayak/bacak yok. Spor ayakkabısı, bot ve dans ayakkabısından ayrı biçim.\"],[\"dugme_tek_001\",\"Tek dört delikli düğme\",\"yardimci-nesneler/giyim/dugme\",\"4-6-tohum\",16,\"D5\",\"düğme\",[\"dugme_tek\",\"giysi_dugmesi\"],null,\"Tek yuvarlak turuncu giysi düğmesi, merkezde 2×2 düzeninde dört gerçek alfa deliği ve her delikte beyaz iç makas payı. İğne/ip/ikinci düğme/giysi yok; teknoloji düğmesi değil. Sahnede doğal küçük ölçek kullanılmalı.\"]]")
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/tohum_4_6_kuyruk_kaniti.json'
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
