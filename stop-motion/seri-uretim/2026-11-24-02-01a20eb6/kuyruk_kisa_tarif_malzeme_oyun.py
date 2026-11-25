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
specs=json.loads("[[\"ayak_izi_tek_001\",\"Tek ayak izi simgesi\",\"yardimci-nesneler/semboller/ayak-izi\",\"4-6-agac\",5,\"D4\",\"resim: bir ayak izi\",[\"ayak_izi_tek\",\"ayakkabi_izi\"],null,\"Tek ayakkabı taban izi simgesi, üstten görünüş: geniş yuvarlak ön uç, daralan iç kavis ve yuvarlak topuk, tek bağlı kâğıt silueti. Koyu lacivert iz içinde birkaç kısa açık kâğıt oluk çizgisi; topuk ayrı parça olmaz. Ayakkabının üstü/bağcık/insan ayağı yok. İki/beş iz seçeneği bu tek varlık sahnede ayrı örneklenerek karşılanabilir; tek PNG içine çoklu iz konmaz.\"],[\"dal_kuru_tek_001\",\"Tek kuru dal\",\"yardimci-nesneler/bahce/dal\",\"4-6-cinar\",7,\"D7\",\"resim: kuru dal\",[\"dal_kuru\",\"kuru_dal\"],null,\"Tek yapraksız kahverengi kuru dal, bir ana ince eğimli gövde ve ona bağlı üç kısa yan dal ucu. Odun kütüğü/tahta parçası/bütün ağaç değildir. Yaprak/çiçek/kar/kök/zemin yok; dar beyaz makas payı ve dallar arasında gerçek alfa. İleride kar/çiçek pozları için bu temel korunur.\"],[\"kavanoz_cam_bos_001\",\"Boş cam kavanoz\",\"yardimci-nesneler/mutfak/kavanoz\",\"4-6-cinar\",12,\"D2\",\"resim: cam kavanoz\",[\"kavanoz_cam_bos\",\"cam_kavanoz_bos\",\"kavanoz_bos\"],null,\"Tek boş kapaksız geniş ağızlı kavanoz. Kısa vidalı boyun, geniş silindirik açık mavi gövde, üstte oval açık ağız ve altta düz yuvarlak taban; camın kendisi opak kesilmiş kâğıt çizimi olarak temsil edilir. Kapak ayrı nesne olmasın diye gösterilmez. Etiket/içerik/bal/reçel yok; mevcut dar boyunlu cam şişeden ayrı kimlik.\"],[\"zimpara_kagidi_tek_001\",\"Tek zımpara kâğıdı\",\"yardimci-nesneler/malzemeler/zimpara\",\"4-6-cinar\",17,\"D4\",\"resim: zımpara kâğıdı\",[\"zimpara\"],null,\"Tek kahverengi dikdörtgen zımpara kâğıdı yaprağı; yüzeyinin pürüzünü temsil eden düzensiz koyu kalem noktaları ve yoğun kahverengi/oker mürekkep vuruşları. Malzeme gerçek zımpara fotoğrafı/pastel dokusu değil kesilmiş beyaz kâğıt üzerinde keçeli kalem çizimi. Bir köşe hafif kıvrık; blok/rulo/ikinci yaprak/alet yok.\"],[\"rakam_yedi_tek_001\",\"Tek yedi rakamı\",\"yardimci-nesneler/semboller/rakam\",\"4-6-cinar\",15,\"D7\",\"resim: yedi rakamı\",[\"rakam_yedi\",\"yedi_rakami\"],null,\"Tek büyük 7 rakamı biçiminde mavi kesilmiş kâğıt: yatay üst çizgi ve sağ üstten sol alta inen eğik gövde; okunur tek yedi, kutu/etiket/diğer rakam yok. Tekerleme/uyak seçeneği için somut simge. Mevcut sayı R/K kartları yeniden üretilmez; yardımcı sahne parçasıdır.\"],[\"oyun_kutusu_kapali_001\",\"Kapalı masa oyunu kutusu\",\"yardimci-nesneler/oyuncaklar/oyun-kutusu\",\"4-6-cinar\",8,\"D4\",\"resim: oyunun kutusu\",[\"oyun_kutusu\",\"masa_oyunu_kutusu\"],null,\"Tek kapalı sığ masa oyunu kutusu, turuncu kapak/mavi alt gövde, kapak üstünde OYUN sözcüğü ve bir basılı piyon simgesi. Basılı simge aynı kutunun çizimi, ayrı nesne değil. Oyun tahtası/piyon/zar/oyuncak saklama kutusu korunur; açık kutu/dağılmış parçalar/marka yok. Kaynakta yanıltıcı seçenek olduğu için ders doğru cevabı olarak sunulmaz.\"]]")
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/kisa_tarif_malzeme_oyun_kaniti.json'
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
