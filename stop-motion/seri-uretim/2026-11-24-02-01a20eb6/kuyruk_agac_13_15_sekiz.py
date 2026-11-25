"""Reconcile eight specific states after full Agac 13-15 reading and reference inspection."""
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
specs=json.loads('[["bisiklet_kirmizi_001", "Tek kırmızı bisiklet", "yardimci-nesneler/oyun/bisiklet", "13-15-agac", 15, "D2", "Sonunda kırmızı bisikleti almaya karar verdim.", ["bisiklet_kirmizi", "kirmizi_bisiklet"], "bisiklet_tek_001", "Mevcut temel bisiklet turuncu gövdeli olarak gerçekten görüldü; yalnız gövde kırmızı olur. İki teker/sap/sele/pedal ve beyaz iç makas payları korunur. R/K bisiklet kartları korunur, animasyon hizası ayrı."], ["toprak_nem_sensoru_001", "Tek toprak nem sensörü", "yardimci-nesneler/bilim/nem-sensoru", "13-15-agac", 9, "D5", "toprağın nemini ölçen küçük bir sensör", ["toprak_nem_sensoru", "nem_sensoru", "nem_olcer"], null, "İki bağlı geniş prob uçlu küçük tek sensörün stilize kâğıt modeli. Devre/kablo/ekran/toprak yok, ölçüm değeri yok; belirli ürün veya çalışan mühendislik tasarımı iddiası değildir."], ["tuzluk_devrilmis_001", "Tek devrilmiş tuzluk", "yardimci-nesneler/mutfak/tuzluk", "13-15-agac", 10, "D5", "Masada tuzluk devrildi", ["tuzluk", "tuz_sisesi", "tuz_kabi"], null, "Kapalı kapaklı tek tuzluk yana yatmış durumda; dökülmüş tuz parçacıkları veya ayrı masa yok. Mevcut kapalı tuz paketi farklı nesnedir ve korunur."], ["sutlac_kase_001", "Tek kâsede sütlaç", "yardimci-nesneler/yiyecek/sutlac", "13-15-agac", 10, "D5", "mantı, dolma ve sütlaç yapmıştı", ["sutlac", "sutlu_pirinc_tatlisi", "rice_pudding"], null, "Sütlaçla dolu tek kâse, krem yüzeyde birkaç belirgin pirinç çizgisi ve hafif tarçın mürekkep lekeleri; kaşık/tepsi/ikinci kâse yok. Servis rengi ve tarçın sanat seçimi, tarif veya kaynak ayrıntısı diye sunulmaz."], ["on_yazi_ornek_001", "Tek örnek ön yazı", "yardimci-nesneler/belgeler/on-yazi", "13-15-agac", 6, "D1", "ön yazı", ["on_yazi", "onyazi", "cover_letter"], null, "Tek kâğıtta ÖN YAZI / ÖRNEK; Sayın Yetkili, / Bu işi istiyorum, çünkü / boş satır / Saygılarımla, / Ad: boş. Kaynağın başvuru dili için eğitim örneği; gerçek başvuru/kurum/kişisel bilgi yok. Özgeçmiş ayrı mevcut nesnedir."], ["bilim_fuari_toplanti_notu_001", "Tek bilim fuarı toplantı notu", "yardimci-nesneler/belgeler/toplanti-notu", "13-15-agac", 9, "D5", "TOPLANTI NOTU – Bilim Fuarı Ekibi", ["bilim_fuari_toplanti_notu", "toplanti_notu", "toplanti_tutanagi"], null, "Tek kâğıtta TOPLANTI NOTU / Bilim Fuarı Ekibi / GÜNDEM / 1 Projenin ilerlemesi / 2 Görev dağılımı / 3 Son tarih ve yedek plan. Kesilmiş görev dağılımı uydurulmaz; yıl belirtilmeyen tarih takvime bağlanmaz."], ["sutun_grafik_ekran_suresi_001", "Tek ekran süresi sütun grafiği", "yardimci-nesneler/belgeler/sutun-grafik", "13-15-agac", 12, "D5", "1 saatten az: 8 öğrenci (yüzde 10)", ["sutun_grafik_ekran_suresi", "ekran_suresi_grafigi", "ekran_suresi_anketi"], "sutun_grafik_sayfasi_001", "80öğrencilik kurmaca ankette8/20/36/16;dört sütun ortak0taban ve bu oranlarda.1saatten az/1–2saat/2–4saat/4saatten fazla. Bar uzunlukları ayrıca ölçülecek.36/80=%45mutlak çoğunluk değildir; öyle yazılmayacak."], ["imza_kampanyasi_formu_ornek_001", "Tek boş örnek imza kampanyası formu", "yardimci-nesneler/belgeler/imza-formu", "13-15-agac", 16, "D2", "Kampanyamıza ___ olmak için imza atın.", ["imza_kampanyasi_formu", "imza_formu", "imza_listesi", "imza_cizelgesi"], null, "Tek kâğıtta İMZA KAMPANYASI / ÖRNEK; Konu: boş; Ad / İmza sütunlarında üç boş satır. Gerçek imza/kişi bilgisi veya canlı kampanya yok. K0716imza toplamak hareket kartı korunur; form ayrı yardımcı nesnedir."]]')
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/agac_13_15_sekiz_kaniti.json'
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
