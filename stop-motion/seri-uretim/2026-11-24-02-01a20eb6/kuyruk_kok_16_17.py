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
specs=json.loads("[[\"suzgec_mutfak_001\",\"Tek mutfak süzgeci\",\"yardimci-nesneler/mutfak/suzgec\",\"16-17-kok\",3,\"D4\",\"Makarnayı süzün.\",[\"suzgec\"],null,\"Kaynakta makarnayı süzme eyleminden çıkarılan tek boş çanak biçimli mutfak süzgeci. İki bağlı sap, üç kısa ayak, delikli mavi çanak. Sapların büyük boşlukları gerçek alfa ve beyaz iç makas paylı; küçük delikler koyu basılı gösterim olabilir. Makarna, su, el veya lavabo yok. Eylem çıkarımı açık kaydedilir.\"],[\"sarimsak_butun_001\",\"Tek bütün sarımsak\",\"yardimci-nesneler/yiyecek/sarimsak\",\"16-17-kok\",3,\"D6\",\"sarımsak\",[\"sarimsak\"],null,\"Tek bütün sarımsak başı, krem/mor yoğun marker dilim sınırları, kısa kuru boyun; ayrı diş, bıçak veya insan yok.\"],[\"mercimek_paketi_kapali_001\",\"Tek kapalı mercimek paketi\",\"yardimci-nesneler/mutfak/mercimek\",\"16-17-kok\",3,\"D7\",\"mercimek\",[\"mercimek\"],null,\"Tek kapalı krem/turuncu mercimek paketi, MERCİMEK yazısı ve pakete basılı küçük turuncu mercimek taneleri motifi. Ayrı taneler, marka veya gramaj yok.\"],[\"kimyon_kavanozu_kapali_001\",\"Tek kapalı kimyon kavanozu\",\"yardimci-nesneler/mutfak/kimyon\",\"16-17-kok\",3,\"D7\",\"kimyon\",[\"kimyon\"],null,\"Tek küçük kapalı baharat kavanozu; oker kimyonu temsil eden opak gövde, turkuaz kapak ve KİMYON etiketi. Toz dökülmesi, kaşık, marka veya miktar yok.\"],[\"kepce_tek_001\",\"Tek kepçe\",\"yardimci-nesneler/mutfak/kepce\",\"16-17-kok\",3,\"D7\",\"kepçe\",[\"kepce\"],null,\"Tek boş mutfak kepçesi; uzun mavi sap ve derin yuvarlak gri kepçe çanağı bağlı, hafif üç çeyrek açı. Sıvı, yemek, tencere veya ikinci gereç yok.\"],[\"kravat_tek_001\",\"Tek kravat\",\"yardimci-nesneler/giysi/kravat\",\"16-17-kok\",4,\"D6\",\"kravat\",[\"kravat\"],null,\"Tek kırmızı bağlanmış kravat, üstte küçük düğüm ve altta tek uzun sivri uç; iki çapraz turkuaz şerit basılı desen. Boyun/kişi/gömlek yok.\"],[\"ayakkabi_topuklu_tek_001\",\"Tek topuklu ayakkabı\",\"yardimci-nesneler/giysi/topuklu-ayakkabi\",\"16-17-kok\",4,\"D6\",\"topuklu ayakkabı\",[\"topuklu\"],null,\"Tek mor kapalı burunlu kadın ayakkabısı yandan; bir orta kalınlıkta topuk, turuncu iç taban, ayak bileği kayışı yok. İnsan/ayak/çift yok.\"],[\"etek_tek_001\",\"Tek etek\",\"yardimci-nesneler/giysi/etek\",\"16-17-kok\",4,\"D7\",\"etek\",[\"etek\"],null,\"Tek turkuaz A kesim etek önden, kapalı bel bandı ve üç lacivert düşey kat çizgisi, hafif düzensiz alt kenar. Kişi/askı/ikinci giysi yok.\"],[\"kimlik_karti_ornek_001\",\"Tek örnek kimlik kartı\",\"yardimci-nesneler/belgeler/kimlik-karti\",\"16-17-kok\",5,\"D4\",\"kimlik kartı\",[\"kimlik\"],null,\"Tek turuncu genel örnek kart, KİMLİK KARTI / ÖRNEK ve boş Ad alanı; fotoğraf yerine basılı boş küçük çerçeve. Gerçek resmî tasarım, kişi, kimlik numarası, çip, barkod, imza veya mühür yok.\"],[\"paspas_kapi_tek_001\",\"Tek kapı paspası\",\"yardimci-nesneler/ev/kapi-paspasi\",\"16-17-kok\",5,\"D6\",\"Anahtarı paspasın altına koydum.\",[\"paspas\"],null,\"Tek yatay oker dikdörtgen kapı paspası, koyu kahverengi çevre bandı ve kaba çapraz marker tarama. Gerçek dokuma değil kâğıt çizim. Anahtar/kapı/zemin/ikinci nesne yok.\"],[\"oda_karti_ornek_001\",\"Tek örnek oda kartı\",\"yardimci-nesneler/belgeler/oda-karti\",\"16-17-kok\",5,\"D7\",\"oda kartı\",[\"oda_karti\"],null,\"Tek mavi örnek otel oda kartı; ODA KARTI / ÖRNEK yazısı ve küçük basılı turuncu anahtar simgesi. Otel markası, kişi, oda numarası, erişim kodu, barkod yok.\"],[\"ehliyet_ornek_001\",\"Tek örnek ehliyet\",\"yardimci-nesneler/belgeler/ehliyet\",\"16-17-kok\",6,\"D6\",\"ehliyet\",[\"ehliyet\"],null,\"Tek yeşil genel eğitim kartı; EHLİYET / ÖRNEK ve küçük basılı turuncu direksiyon simgesi. Gerçek resmî belge tasarımı, kişi, tarih, sınıf, kimlik numarası, barkod veya mühür yok.\"],[\"muze_karti_ornek_001\",\"Tek örnek müze kartı\",\"yardimci-nesneler/belgeler/muze-karti\",\"16-17-kok\",13,\"D6\",\"müze kartı\",[\"muze_karti\"],null,\"Tek mor örnek müze giriş kartı; MÜZE KARTI / ÖRNEK yazısı ve basılı turuncu üç sütunlu küçük müze cephesi simgesi. Gerçek marka, kişi, fiyat, geçerlilik veya barkod yok.\"]]")
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/kok_16_17_kuyruk_kaniti.json'
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
    item={'id':aid,'title':title,'category':cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':rel,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+pointer,'match':'exact_json_leaf' if value==term else 'substring_of_exact_json_leaf','leaf_sha256':hashlib.sha256(value.encode()).hexdigest()}],'felt_cards_preserved':cardids,'role':'missing pose of existing paper helper' if baseid else 'independent missing paper helper','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} records, {len(canonical)} canonical PNGs, {len(q["items"])} queue items','source_is_action_inference':aid in {'suzgec_mutfak_001'},'semantic_review':semantic+' Seçilen tam mevcut ders alanı okundu. Mevcut R/K kartlar ve temel yardımcı nesne dosyaları korunur. Üretim sonrası her PNG için ayrı teknik ve üç görünümde sanatsal QA gerekir; poz hizası/animasyon henüz doğrulanmış değildir. Tüm müfredat ayrıştırması bitmedi.'}
    if reference:item['pose_reference']=reference
    new.append(item)
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blobs_sha_verified':{k:v[1] for k,v in sources.items()},'base_references':[x['pose_reference'] for x in new if 'pose_reference' in x],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'records':len(h),'pngs':len(canonical)}))
