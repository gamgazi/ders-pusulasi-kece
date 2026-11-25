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
specs=json.loads("[[\"kabartma_tozu_paket_001\",\"Tek kapalı kabartma tozu paketi\",\"yardimci-nesneler/mutfak/kabartma-tozu\",\"13-15-kok\",3,\"D6\",\"kabartma tozu\",[\"kabartma_tozu\"],null,\"Tek küçük kapalı sarı kabartma tozu poşeti; üst/alt kapalı kıvrım, KABARTMA TOZU yazısı. Marka, gramaj, dökülen toz, kek veya ikinci paket yok. Un/şeker/tuz paketlerinden farklı mutfak malzemesi.\"],[\"kurdan_tek_001\",\"Tek kürdan\",\"yardimci-nesneler/mutfak/kurdan\",\"13-15-kok\",3,\"D7\",\"Bir kürdanla kontrol edin.\",[\"kurdan\"],null,\"Tek ince ahşap renkli kürdan, iki ucu sivrilen düz çubuk; yoğun oker marker çizgileri. Ağız/el/yiyecek/ikinci çubuk yok; kullanım gösterimi değil ders nesnesi. Sahnede küçük ölçeklenir.\"],[\"komodin_kapali_001\",\"Tek komodin\",\"yardimci-nesneler/ev/komodin\",\"13-15-kok\",5,\"D3\",\"komodin\",[\"komodin\"],null,\"Tek alçak küçük komodin; iki kapalı çekmece, iki yuvarlak kulp ve dört kısa ayak. Turuncu gövde/mavi çekmece; yatak, lamba veya üstünde eşya yok. Bağımsız çekmece ve duvar rafından farklı mobilya.\"],[\"gardirop_kapali_001\",\"Tek kapalı gardırop\",\"yardimci-nesneler/ev/gardirop\",\"13-15-kok\",5,\"D3\",\"gardırop\",[\"gardirop\",\"gardrop\"],null,\"Tek uzun iki kapaklı giysi gardırobu; iki bağlı kulp, dört kısa ayak. Mavi kapaklar turuncu çerçeve, kapalı. Giysi, ayna, yatak, insan veya ikinci mobilya yok; genel dolaptan giysi dolabı biçimi.\"],[\"kitaplik_bos_001\",\"Tek boş kitaplık\",\"yardimci-nesneler/ev/kitaplik\",\"13-15-kok\",5,\"D3\",\"kitaplık\",[\"kitaplik\"],null,\"Tek uzun ayaklı kitaplık; turuncu dış çerçeve ve üç mavi rafla dört boş bölme, opak turkuaz arka panel. Kitap, dekor veya duvar yok. Mevcut raf/ayakkabılıktan ayrı mobilya.\"],[\"okul_servisi_yandan_001\",\"Tek okul servis minibüsü\",\"yardimci-nesneler/ulasim/okul-servisi\",\"13-15-kok\",8,\"D4\",\"okul servisi\",[\"okul_servisi\",\"okul_servis\",\"servis_minibusu\"],null,\"Tek beyaz/turuncu okul servis minibüsü yandan; iki görünür tekerlek, kapalı sürgülü kapı, mavi camlar ve OKUL SERVİSİ yazısı. Çocuk/şoför/plaka/şehir/yol yok; mevzuata uygun gerçek araç iddiası değil genel ders resmi.\"],[\"ogrenci_ulasim_karti_001\",\"Tek örnek öğrenci ulaşım kartı\",\"yardimci-nesneler/okul/ogrenci-karti\",\"13-15-kok\",8,\"D6\",\"öğrenci kartı\",[\"ogrenci_karti\",\"ogrenci_ulasim_karti\"],null,\"Ders ulaşım bağlamında öğrenci kartı: tek turkuaz kart, ÖĞRENCİ KARTI / ÖRNEK yazısı ve basit basılı otobüs simgesi. Kimlik numarası, kişi fotoğrafı, barkod/QR, gerçek kurum veya bakiye yok. Kütüphane/kredi kartından işlev ayrı.\"],[\"enerji_icecegi_kutu_001\",\"Tek kapalı enerji içeceği kutusu\",\"yardimci-nesneler/yiyecek/enerji-icecegi\",\"13-15-kok\",11,\"D7\",\"enerji içeceği\",[\"enerji_icecegi\"],null,\"Tek uzun mor kapalı içecek kutusu, gri bağlı çekme halkası ve ENERJİ İÇECEĞİ yazısı. Marka, performans/sağlık iddiası, kişi veya tüketim özendirmesi yok; kaynağın sağlıklı yaşam dersindeki tartışma nesnesi. Gazoz kutusundan etiket ve biçim farklı.\"],[\"heykel_tek_001\",\"Tek soyut heykel\",\"yardimci-nesneler/sanat/heykel\",\"13-15-kok\",13,\"D3\",\"heykel\",[\"heykel\"],null,\"Tek bronz renkli soyut S kıvrımlı dik heykel kendi küçük mavi kaidesine bağlı; metal nesneyi yoğun marker ile kâğıt olarak resmet. Gerçek sanatçı eseri veya insan karakteri değil özgün genel sanat nesnesi; müze/arka plan yok.\"],[\"maske_parti_001\",\"Tek parti maskesi\",\"yardimci-nesneler/kutlama/maske\",\"13-15-kok\",14,\"D3\",\"maske\",[\"maske\"],null,\"Tek turkuaz/turuncu yarım yüz parti maskesi; burun köprüsüyle birleşen iki göz çevresi ve iki gerçek alfa göz deliği, beyaz iç makas paylı. İp/tüy/baş/insan/ikinci maske yok. Tıbbi maske veya yüz karakteri değil parti aksesuarı.\"],[\"tebrik_karti_001\",\"Tek doğum günü tebrik kartı\",\"yardimci-nesneler/kutlama/tebrik-karti\",\"13-15-kok\",14,\"D6\",\"tebrik kartı\",[\"tebrik_karti\"],null,\"Tek hafif açılmış katlı turkuaz tebrik kartı, ön yüzde İYİ Kİ DOĞDUN! yazısı ve basılı küçük turuncu kalp. Basılı motif aynı kartın parçası; zarf/ikinci kart/kişisel ad yok. Kartpostal ve davetiyeden işlev farklı.\"],[\"karne_ornek_001\",\"Tek örnek karne\",\"yardimci-nesneler/okul/karne\",\"13-15-kok\",16,\"D4\",\"karne\",[\"karne\"],null,\"Tek opak krem belge, KARNE / ÖRNEK başlıkları ve Ad / Ders / Not alanları boş; kısa üç satırlı tablo aynı belge üzerindeki basılı çizimdir, nesne grid/kolajı değildir. Not, kişi, imza, resmî mühür/kurum logosu yok.\"]]")
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/kok_13_15_kuyruk_kaniti.json'
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
