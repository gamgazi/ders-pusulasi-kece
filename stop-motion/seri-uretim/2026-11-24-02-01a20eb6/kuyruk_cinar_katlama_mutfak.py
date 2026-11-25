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
specs=json.loads("[[\"surahi_bos_001\",\"Boş sürahi\",\"yardimci-nesneler/mutfak/surahi\",\"7-9-fidan\",6,\"D6\",\"suyu bir sürahiye koydular.\",[\"surahi\"],null,\"Tek boş mavi sürahi, üst açık ağız ve akıtma dudağı, yanda tek bağlı kulp. Kağıt gövde opak; kulp açıklığı gerçek alfa. Kaynaktaki sürahi için önce boş taban üretilir; limonata/sıvı/bardak eklenmez. İç içe oku alanı soru kısmında kesiktir; mevcut nesne cümlesi tam, eksik soru tamamlanmış sayılmaz.\"],[\"ucak_kagit_001\",\"Tek kâğıt uçak\",\"yardimci-nesneler/oyuncak/kagit-ucak\",\"10-12-fidan\",3,\"D8\",\"Uçağı ____ önce bir kâğıt seç.\",[\"ucak_kagit\",\"kagit_ucak\"],null,\"Katlama eyleminden tek kağıt uçak çıkarımı. Sivri burun, iki bağlı kanat ve orta kat izi; uçan gerçek uçak, maket kit, ikinci kağıt veya el yok.\"],[\"origami_kus_001\",\"Tek origami kuş\",\"yardimci-nesneler/sanat/origami-kus\",\"10-12-fidan\",3,\"D2\",\"Kâğıdı katlayıp kuş ya da çiçek yapmak:\",[\"origami_kus\",\"origami\"],null,\"Origami örneği olarak tek katlanmış kağıt kuş seçimi. İki bağlı açısal kanat, ince katlı boyun, küçük sivri gaga ve kuyruk; gerçek kuş tüyleri/göz/ayak eklenmez. Nesne seçimi kaynakta kuş veya çiçek örneğine dayanır; kuş türü veya adım adım katlama şeması iddiası yok.\"],[\"mama_paketi_kapali_001\",\"Kapalı evcil hayvan maması paketi\",\"yardimci-nesneler/evcil-hayvan/mama-paketi\",\"4-6-cinar\",9,\"D4\",\"resim: kedi ve köpek maması\",[\"mama_paketi\"],null,\"Tek kapalı yeşil mama paketi; MAMA yazısı ve basit basılı pati işareti. Kedi veya köpek nesnesi, ayrı mama tanesi, kase yok. Boş mama kabı ve kuş yemi paketinden ayrı nesne; ambalaj seçimi görsel temsil kararıdır.\"],[\"oyun_karti_destesi_001\",\"Tek oyun kartı destesi\",\"yardimci-nesneler/oyun/kart-destesi\",\"4-6-cinar\",8,\"D5\",\"deste\",[\"oyun_karti_destesi\",\"kart_destesi\"],null,\"Tek kompakt dikdörtgen kart destesi, beyaz yan kenarda birkaç katman çizgisi, üstte tek mavi arka yüz ve basılı turuncu yıldız. Dağılmış/açılmış kartlar, ızgara, kolaj veya birden fazla ayrı varlık yok. Tek bağlı nesne silueti; mevcut joker kartı ve oyun tahtası korunur.\"],[\"portakal_soyulmus_001\",\"Soyulmuş bütün portakal\",\"yardimci-nesneler/yiyecek/portakal\",\"4-6-cinar\",15,\"D3\",\"Portakalı soydum, başucuma koydum.\",[\"portakal_soyulmus\"],\"portakal_butun_001\",\"Mevcut portakalın tamamen kabuğu soyulmuş fakat dilimleri ayrılmamış tek meyve hali. Açık turuncu birleşik dilim yüzeyleri, aralarda ince krem zar çizgileri ve üstte küçük açık krem merkez; kabuk ve yeşil yaprak çıkarılmıştır. Ayrı kabuk, ayrı dilim veya el yok. Referansın yoğun turuncu mürekkebi/lacivert konturu/kağıt dili korunur; değişiklik eylemden poz çıkarımıdır.\"]]")
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/cinar_katlama_mutfak_kaniti.json'
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
    item={'id':aid,'title':title,'category':cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':rel,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+pointer,'match':'exact_json_leaf' if value==term else 'substring_of_exact_json_leaf','leaf_sha256':hashlib.sha256(value.encode()).hexdigest()}],'felt_cards_preserved':cardids,'role':'missing pose of existing paper helper' if baseid else 'independent missing paper helper','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} records, {len(canonical)} canonical PNGs, {len(q["items"])} queue items','source_is_action_inference':aid in {'ucak_kagit_001','origami_kus_001','portakal_soyulmus_001'},'semantic_review':semantic+' Seçilen tam mevcut ders alanı okundu. Mevcut R/K kartlar ve temel yardımcı nesne dosyaları korunur. Üretim sonrası her PNG için ayrı teknik ve üç görünümde sanatsal QA gerekir; poz hizası/animasyon henüz doğrulanmış değildir. Tüm müfredat ayrıştırması bitmedi.'}
    if reference:item['pose_reference']=reference
    new.append(item)
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blobs_sha_verified':{k:v[1] for k,v in sources.items()},'base_references':[x['pose_reference'] for x in new if 'pose_reference' in x],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'records':len(h),'pngs':len(canonical)}))
