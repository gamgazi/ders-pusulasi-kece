"""Reconcile seven curriculum needs against canonical records, files and live queue."""
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
specs=json.loads("[[\"oy_sandigi_kapali_001\",\"Tek kapalı oy sandığı\",\"yardimci-nesneler/cevre/oy-sandigi\",\"16-17-agac\",8,\"D1\",\"oy kullanmak\",[\"oy_sandigi\",\"secim_sandigi\"],null,\"Oy kullanma eylemi için tek kapalı kutu, üstte tek oy atma yarığı ve OY yazısı. Nesne kaynak eyleminden çıkarılan nötr sınıf sahne desteğidir; parti, aday, gerçek seçim prosedürü, ülke veya yaş hakkı iddiası yok. Yardım/öneri kutusu farklı işlevdedir; ayrı zarf eklenmez.\"],[\"anket_formu_ornek_001\",\"Tek boş örnek anket formu\",\"yardimci-nesneler/kirtasiye/anket-formu\",\"16-17-agac\",11,\"D3\",\"anket\",[\"anket_formu\",\"anket_kagidi\"],null,\"ANKET / ÖRNEK başlıklı tek kâğıt, boş Soru alanı ve üç boş yanıt kutucuğu. Kaynaktaki yüzde45/60 verisi ayrı değerlendirme cümlesidir; formda uydurma veri/sonuç üretilmez. Soyut veri kavramı değil somut anket kâğıdı olarak sahne desteği.\"],[\"pano_okul_bos_001\",\"Tek boş okul duyuru panosu\",\"yardimci-nesneler/okul/duyuru-panosu\",\"16-17-agac\",12,\"D6\",\"Bu biyografiyi okul panosuna koyacağım.\",[\"duyuru_panosu\",\"pano_okul\"],null,\"Tek boş dikdörtgen okul panosu, ince ahşap renkli çevre ve boş mavi iç yüzey. Üzerine biyografi/afiş sonradan ayrı katman olarak konabilir; hazır sayfa, kolaj, grid, resim seti, ayrı raptiye veya duvar yok. Mozaik panel, tuval ve oyun tahtası farklı nesnelerdir.\"],[\"kamera_guvenlik_001\",\"Tek güvenlik kamerası\",\"yardimci-nesneler/teknoloji/guvenlik-kamerasi\",\"16-17-cinar\",1,\"D2\",\"kamera\",[\"guvenlik_kamerasi\",\"kamera_guvenlik\"],null,\"Gözetim/gizlilik tartışması bağlamında tek duvar bağlantı ayağı gövdesine bağlı sabit güvenlik kamerası. Ön dairesel mercek, kısa üst siperlik, ayarlı bağlantı kolu ve montaj plakası bir nesne. El kamerasından farklı; gerçek izleme kaydı, kişi, yüz tanıma çıktısı veya kablo yok.\"],[\"basvuru_formu_ornek_001\",\"Tek boş örnek başvuru formu\",\"yardimci-nesneler/kirtasiye/basvuru-formu\",\"16-17-cinar\",2,\"D4\",\"başvuru formu\",[\"basvuru_formu\"],null,\"BAŞVURU / FORMU / ÖRNEK başlıklı tek kâğıt, boş Ad ve Tarih alanları. Kayıt yenileme talebi bağlamında genel sahne formu; gerçek kişi, kurum, imza, başvuru teslimi veya hukuki geçerlik yok. Dilekçe ve özgeçmiş farklı belge türüdür.\"],[\"sozluk_kapali_001\",\"Tek kapalı sözlük\",\"yardimci-nesneler/kirtasiye/sozluk\",\"16-17-cinar\",7,\"D6\",\"Anlamadığım terime sözlükten baktım.\",[\"sozluk\"],null,\"Tek kalın kapalı sözlük; SÖZLÜK başlığı, sade harf motifi, görünen sayfa bloğu. Ansiklopedi, roman ve masal kitabından işlevi farklı; gerçek yayınevi veya tanımı olmayan uydurma sözlük maddesi yok.\"],[\"diploma_ornek_001\",\"Tek boş örnek diploma\",\"yardimci-nesneler/kirtasiye/diploma\",\"16-17-orman\",8,\"D4\",\"diploma\",[\"diploma\"],null,\"DİPLOMA / ÖRNEK başlıklı tek yatay kâğıt; boş Ad ve Tarih alanları, çizilmiş sade kenar süsü. Kurum, gerçek mezun, imza, mühür, seri numarası veya akreditasyon yok; eğitimde belge türünü anlatan açıkça örnek sahne aksesuarı.\"]]")
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/agac_cinar_orman_16_17_kuyruk_kaniti.json'
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
    item={'id':aid,'title':title,'category':cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':rel,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+pointer,'match':'exact_json_leaf' if value==term else 'substring_of_exact_json_leaf','leaf_sha256':hashlib.sha256(value.encode()).hexdigest()}],'felt_cards_preserved':cardids,'role':'missing pose of existing paper helper' if baseid else 'independent missing paper helper','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} records, {len(canonical)} canonical PNGs, {len(q["items"])} queue items','source_is_action_inference':aid in {'oy_sandigi_kapali_001'},'semantic_review':semantic+' Seçilen tam mevcut ders alanı okundu. Mevcut R/K kartlar ve temel yardımcı nesne dosyaları korunur. Üretim sonrası her PNG için ayrı teknik ve üç görünümde sanatsal QA gerekir; poz hizası/animasyon henüz doğrulanmış değildir. Tüm müfredat ayrıştırması bitmedi.'}
    if reference:item['pose_reference']=reference
    new.append(item)
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blobs_sha_verified':{k:v[1] for k,v in sources.items()},'base_references':[x['pose_reference'] for x in new if 'pose_reference' in x],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'records':len(h),'pngs':len(canonical)}))
