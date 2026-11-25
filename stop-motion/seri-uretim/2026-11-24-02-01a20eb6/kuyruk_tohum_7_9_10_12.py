"""Reconcile seventeen curriculum needs against canonical records, files and live queue."""
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
specs=json.loads("[[\"kalemlik_bos_001\",\"Tek boş masa kalemliği\",\"yardimci-nesneler/okul/kalemlik\",\"7-9-tohum\",2,\"D3\",\"kalemlik\",[\"kalemlik\"],null,\"Kaynak testinde içinde kalemler olan kap geçiyor. Montaj için tek boş turkuaz silindirik masa kalemliği ayrıştırılır; üstte açık oval ağız, içi koyu mavi opak. Kalemler bu PNG'de yok; mevcut kalem ayrı katmanda eklenebilir. Kapalı kalem kutusundan farklı masa kabı.\"],[\"seftali_butun_001\",\"Tek bütün şeftali\",\"yardimci-nesneler/yiyecek/seftali\",\"7-9-tohum\",8,\"D4\",\"şeftali\",[\"seftali\"],null,\"Tek bütün turuncu-pembe şeftali; belirgin orta yarık çizgisi, kısa sap ve ona bağlı bir küçük yeşil yaprak. Tüy fotoğraf dokusu yerine yoğun marker taraması; ayrı dilim, çekirdek veya tabak yok.\"],[\"kavun_butun_001\",\"Tek bütün kavun\",\"yardimci-nesneler/yiyecek/kavun\",\"7-9-tohum\",8,\"D4\",\"kavun\",[\"kavun\"],null,\"Tek bütün sarı oval kavun; düzensiz oker kabuk çizgileri, kısa kahverengi sap. Karpuzdan farklı sarı kabuk, ayrı dilim/çekirdek/yaprak yok.\"],[\"mandalina_butun_001\",\"Tek bütün mandalina\",\"yardimci-nesneler/yiyecek/mandalina\",\"7-9-tohum\",8,\"D4\",\"mandalina\",[\"mandalina\"],null,\"Tek basık yuvarlak turuncu mandalina, üstte küçük yeşil çanak izi ve hafif segment kıvrımları. Portakaldan belirgin basık biçim; kabuk soyulmuş değil, ayrı dilim veya yaprak yok.\"],[\"recel_kavanozu_kapali_001\",\"Tek kapalı çilek reçeli kavanozu\",\"yardimci-nesneler/yiyecek/recel\",\"7-9-tohum\",9,\"D2\",\"çilek reçeli kavanozu\",[\"recel\"],null,\"Tek kapalı çilek reçeli kavanozu; kırmızı opak gövde, mavi kapak, krem etikette ÇİLEK REÇELİ ve küçük basılı çilek motifi. Kavanoz tek fiziksel nesne, dışarıda meyve/kaşık yok.\"],[\"tavuk_but_pismis_001\",\"Tek pişmiş tavuk budu\",\"yardimci-nesneler/yiyecek/pismis-tavuk\",\"7-9-tohum\",9,\"D3\",\"tavuk\",[\"tavuk_but\",\"pismis_tavuk\"],null,\"Kahvaltı/yiyecek dersi bağlamında tek pişmiş tavuk budu; altın kahverengi et ve bağlı kısa krem kemik ucu. Canlı hayvan karakteri değil yiyecek, kan/çiğ et/tabak/ikinci parça yok.\"],[\"patates_kizartmasi_tek_001\",\"Tek patates kızartması çubuğu\",\"yardimci-nesneler/yiyecek/patates-kizartmasi\",\"7-9-tohum\",9,\"D3\",\"patates kızartması\",[\"patates_kizartmasi\"],null,\"Tek altın sarı kızarmış patates çubuğu, hafif eğri dikdörtgen prizma ve koyu oker kızarmış kenarlar. Çoklu porsiyon için sahnede çoğaltılabilir; bu PNG'de yalnız bir çubuk, kutu/tabak/sos yok.\"],[\"sucuk_halka_001\",\"Tek bütün sucuk halkası\",\"yardimci-nesneler/yiyecek/sucuk\",\"7-9-tohum\",9,\"D4\",\"sucuk\",[\"sucuk\"],null,\"Tek kızıl kahverengi U biçimli bütün sucuk; iki kapalı uç üstte birbirine yakın, açık orta boşluk dış alfa ile birleşir. Bağ ipi veya ayrı dilimler yok; bir kâğıt silueti, beyaz iç/dış kesim payı.\"],[\"oyuncak_kutusu_bos_001\",\"Tek boş oyuncak kutusu\",\"yardimci-nesneler/oyun/oyuncak-kutusu\",\"7-9-tohum\",13,\"D5\",\"oyuncak kutusu\",[\"oyuncak_kutusu\"],null,\"Tek kapaksız boş turkuaz saklama kutusu; ön yüzde OYUNCAK yazısı, turuncu kenar, koyu mavi iç taban. Oyuncaklar/kapak ayrı nesne yok; kayıp eşya/bağış kutusundan işlev ve açık biçim farklı.\"],[\"kukla_el_001\",\"Tek el kuklası oyuncağı\",\"yardimci-nesneler/oyun/kukla\",\"7-9-tohum\",13,\"D5\",\"kukla\",[\"kukla\"],null,\"Tek basit el kuklası oyuncağı: yuvarlak krem yüz, turuncu saç başa bağlı, mavi eldiven biçimli gövde ve iki kısa bağlı kol. İçinde insan eli yok; ip/çubuk/ikinci kukla yok. Oyuncak genel insanımsı figür, mevcut karakterin yeniden üretimi değil.\"],[\"motosiklet_yandan_001\",\"Tek motosiklet\",\"yardimci-nesneler/ulasim/motosiklet\",\"7-9-tohum\",17,\"D7\",\"motosiklet\",[\"motosiklet\",\"motorsiklet\"],null,\"Tek mavi/turuncu motosiklet yandan; iki görünür tekerlek, yakıt deposu, siyah sele, motor bloğu, ön çatal ve bağlı gidon. Sürücü/kask/yol/plaka yok; bisikletten motorlu gövdeyle farklı. Büyük çerçeve açıklıkları gerçek alfa beyaz iç paylı.\"],[\"yaris_arabasi_yandan_001\",\"Tek yarış arabası\",\"yardimci-nesneler/ulasim/yaris-arabasi\",\"7-9-tohum\",17,\"D7\",\"yarış arabası\",[\"yaris_arabasi\"],null,\"Tek alçak turuncu yarış otomobili yandan, mavi kapalı kokpit camı, iki görünür siyah tekerlek ve gövdeye bağlı kısa arka kanat. Marka/numara/sürücü/yol yok; oyuncak ve genel otomobilden yarış gövdesi biçimiyle farklı.\"],[\"ambalaj_kagidi_tek_001\",\"Tek ambalaj kâğıdı yaprağı\",\"yardimci-nesneler/kutlama/ambalaj-kagidi\",\"7-9-tohum\",18,\"D5\",\"ambalaj kâğıdı\",[\"ambalaj\"],null,\"Tek hafif kıvrık turkuaz ambalaj kâğıdı yaprağı; yüzeyde düzensiz dağılmış basılı turuncu küçük yıldızlar. Desen aynı kâğıdın parçası, ayrı yıldız nesneleri değil. Hediye kutusu/makas/rulo/ikinci yaprak yok.\"],[\"banknot_ornek_001\",\"Tek örnek kâğıt para\",\"yardimci-nesneler/belgeler/banknot\",\"7-9-tohum\",18,\"D3\",\"kâğıt para ve bozuk para\",[\"banknot\",\"kagit_para\"],null,\"Kaynak bileşik resmindeki tek kâğıt para bileşeni; yeşil hayali oyun parası üzerinde PARA / ÖRNEK ve küçük basılı yıldız. Gerçek para birimi, değer, portre, seri numarası veya güvenlik tasarımı yok. Mevcut bozuk para ayrı katmanda kullanılabilir.\"],[\"dosya_kapali_001\",\"Tek kapalı dosya\",\"yardimci-nesneler/okul/dosya\",\"10-12-tohum\",3,\"D7\",\"dosya\",[\"dosya\"],null,\"Tek kapalı turuncu karton evrak dosyası, üstte küçük bağlı sekme ve lacivert kat çizgisi. İçinden ayrı belge taşmaz, yazı/klips/el/ikinci dosya yok.\"],[\"ispanak_yaprak_tek_001\",\"Tek ıspanak yaprağı\",\"yardimci-nesneler/yiyecek/ispanak\",\"10-12-tohum\",7,\"D7\",\"ıspanak\",[\"ispanak\"],null,\"Tek koyu yeşil geniş oval ıspanak yaprağı ve bağlı kısa sap; bir orta damar ve düzensiz yan damarlar. Yemek bağlamındaki bitkisel malzemenin tek nesne bileşeni, demet/tencere/toprak/ikinci yaprak yok.\"],[\"kayisi_butun_001\",\"Tek bütün kayısı\",\"yardimci-nesneler/yiyecek/kayisi\",\"10-12-tohum\",8,\"D6\",\"kayısı\",[\"kayisi\"],null,\"Tek küçük bütün altın turuncu kayısı; oval biçim, bir ince dikiş/yarık çizgisi ve üstte küçük kahverengi sap çukuru. Şeftaliden daha düzgün oval, belirgin pembe alan/yaprak yok; ayrı çekirdek/dilim yok.\"]]")
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/tohum_7_9_10_12_kuyruk_kaniti.json'
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
