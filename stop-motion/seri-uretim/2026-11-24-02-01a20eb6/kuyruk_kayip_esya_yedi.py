"""Reconcile seven source-specific object states and colors; preserve original accepted variants."""
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
specs=json.loads('[["matara_yesil_gazi_001", "Tek Gazi yazılı yeşil suluk", "yardimci-nesneler/kamp/matara", "7-9-fidan", 16, "D6", "Sonra öğretmen yeşil bir suluk çıkardı.", ["matara_yesil", "suluk_yesil", "yesil_suluk", "yesil_matara", "gazi_suluk", "gazi_matara"], "matara_kapali_001", "Mevcut sarı-turuncu kıvrımlı mataranın mavi vidalı kapağı, iki lacivert kavrama çizgisi ve sağ alt kıvrımı görüldü. Kaynak açıkça yeşil suluk ve üzerinde Gazi adı diyor. Yeşil gövde ile üzerinde GAZİ yazılı küçük etiket üretilir; ad kurmaca ders karakterine aittir."], ["tava_yumurtali_001", "Tek içinde yumurta pişen tava", "yardimci-nesneler/mutfak/tava", "4-6-filiz", 10, "D6", "Annesi tavada yumurta pişiriyor.", ["tava_yumurtali", "yumurtali_tava", "tavada_yumurta", "yumurta_pismis_tava", "sahanda_yumurta"], "tava_bos_001", "Mevcut kırmızı dış gövdeli, koyu gri içli ve sağda turuncu saplı tava r03 ham çizimi görüldü. İçinde tek pişmiş yumurta yüzey çizimi olarak beyazı ve sarısıyla gösterilir; kaynak pişirme biçimini ayrıntılandırmadığı için sahanda yorum tasarım seçimidir. Menemen tavası aynı durum değildir."], ["boya_kalemi_kirmizi_ucu_kirik_001", "Tek ucu kırık kırmızı boya kalemi", "yardimci-nesneler/okul/boya-kalemi", "7-9-orman", 9, "D6", "Ela kalemleri geri koydu ama kırmızının ucu kırıktı.", ["boya_kalemi_kirmizi_ucu_kirik", "boya_kalemi_kirik", "kirmizi_kalem_kirik", "kalem_kirmizi_kirik", "renkli_kalem_kirik"], "boya_kalemi_tek_001", "Mevcut kırmızı ahşap boya kalemi görüldü: sol altta sivri kırmızı uç, sağ üst arka kâğıt kıvrımı, kırmızı iki yüzey. Kaynak gövde kırığı değil kırmızı ucun kırılmasıdır. Yalnız renkli uç küt ve düzensiz yapılır; ayrı kopmuş parça eklenmez. Mevcut kırık grafit kalem eşdeğer değildir."], ["boya_kalemi_yesil_001", "Tek yeşil boya kalemi", "yardimci-nesneler/okul/boya-kalemi", "4-6-fidan", 15, "D1", "resim: yeşil kalem", ["boya_kalemi_yesil", "yesil_boya_kalemi", "kalem_yesil", "yesil_kalem"], "boya_kalemi_tek_001", "Renk tercihleri sorusunda yeşil kalem açık doğru seçenektir. Mevcut kırmızı boya kaleminin aynı ahşap yapısı ve kâğıt biçimi yeşil gövde/yeşil uçla kullanılır. R/K keçe kartlar değiştirilmez."], ["boya_kalemi_sari_001", "Tek sarı boya kalemi", "yardimci-nesneler/okul/boya-kalemi", "4-6-fidan", 15, "D1", "resim: sarı kalem", ["boya_kalemi_sari", "sari_boya_kalemi", "kalem_sari", "sari_kalem"], "boya_kalemi_tek_001", "Aynı renk tercihleri sorusundaki sarı kalem ayrı bir seçenektir. Mevcut kırmızı kalem yeniden üretilmez; sarı gövde ve sarı renkli uç, açık ahşap koniden ayırt edilir."], ["pasta_yarim_001", "Tek yarım yuvarlak pasta", "yardimci-nesneler/yiyecek/pasta", "4-6-agac", 16, "D3", "resim: pastayı ikiye bölen Ela", ["pasta_yarim", "yarim_pasta", "pasta_ikiye_bolunmus"], "pasta_butun_001", "Mevcut pembe yan gövdeli, beyaz kremalı ve kırmızı/pembe şeker çizgili bütün pasta r03 görüldü. Bölüşme eyleminden türetilen tek yarım pasta: üst planı yarım daire, önünde tek düz çap kesiti. İki ayrı yarı aynı PNGye konulmaz; mevcut çikolatalı üçgen dilim veya devrilmiş pasta eşdeğer değildir. Kesir alanı sayısal ölçüldü iddiası yok."], ["tuy_sari_001", "Tek sarı kuş tüyü", "yardimci-nesneler/doga/tuy", "7-9-cinar", 3, "D6", "küçük, sarı bir tüy!", ["tuy_sari", "sari_tuy", "kanarya_tuyu"], "tuy_tek_001", "Mevcut kahverengi-mavi çizgili tüy r01 ham görseli görüldü. Sarı kanarya öyküsündeki sarı ipucu için tüyün geniş alanları sarıya dönüştürülür, tek sarı sap/çubuk, düzensiz lacivert damarlar ve beyaz makas payı korunur. Türün anatomik bilimsel tanımlaması veya kesin ölçek iddiası yok."]]')
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/kayip_esya_yedi_kaniti.json'
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
