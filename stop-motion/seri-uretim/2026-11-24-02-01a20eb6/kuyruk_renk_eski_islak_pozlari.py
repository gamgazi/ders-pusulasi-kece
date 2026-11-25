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
specs=json.loads("[[\"balon_sari_saglam_001\",\"Sarı sağlam balon\",\"yardimci-nesneler/oyun/balon\",\"4-6-kok\",3,\"D1\",\"resim: sarı balon\",[\"balon_sari\",\"sari_balon\"],\"balon_mavi_saglam_001\",\"Mevcut tek mavi sağlam balonun oval gövde, bağlı düğüm, kısa S ipi, beyaz sol üst parıltı ve kâğıt kıvrımı korunur. Yalnız gövde/düğüm sarı renk ailesine dönüştürülür; bir PNG tek balon. Renk kaynakta doğrudan belirtilir. Beyaz balonda opak beyaz merkez korunur; siyah/gri/lacivert ayrımı gerçek görsel QA gerektirir.\"],[\"balon_mor_saglam_001\",\"Mor sağlam balon\",\"yardimci-nesneler/oyun/balon\",\"4-6-kok\",3,\"D3\",\"resim: mor balon\",[\"balon_mor\",\"mor_balon\"],\"balon_mavi_saglam_001\",\"Mevcut tek mavi sağlam balonun oval gövde, bağlı düğüm, kısa S ipi, beyaz sol üst parıltı ve kâğıt kıvrımı korunur. Yalnız gövde/düğüm mor renk ailesine dönüştürülür; bir PNG tek balon. Renk kaynakta doğrudan belirtilir. Beyaz balonda opak beyaz merkez korunur; siyah/gri/lacivert ayrımı gerçek görsel QA gerektirir.\"],[\"balon_gri_saglam_001\",\"Gri sağlam balon\",\"yardimci-nesneler/oyun/balon\",\"4-6-kok\",3,\"D4\",\"resim: gri balon\",[\"balon_gri\",\"gri_balon\"],\"balon_mavi_saglam_001\",\"Mevcut tek mavi sağlam balonun oval gövde, bağlı düğüm, kısa S ipi, beyaz sol üst parıltı ve kâğıt kıvrımı korunur. Yalnız gövde/düğüm gri renk ailesine dönüştürülür; bir PNG tek balon. Renk kaynakta doğrudan belirtilir. Beyaz balonda opak beyaz merkez korunur; siyah/gri/lacivert ayrımı gerçek görsel QA gerektirir.\"],[\"balon_beyaz_saglam_001\",\"Beyaz sağlam balon\",\"yardimci-nesneler/oyun/balon\",\"4-6-kok\",3,\"D4\",\"resim: beyaz balon\",[\"balon_beyaz\",\"beyaz_balon\"],\"balon_mavi_saglam_001\",\"Mevcut tek mavi sağlam balonun oval gövde, bağlı düğüm, kısa S ipi, beyaz sol üst parıltı ve kâğıt kıvrımı korunur. Yalnız gövde/düğüm beyaz renk ailesine dönüştürülür; bir PNG tek balon. Renk kaynakta doğrudan belirtilir. Beyaz balonda opak beyaz merkez korunur; siyah/gri/lacivert ayrımı gerçek görsel QA gerektirir.\"],[\"balon_lacivert_saglam_001\",\"Lacivert sağlam balon\",\"yardimci-nesneler/oyun/balon\",\"4-6-kok\",3,\"D4\",\"resim: lacivert balon\",[\"balon_lacivert\",\"lacivert_balon\"],\"balon_mavi_saglam_001\",\"Mevcut tek mavi sağlam balonun oval gövde, bağlı düğüm, kısa S ipi, beyaz sol üst parıltı ve kâğıt kıvrımı korunur. Yalnız gövde/düğüm lacivert renk ailesine dönüştürülür; bir PNG tek balon. Renk kaynakta doğrudan belirtilir. Beyaz balonda opak beyaz merkez korunur; siyah/gri/lacivert ayrımı gerçek görsel QA gerektirir.\"],[\"balon_pembe_saglam_001\",\"Pembe sağlam balon\",\"yardimci-nesneler/oyun/balon\",\"4-6-kok\",3,\"D4\",\"resim: pembe balon\",[\"balon_pembe\",\"pembe_balon\"],\"balon_mavi_saglam_001\",\"Mevcut tek mavi sağlam balonun oval gövde, bağlı düğüm, kısa S ipi, beyaz sol üst parıltı ve kâğıt kıvrımı korunur. Yalnız gövde/düğüm pembe renk ailesine dönüştürülür; bir PNG tek balon. Renk kaynakta doğrudan belirtilir. Beyaz balonda opak beyaz merkez korunur; siyah/gri/lacivert ayrımı gerçek görsel QA gerektirir.\"],[\"balon_siyah_saglam_001\",\"Siyah sağlam balon\",\"yardimci-nesneler/oyun/balon\",\"4-6-kok\",3,\"D7\",\"resim: siyah balon\",[\"balon_siyah\",\"siyah_balon\"],\"balon_mavi_saglam_001\",\"Mevcut tek mavi sağlam balonun oval gövde, bağlı düğüm, kısa S ipi, beyaz sol üst parıltı ve kâğıt kıvrımı korunur. Yalnız gövde/düğüm siyah renk ailesine dönüştürülür; bir PNG tek balon. Renk kaynakta doğrudan belirtilir. Beyaz balonda opak beyaz merkez korunur; siyah/gri/lacivert ayrımı gerçek görsel QA gerektirir.\"],[\"balon_kahverengi_saglam_001\",\"Kahverengi sağlam balon\",\"yardimci-nesneler/oyun/balon\",\"4-6-kok\",3,\"D7\",\"resim: kahverengi balon\",[\"balon_kahverengi\",\"kahverengi_balon\"],\"balon_mavi_saglam_001\",\"Mevcut tek mavi sağlam balonun oval gövde, bağlı düğüm, kısa S ipi, beyaz sol üst parıltı ve kâğıt kıvrımı korunur. Yalnız gövde/düğüm kahverengi renk ailesine dönüştürülür; bir PNG tek balon. Renk kaynakta doğrudan belirtilir. Beyaz balonda opak beyaz merkez korunur; siyah/gri/lacivert ayrımı gerçek görsel QA gerektirir.\"],[\"balon_turuncu_saglam_001\",\"Turuncu sağlam balon\",\"yardimci-nesneler/oyun/balon\",\"4-6-kok\",3,\"D7\",\"resim: turuncu balon\",[\"balon_turuncu\",\"turuncu_balon\"],\"balon_mavi_saglam_001\",\"Mevcut tek mavi sağlam balonun oval gövde, bağlı düğüm, kısa S ipi, beyaz sol üst parıltı ve kâğıt kıvrımı korunur. Yalnız gövde/düğüm turuncu renk ailesine dönüştürülür; bir PNG tek balon. Renk kaynakta doğrudan belirtilir. Beyaz balonda opak beyaz merkez korunur; siyah/gri/lacivert ayrımı gerçek görsel QA gerektirir.\"],[\"ayakkabi_spor_yirtik_001\",\"Yırtık eski spor ayakkabı\",\"yardimci-nesneler/giysi/spor-ayakkabisi\",\"4-6-filiz\",5,\"D5\",\"resim: yırtık eski ayakkabı\",[\"ayakkabi_spor_yirtik\",\"ayakkabi_yirtik\",\"yirtik_ayakkabi\"],\"ayakkabi_spor_tek_001\",\"Mevcut tek spor ayakkabının yan görünümü, renkleri ve bağlı bağcıkları korunur. Üst burun/yan panelde yırtık düzensiz açıklık ve iki kısa kalkık kumaş kenarı çizilir; iç karanlık astar aynı kâğıda opak mürekkeple çizilir, kâğıtta keyfi alfa deliği açılmaz. Kullanılmışlık birkaç çizili aşınma izi; kir/sıçrama ayrı nesne olmaz.\"],[\"ayakkabi_spor_camurlu_001\",\"Çamurlu eski spor ayakkabı\",\"yardimci-nesneler/giysi/spor-ayakkabisi\",\"4-6-filiz\",5,\"D5\",\"resim: çamurlu eski ayakkabı\",[\"ayakkabi_spor_camurlu\",\"ayakkabi_camurlu\",\"camurlu_ayakkabi\"],\"ayakkabi_spor_tek_001\",\"Aynı tek spor ayakkabının bağlı taban/burun/alt yan yüzeyinde kahverengi marker ile çizilmiş birkaç çamur lekesi; ayrı damla, zemin veya çamur yığını yok. Temel renk kimliği ve kesilmiş kâğıt standardı korunur.\"],[\"havlu_katli_islak_001\",\"Islak katlı havlu\",\"yardimci-nesneler/bakim/havlu\",\"4-6-filiz\",5,\"D5\",\"resim: ıslak havlu\",[\"havlu_katli_islak\",\"havlu_islak\",\"islak_havlu\"],\"havlu_katli_001\",\"Mevcut katlı havlunun biçimi ve çizili renk kimliği korunur. Yüzeye bağlı koyu renk düzensiz ıslak alanlar ve bunların üstünde kısa açık renk parlama kıvrımları çizilir. Su damlaları/ikinci nesne eklenmez. Havlu tekstil fotoğrafı değil, yoğun keçeli kalemle çizilmiş opak kâğıttır. Islak/kuru ayrımı görsel QA’da gerçekten okunmalıdır.\"]]")
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/renk_eski_islak_pozlari_kaniti.json'
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
