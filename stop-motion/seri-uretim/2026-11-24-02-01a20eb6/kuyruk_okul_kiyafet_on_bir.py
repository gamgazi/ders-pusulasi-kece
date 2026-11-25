"""Reconcile eleven needs after full Tohum/Kok reading, including visual color-reference review."""
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
specs=json.loads("[[\"saat_calar_12_00_001\",\"Saat 12.00 gösteren çalar saat\",\"yardimci-nesneler/esya/saat\",\"10-12-tohum\",5,\"D5\",\"Öğle yemeği saat on ikide.\",[\"saat_calar_12_00\",\"saat_12_00\"],\"saat_calar_001\",\"Mevcut çalar saatte iki ibre tam yukarı: kısa kalın akrep ile daha uzun ince yelkovan ortak merkezde üst üste. 12 rakamıyla birleşme yok. Zaman ifadesinden poz çıkarımı.\"],[\"kalem_kutusu_acik_001\",\"Tek açık boş kalem kutusu\",\"yardimci-nesneler/okul/kalem-kutusu\",\"10-12-tohum\",3,\"D5\",\"Kalem kutusunda kalem, silgi ve kalemtıraş var.\",[\"kalem_kutusu_acik\",\"kalemkutusu_acik\"],\"kalem_kutusu_kapali_001\",\"Mevcut turkuaz kapaklı mavi kutunun kapağı arkaya açılmış boş pozu; kapak menteşe boyunca bağlı, turuncu kilit önde. İçindeki nesneler sahnede ayrı mevcut PNG'lerle kurulacak; tek PNG'de yalnız kutu. İç mekân ilişkisinden açık poz çıkarımı.\"],[\"kopek_yatagi_bos_001\",\"Tek boş köpek yatağı\",\"yardimci-nesneler/evcil-hayvan/kopek-yatagi\",\"10-12-kok\",3,\"D5\",\"Köpeğin yatağı buzdolabıyla masanın arasında.\",[\"kopek_yatagi\",\"kopek_yatak\",\"hayvan_yatagi\",\"evcil_yatagi\"],null,\"Tek alçak oval evcil köpek yatağı; turkuaz yükseltilmiş yumuşak kenarlık ve bunun içine dikili turuncu oval taban. Ön kenar biraz alçak. Tek bütün eşya; ayrı yastık, köpek, ayakkabı veya oda yok. Ürünün kendisi çizilmiş kâğıt; kumaş fotoğrafı/dokusu yok.\"],[\"hirka_kirmizi_001\",\"Tek kırmızı düğmeli hırka\",\"yardimci-nesneler/giysi/hirka\",\"10-12-kok\",6,\"D5\",\"Bu kırmızı hırka kimin?\",[\"hirka_kirmizi\",\"kirmizi_hirka\"],\"hirka_kapali_001\",\"Mevcut yeşil hırkanın aynı dört turuncu düğme ve iki cepli kimliğinde kırmızı renk çeşidi. Gerçek örgü değil keçeli kalem kâğıt çizimi.\"],[\"kazak_kirmizi_001\",\"Tek kırmızı kazak\",\"yardimci-nesneler/giyim/kazak\",\"10-12-kok\",6,\"D1\",\"Kırmızı bir kazak giymiş.\",[\"kazak_kirmizi\",\"kirmizi_kazak\"],\"kazak_tek_001\",\"Mevcut turuncu kazağın aynı uzun kollu yuvarlak yaka formunda kırmızı çeşidi; lacivert yaka, manşet ve etek ucu korunur.\"],[\"kazak_mavi_001\",\"Tek mavi kazak\",\"yardimci-nesneler/giyim/kazak\",\"10-12-kok\",6,\"D5\",\"Ahmet mavi bir kazak giymiş.\",[\"kazak_mavi\",\"mavi_kazak\"],\"kazak_tek_001\",\"Mevcut turuncu kazağın aynı uzun kollu yuvarlak yaka formunda doygun mavi çeşidi; lacivert yaka, manşet ve etek ucu korunur.\"],[\"gomlek_beyaz_001\",\"Tek beyaz kısa kollu gömlek\",\"yardimci-nesneler/giyim/okul-uniformasi\",\"10-12-kok\",6,\"D4\",\"Kim beyaz gömlek giymiş?\",[\"gomlek_beyaz\",\"beyaz_gomlek\"],\"uniforma_gomlek_001\",\"Mevcut mavi kısa kollu yakalı gömleğin beyaz çeşidi; beş düğme ve tek göğüs cebi korunur. Beyaz gövde opak kâğıt üzerinde soğuk açık gri mürekkep izleriyle okunur; dış makas payı beyaz, kontur lacivert. Boyun boşluğunun çevresinde beyaz kâğıt kesim payı.\"],[\"etek_kirmizi_001\",\"Tek kırmızı etek\",\"yardimci-nesneler/giysi/etek\",\"10-12-kok\",6,\"D2\",\"Kız kırmızı bir\",[\"etek_kirmizi\",\"kirmizi_etek\"],\"etek_tek_001\",\"D2 tamamlamanın doğru cevabı etek; kırmızı renk+etek ders bağlamında birleşir. Mevcut turkuaz pilili eteğin kırmızı çeşidi; bel bandı ve üç düzensiz pile çizgisi korunur.\"],[\"etek_yesil_001\",\"Tek yeşil etek\",\"yardimci-nesneler/giysi/etek\",\"10-12-kok\",6,\"D9\",\"Yeşil bir etek giymiş.\",[\"etek_yesil\",\"yesil_etek\"],\"etek_tek_001\",\"Mevcut turkuaz pilili eteğin açıkça yeşil çeşidi; bel bandı ve üç düzensiz pile çizgisi korunur.\"],[\"tisort_cizgili_kirmizi_beyaz_001\",\"Tek kırmızı beyaz çizgili tişört\",\"yardimci-nesneler/giyim/tisort\",\"10-12-kok\",6,\"D6\",\"Ahmet kırmızı beyaz çizgili bir tişört giymiş.\",[\"tisort_cizgili\",\"cizgili_tisort\",\"tisort_kirmizi_beyaz\"],\"tisort_tek_001\",\"Mevcut sarı kısa kollu tişörtün kırmızı-beyaz geniş yatay çizgili çeşidi; aynı siluet, yaka kırmızı. Beyaz bantlar kâğıt üzerinde opak. Desen tek giysinin yüzeyidir; ayrı varlık dizisi değil.\"],[\"tisort_beyaz_001\",\"Tek beyaz tişört\",\"yardimci-nesneler/giyim/tisort\",\"10-12-kok\",6,\"D1\",\"Bugün beyaz bir tişört\",[\"tisort_beyaz\",\"beyaz_tisort\"],\"tisort_tek_001\",\"Mevcut sarı kısa kollu tişörtün beyaz çeşidi; yaka beyaz, gövde opak beyaz üzerinde soğuk açık gri geniş mürekkep vuruşları ve lacivert kontur. Beyaz makas payı korunur; şeffaf iç boşluklar oluşturulmaz.\"]]")
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/tohum_kok_10_12_on_bir_kaniti.json'
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
    item={'id':aid,'title':title,'category':cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':rel,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+pointer,'match':'exact_json_leaf' if value==term else 'substring_of_exact_json_leaf','leaf_sha256':hashlib.sha256(value.encode()).hexdigest()}],'felt_cards_preserved':cardids,'role':'missing pose of existing paper helper' if baseid else 'independent missing paper helper','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} records, {len(canonical)} canonical PNGs, {len(q["items"])} queue items','source_is_action_inference':aid in {'saat_calar_12_00_001','kalem_kutusu_acik_001','etek_kirmizi_001'},'semantic_review':semantic+' Seçilen tam mevcut ders alanı okundu. Mevcut R/K kartlar ve temel yardımcı nesne dosyaları korunur. Üretim sonrası her PNG için ayrı teknik ve üç görünümde sanatsal QA gerekir; poz hizası/animasyon henüz doğrulanmış değildir. Tüm müfredat ayrıştırması bitmedi.'}
    if reference:item['pose_reference']=reference
    new.append(item)
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blobs_sha_verified':{k:v[1] for k,v in sources.items()},'base_references':[x['pose_reference'] for x in new if 'pose_reference' in x],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'records':len(h),'pngs':len(canonical)}))
