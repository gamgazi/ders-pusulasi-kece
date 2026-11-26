"""Reconcile six food, clothing and torn drawing states against existing accepted files."""
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
specs=json.loads('[["limon_sikilmis_yarim_001", "Tek sıkılmış yarım limon", "yardimci-nesneler/yiyecek/limon", "7-9-fidan", 6, "D4", "Limonları sıkıp suya ekleriz.", ["limon_sikilmis", "sikilmis_limon", "limon_yarim_sikilmis"], "limon_yarim_001", "Mevcut yarım limonun sarı bölümlü kesik yüzeyi, kavisli kabuğu ve sağ alt kıvrımı görüldü. Sıkılmış durumda posa çökmüş, bölmeler buruşuk ve kabuk basılmış olur. Ayrı damla, el veya sıkacak eklenmez."], ["surahi_limonatali_001", "Tek limonata dolu sürahi", "yardimci-nesneler/mutfak/surahi", "7-9-fidan", 6, "D6", "Sonra limonları sıkıp suyu bir sürahiye koydular.", ["surahi_limonatali", "limonata_surahisi", "surahi_limonata", "surahi_limonlu"], "surahi_bos_001", "Mevcut turkuaz opak gövdeli, sağ kulplu, sol ağızlı boş sürahi görüldü. Limonata üst açıklıkta sarı içecek yüzeyiyle gösterilir; gövde keyfi biçimde şeffaflaştırılmaz. Öykünün tamamlanmış limonatasını ayırt etmek için gövde üzerinde tek küçük limon çizimi yüzey süsü olarak kullanılabilir. Ayrı limon veya buz nesnesi yok."], ["pilav_yanmis_tabak_001", "Tek tabakta yanmış pilav", "yardimci-nesneler/yiyecek/pilav", "7-9-orman", 18, "D6", "kırk kişilik pilavı yaktım.", ["pilav_yanmis", "yanmis_pilav", "pilav_yanik"], "pilav_tabagi_001", "Mevcut mavi tabakta krem renk pirinç taneli pilav r03 ham çizimi görüldü. Aynı tabağın pirincinde belirgin koyu kahverengi ve siyah yanık bölgeler oluşturulur. Tek servis görseli öyküdeki yanmış yemek durumunu temsil eder; kırk kişilik miktar gösterdiği iddia edilmez."], ["bere_mavi_001", "Tek mavi bere", "yardimci-nesneler/giyim/bere", "7-9-fidan", 16, "D6", "Kutuda mavi bir bere de vardı.", ["bere_mavi", "mavi_bere"], "bere_tek_001", "Mevcut bere pembe ana gövde, turuncu ponpon, turkuaz katlı bant ve sağ alt kâğıt kıvrımına sahip. Kaynakta açıkça istenen mavi bere için ana gövde maviye dönüştürülür; nesne ve mevcut temel dosya korunur."], ["onluk_mutfak_beyaz_001", "Tek beyaz mutfak önlüğü", "yardimci-nesneler/giyim/onluk", "7-9-fidan", 12, "D6", "Bir lokantanın mutfağında yemek pişirir ve beyaz bir önlük giyer.", ["onluk_mutfak_beyaz", "beyaz_mutfak_onlugu", "asci_onlugu_beyaz", "beyaz_asci_onlugu"], "onluk_mutfak_001", "Mevcut turuncu mutfak önlüğünün mavi boyun askısı, yan bağları ve cebi görüldü. Aşçı için gövde ve cep beyaz yapılır; dar mavi askı ve bağlar korunur. Laboratuvar önlüğü veya okul önlüğüyle aynı nesne değildir."], ["cocuk_resmi_mavi_ev_yirtik_001", "Tek yırtılmış mavi ev resimli kâğıt", "yardimci-nesneler/egitim/cocuk-resmi", "4-6-cinar", 19, "D4", "Özür dilerim, resmini yırttım.", ["cocuk_resmi_mavi_ev_yirtik", "resim_mavi_ev_yirtik", "yirtilmis_cocuk_resmi", "cocuk_resmi_yirtik"], "cocuk_resmi_mavi_ev_gunes_001", "Yeni kabul edilen mavi ev ve güneş çizimli tek kâğıt aynı çizimle yırtık duruma getirilir. Kaynak resmin konusunu belirtmediği için mevcut çizim yeniden kullanım seçimi kaydedilir; belirli çocuğa ait olduğu iddia edilmez. Üst kenardan kâğıdın yaklaşık üçte ikisine inen gerçek alfa boşluğu, altta bağlantı ve lifli beyaz yırtık kenarı gerekir."]]')
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/mutfak_giyim_alti_kaniti.json'
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
