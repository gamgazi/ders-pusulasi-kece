"""Reconcile seven source-backed transport, invention and household states."""
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
specs=json.loads('[["ucus_bilgi_panosu_rotar_2_saat_001", "Tek uçuş ekranında iki saat rötar", "yardimci-nesneler/ulasim/ucus-bilgisi", "16-17-filiz", 11, "D9", "Sis ____ uçağımız iki saat gecikti.", ["ucus_bilgi_panosu_rotar_2", "ucus_rotar_2", "rotar_2_saat", "ucak_gecikme_2"], "ucus_bilgi_panosu_rotar_3_saat_001", "Kaynak iki saat ve sis der; D5 üç saat örneği farklıdır. Ekran taşıyıcısı sanatsal çıkarım; güncel sefer değildir. Üç saatlik temel dosya korunur."], ["yaya_isigi_kirmizi_001", "Tek kırmızı yaya sinyali", "yardimci-nesneler/ulasim/trafik", "4-6-fidan", 19, "D5", "Kırmızı ışıkta dur!", ["yaya_isigi_kirmizi", "kirmizi_yaya_isigi", "yaya_kirmizi", "yaya_sinyali_kirmizi"], "yaya_isigi_yesil_001", "Temel mor gövdeli iki gözlü sinyal görüldü. Üstte duran insan kırmızı, altta yürüyen insan sönük gri olur; yeşil yanmaz. Durma/karşıya geçme sahnesinin yalnız aksesuarıdır; çocuk sahnesi tamamlanmış sayılmaz."], ["sirt_cantasi_tekerlekli_001", "Tek tekerlekli okul çantası", "yardimci-nesneler/esya/canta", "7-9-orman", 7, "D6", "tekerlekli bir okul çantası", ["sirt_cantasi_tekerlekli", "tekerlekli_canta", "okul_cantasi_tekerlekli", "tekerlekli_okul_cantasi"], "sirt_cantasi_kapali_001", "Kaynak iki tekerlek eklenmiş okul çantası ve sırta takmayı açıkça anlatır. Mor gövde, turuncu cep, mavi askılar görüldü. Tekerlekler gövdeye bağlı çizilir; yeni çizimde bütün iç kesim boşluklarına beyaz kâğıt payı zorunludur. Bavul yerine okul çantası kimliği korunur."], ["robot_gunes_panelli_001", "Üstünde güneş paneli olan tek robot", "yardimci-nesneler/oyuncak/robot", "7-9-orman", 7, "D3", "Robotun üstünde bir güneş paneli var", ["robot_gunes_panelli", "gunes_panelli_robot", "robot_gunes_enerjili", "gunesle_calisan_robot"], "robot_tek_001", "Kaynak paneli robotun üstünde tarif eder. Mavi baş, turuncu gövde, gri eklemler ve mavi eller/ayaklı temel robot görüldü; tepedeki anten yerine bağlı küçük panel eklenir. İşlev/enerji verimi test edilmiş iddia edilmez."], ["telefon_goruntulu_arama_donmus_001", "Ekranı donmuş tek görüntülü arama telefonu", "yardimci-nesneler/esya/telefon", "7-9-fidan", 9, "D6", "Sonra ekran dondu.", ["telefon_goruntulu_arama_donmus", "telefon_ekran_donmus", "donmus_goruntulu_arama", "ekran_dondu_telefon"], "telefon_goruntulu_arama_001", "Kaynak görüntülü dede araması sırasında ekran donmasını açıkça anlatır. Temel genel kullanıcı simgesi görüldü; kanonik dede resmi üretilmez. EKRAN DONDU yazısı arızanın açık göstergesidir; yalnız durağan resim donmayı ispatlamaz. Karakter sahnesi tamamlanmış sayılmaz."], ["cop_kovasi_dolu_acik_001", "Tek dolu açık çöp kovası", "yardimci-nesneler/esya/cop", "16-17-filiz", 9, "D5", "çöpler birikmişti", ["cop_kovasi_dolu", "cop_kutusu_dolu", "dolu_cop_kovasi", "tasan_cop"], "cop_kovasi_kapali_001", "Kaynak çöplerin birikmesini anlatır. Yeşil gövde, gri kapak/pedallı temel kova görüldü. Dolu kova sahne yorumudur; çöp parçaları aynı kova kesimi içinde kalır, zemine ayrı çöpler eklenmez."], ["evye_bulasik_dolu_001", "Tek bulaşık dolu mutfak evyesi", "yardimci-nesneler/mutfak/evye", "16-17-filiz", 9, "D5", "lavabo bulaşık doluydu", ["evye", "lavabo", "bulasik_lavabo", "bulasik_dolu_evye"], "", "Kaynak bulaşık dolu lavabo der; mutfak evyesi olarak yorumlandı. Tek evye ünitesi üzerinde bağlı musluk ve haznede kirli tabak/kâse çizilir; ayrı mutfak/tezgâh sahnesi veya su damlası üretilmez."]]')
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/ulasim_ev_yedi_kaniti.json'
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
