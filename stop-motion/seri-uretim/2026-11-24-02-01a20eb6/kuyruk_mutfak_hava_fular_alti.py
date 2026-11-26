"""Reconcile six food, scarf and weather variants; preserve base and alternate-temperature assets."""
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
specs=json.loads('[["sandvic_sebzeli_001", "Tek sebzeli sandviç", "yardimci-nesneler/yiyecek/sandvic", "16-17-tohum", 5, "D5", "sebzeli sandviç", ["sandvic_sebzeli", "sebzeli_sandvic", "sandvic_vegan"], "sandvic_peynirli_001", "Mevcut kaynak peynirli sandviç gerçekten görüldü: kahverengi oval ekmek, tek sarı peynir tabakası ve sol alt kıvrım. Kaynak vegan seçenek bağlamında sebzeli sandviç der; sarı peynir korunarak eşleştirilemez. Dolgu marul, domates ve salatalıkla değiştirilir. Görsel bir tarif/alerjen sertifikası sayılmaz."], ["meyve_salatasi_kase_001", "Tek kâsede meyve salatası", "yardimci-nesneler/yiyecek/meyve-salatasi", "16-17-tohum", 5, "D5", "meyve salata", ["meyve_salatasi", "meyve_salata", "salata_meyve"], "salata_kasesi_001", "Kaynak oku alanı meyve salata sözcüklerinde kesiliyor; eksik cümlenin devamı uydurulmaz. Görünen ifade meyve salatası aksesuarını destekler. Mevcut turuncu kâsede marul/domates/salatalık resmi gerçekten görüldü, bu sebze salatası meyve salatası yerine atanmaz. Meyve parçaları kâsenin dolgu çizimleridir, bağımsız assetler değil."], ["suzgec_makarna_dolu_001", "Tek süzgeçte süzülmüş makarna", "yardimci-nesneler/mutfak/suzgec", "16-17-kok", 3, "D4", "Makarnayı süzün.", ["suzgec_makarna", "makarna_suzgec", "suzulmus_makarna"], "suzgec_mutfak_001", "Mevcut mavi süzgeç, turuncu ağız/kulplar, gri boş iç yüzey ve sağ üst kıvrım gerçekten görüldü. Süzme eyleminin sonuç durumu sarı makarnayla dolu süzgeçtir. Su döken el, ayrı damla ve tencere eklenmez. Kulp boşlukları gerçek alfa ve beyaz iç kesim payıyla korunmalı."], ["fular_boyun_001", "Tek düğümlü boyun fuları", "yardimci-nesneler/giysi/fular", "7-9-cinar", 18, "D6", "güzel bir fular almak istiyor", ["fular_boyun", "fular_tek", "boyun_fulari"], "", "Kaynak annesine alınacak fuları açıkça adlandırır. Mevcut yeşil kış atkısı ile işlev/biçim ayrımı için küçük düğümlü, iki sivri uçlu boyun fuları çizilir. Kumaş fotoğrafı veya örgü doku değil, beyaz kesilmiş kâğıda keçeli kalem çizimi. İnsan boynu/baş yok."], ["hava_tahmini_hafta_sonu_24_001", "Tek kâğıtta hafta sonu yirmi dört derece tahmini", "yardimci-nesneler/belgeler/hava-tahmini", "16-17-filiz", 11, "D8", "Cumartesi sağanak olacakmış, pazar güneşli ve 24 derece.", ["hava_tahmini_hafta_sonu_24", "hafta_sonu_hava_24"], "hava_tahmini_hafta_sonu_001", "Mevcut kâğıt kaynağı gerçekten görüldü: yeşil çerçeve, lacivert başlık, Cumartesi Sağanak ve şimşek, Pazar Güneşli 22°C, sol alt kıvrım. Yeni kaynak 24 derece ve yalnız sağanak der; 22 dosyası korunur, şimşek ek bilgisi kaldırılır. Kurmaca ders verisi, güncel hava tahmini değildir."], ["dal_kiragili_001", "Tek kırağılı dal", "yardimci-nesneler/doga/dal", "7-9-fidan", 10, "D3", "kırağı", ["dal_kiragili", "kiragili_dal", "dal_kiragi"], "dal_kuru_tek_001", "Mevcut kuru kahverengi dalın alt soldan üst sağa gövdesi ve üç yan dalı gerçekten görüldü; sol alt kıvrım var. Kaynak kırağı sözcüğünü öğretir; dal taşıyıcısı sanatsal çıkarımdır. Kar yığınlı dal yerine kahverengi kabuk üzerinde ince beyaz kristalimsi çizgiler ve soluk mavi vurgular gerekir. Bağımsız kar tanesi/kristal asseti üretilmez."]]')
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/mutfak_hava_fular_alti_kaniti.json'
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
