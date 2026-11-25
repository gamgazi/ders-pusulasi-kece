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
specs=json.loads("[[\"oyun_tahtasi_basla_yazili_001\",\"BAŞLA yazılı oyun tahtası\",\"yardimci-nesneler/oyun/oyun-tahtasi\",\"4-6-cinar\",8,\"D4\",\"resim: «BAŞLA» yazan ilk kare\",[\"oyun_tahtasi_basla\",\"basla_yazili\"],\"oyun_tahtasi_001\",\"Mevcut kıvrımlı yol oyun tahtasının yeşil başlangıç hücresine BAŞLA yazılır. Yol ve bitiş bayrağı aynı yüzeyde; piyon/zar eklenmez. Sayılı hareket sahnesi veya animasyon hizası doğrulaması değildir.\"],[\"fener_el_yanan_001\",\"Yanan el feneri\",\"yardimci-nesneler/esya/fener\",\"4-6-filiz\",17,\"D1\",\"resim: karanlıkta ışık veren bir fener\",[\"fener_el_yanan\",\"fener_isikli\"],\"fener_el_001\",\"Mavi saplı sarı başlıklı mevcut el fenerinin merceği sarı ve krem ışıklı yüzey olarak çizilir; düğme açık konumda. Ayrı ışın, karanlık fon veya ışık konisi eklenmez. Kaynağın fener nesnesinin açık durumu sağlanır; karanlık sahne arka planı ayrı tutulur.\"],[\"kartpostal_manzarali_on_001\",\"Manzaralı kartpostal ön yüzü\",\"yardimci-nesneler/iletisim/kartpostal\",\"4-6-cinar\",16,\"D4\",\"resim: önünde manzara olan kartpostal\",[\"kartpostal_manzarali\",\"kartpostal_on\"],\"kartpostal_tek_001\",\"Mevcut kartpostalın ön yüzü: aynı yatay kâğıdın içine çizili dağ, göl ve güneş manzarası. Resim kâğıt sınırları içinde; ayrı doğal nesneler veya tam ekran arka plan değil. Arka yüzdeki yazı/adres çizgileri bulunmaz.\"],[\"roket_kalkis_001\",\"Kalkış yapan roket\",\"yardimci-nesneler/uzay/roket\",\"4-6-orman\",14,\"D4\",\"resim: ateş ve dumanla yükselen roket\",[\"roket_kalkis\",\"roket_ucan\"],\"roket_duran_001\",\"Mevcut kırmızı burun/turkuaz gövdeli roketin egzozuna bağlı kısa turuncu-sarı alev ve tek gri duman kuyruğu; hepsi tek bağlı kâğıt siluetinin parçaları. Ayrık alev/duman, yer veya kişi yok. Kaynak kalkış durumu; fiziksel motor şeması değildir.\"],[\"posta_cantasi_mektuplu_001\",\"Mektuplu posta çantası\",\"yardimci-nesneler/iletisim/posta-cantasi\",\"4-6-cinar\",16,\"D1\",\"resim: posta çantasından çıkan mektuplar\",[\"posta_cantasi\",\"postaci_cantasi\"],null,\"Tek açık mavi posta çantasının ağzında kısmen görünen iki krem zarf biçimi. Zarflar bölmeye bağlı/örtüşen iç içerik, ayrı kâğıt nesneler değil. Tek çanta silueti; posta işareti olarak yüzeye çizili küçük zarf ikonu. Kişi/adres/metin yok.\"],[\"cam_kirik_parca_001\",\"Tek kırık cam parçası\",\"yardimci-nesneler/malzeme/cam-parcasi\",\"4-6-fidan\",19,\"D4\",\"resim: yerde kırık cam parçaları\",[\"cam_kirik_parca\",\"cam_parcasi\"],null,\"Çoğul kaynak için yeniden kullanılabilir tek düzensiz köşeli cam kırığı. Açık mavi opak kâğıt üzerinde lacivert kenar ve açık yansıma çizgisi; gerçek kesici malzeme değil çizim. Bir PNG’de tek parça; yer/çoklu parça düzeni yok, çoğul sahne daha sonra kompozisyonda kurulur.\"],[\"pati_izi_camurlu_001\",\"Tek çamurlu pati izi\",\"yardimci-nesneler/iz/pati\",\"7-9-agac\",1,\"D2\",\"resim: yerde çamurlu pati izleri\",[\"pati_izi\",\"camurlu_pati\"],null,\"Tek stilize çamurlu pati izi: bir büyük taban ve dört küçük parmak lekesi kahverengi mürekkeple aynı bağlı beyaz pati biçimli kâğıt üzerine çizilir. Ayrı lekeler/zemin/hayvan yok; çoğul izler aynı varlıkla daha sonra yerleştirilir.\"],[\"kok_bitki_tek_001\",\"Tek dallanan bitki kökü\",\"yardimci-nesneler/bahce/kok\",\"7-9-fidan\",6,\"D2\",\"resim: toprağın altındaki ince parçalar\",[\"kok_bitki\",\"bitki_koku\",\"kok_tek\"],null,\"Üstte kısa gövde boğazına bağlı açık kahverengi ana kök ve kalın yan kökler, tek bağlı siluet. Filiz_koklu_001 bütün genç bitkiyi içerir; burada hedef kök organının bağımsız görünümüdür. Yaprak, toprak, saksı yok; biyolojik tür/ölçek iddiası yok.\"],[\"poster_kutuplar_001\",\"Kutuplar resimli poster\",\"yardimci-nesneler/kagit/poster\",\"7-9-fidan\",20,\"D3\",\"resim: duvarda büyük resimli kâğıt\",[\"poster_kutuplar\",\"kutuplar_afisi\"],\"afis_tek_001\",\"Tek dikey kâğıt posterin yüzeyinde buz üstünde kutup ayısı, mavi deniz ve açık mavi gökyüzü çizimi. Kutuplar bağlamı tam ders okuma metninden gelir. Tüm manzara posterin sınırları içindedir; duvar/oda ayrı sahne olarak eklenmez. Başlık KUTUPLAR okunarak QA edilir. Mevcut afis_tek_001 genel çevre konusu taşır; yeni konu aynı afiş referansına bağlı bir yüzey varyantıdır.\"]]")
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/uzun_tarif_dokuz_devam_kaniti.json'
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
