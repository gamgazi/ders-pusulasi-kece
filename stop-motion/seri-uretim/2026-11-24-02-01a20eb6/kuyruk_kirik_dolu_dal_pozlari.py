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
specs=json.loads("[[\"bardak_kirik_001\",\"Kenarı kırılmış bardak\",\"yardimci-nesneler/mutfak/bardak\",\"4-6-fidan\",3,\"D1\",\"resim: kırık bardak\",[\"bardak_kirik\",\"kirik_bardak\"],\"bardak_bos_001\",\"Mevcut boş bardağın tek gövdesi korunur. Üst ağız kenarında belirgin tek V biçimli eksik kırık çentik ve onun altına inen ince lacivert çatlak. Kırılmış ayrı parça gösterilmez; bardak halen tek bağlı opak kâğıt nesnesi. Su/el/masa yok. Dersin yanıltıcı seçenek nesnesidir; kaynakta kırık olarak açıkça belirtilir.\"],[\"kova_mavi_dolu_001\",\"Su dolu mavi kova\",\"yardimci-nesneler/bahce/kova\",\"4-6-fidan\",4,\"D3\",\"resim: dolu kova\",[\"kova_mavi_dolu\",\"kova_dolu\"],\"kova_mavi_001\",\"Mevcut mavi kovanın gövde ve kulbu korunur; açık ağzın içinde belirgin turkuaz mavi su yüzeyi üst sınıra yakın görünür. Su kovaya ait içerik; damla/dökülme/ikinci kap yok. Doluluk kaynakta doğrudan istenir. Tek bağlı kâğıt nesnesi, kulp iç boşluğu gerçek alfa.\"],[\"kova_mavi_kirik_001\",\"Kırık mavi kova\",\"yardimci-nesneler/bahce/kova\",\"4-6-fidan\",4,\"D3\",\"resim: kırık kova\",[\"kova_mavi_kirik\",\"kova_kirik\",\"kirik_kova\"],\"kova_mavi_001\",\"Mevcut mavi boş kovanın üst kenarında belirgin kırık çentik ve gövdeye inen düzensiz lacivert çatlak. Ana gövde/kulp tek bağlı parça; ayrık kırık parça veya su gösterilmez. Kulp ve çevrede beyaz makas payı, dış ve kulp içi alfa korunur. Kaynakta boş/dolu/kırık karşılaştırması.\"],[\"dikkat_isareti_001\",\"Tek dikkat işareti\",\"yardimci-nesneler/semboller/dikkat\",\"4-6-fidan\",14,\"D1\",\"resim: dikkat işareti\",[\"dikkat_isareti\",\"uyari_ucgeni\"],null,\"Tek sarı uyarı üçgeni içinde lacivert ünlem çizimi. Üçgen sarı alan tek opak kâğıt nesnesi; ünlem noktası bu yüzeye basılı, ayrı kesilmiş nokta değil. Direk/çerçeve kutusu/yazı yok. Genel eğitim dikkat simgesi, resmi trafik/iş güvenliği standardı iddiası yok.\"],[\"dal_karli_001\",\"Üzerinde kar olan dal\",\"yardimci-nesneler/bahce/dal\",\"4-6-cinar\",7,\"D7\",\"resim: karlı dal\",[\"dal_karli\",\"karli_dal\"],\"dal_kuru_tek_001\",\"Aynı kuru dal temelinin ana gövde ve üç yan uç düzeni korunur. Üst yüzeylere bağlı birkaç beyaz kar şeridi; açık mavi marker kıvrımlarıyla çizilmiş opak kâğıt kar. Kar ayrı düşen taneler değil dala bağlı tek nesne. Yaprak/çiçek/zemin/ikinci dal yok.\"],[\"dal_cicekli_001\",\"Çiçek açmış dal\",\"yardimci-nesneler/bahce/dal\",\"4-6-cinar\",7,\"D7\",\"resim: çiçek açan dal\",[\"dal_cicekli\",\"cicekli_dal\"],\"dal_kuru_tek_001\",\"Aynı kuru dal ana gövde ve üç yan uç düzeni korunur. Dala bağlı üç küçük pembe çiçek başı, her birinde beş düzensiz petal ve sarı merkez; ayrı uçuşan petal/çiçek yok. Tek çiçekli dal nesnesi; kavanoz/vazo/zemin/ikinci dal yok. Genel bahar dalı, tür/çeşit iddiası yok.\"]]")
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/kirik_dolu_dal_pozlari_kaniti.json'
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
