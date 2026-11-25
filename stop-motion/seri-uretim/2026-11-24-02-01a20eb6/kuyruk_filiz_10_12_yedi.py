"""Reconcile eleven needs after full Tohum/Kok reading, including visual color-reference review."""
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
specs=json.loads("[[\"tisort_mavi_001\",\"Tek mavi tişört\",\"yardimci-nesneler/giyim/tisort\",\"10-12-filiz\",11,\"D5\",\"mavi bir tişört aldı\",[\"tisort_mavi\",\"mavi_tisort\"],\"tisort_tek_001\",\"Mevcut sarı tişörtün aynı kısa kollu biçiminde mavi çeşidi; yaka koyu mavi, lacivert kontur. Leke ve beden farkı eklenmez.\"],[\"tisort_yesil_001\",\"Tek yeşil tişört\",\"yardimci-nesneler/giyim/tisort\",\"10-12-filiz\",11,\"D5\",\"yeşil bir tişört getirdi\",[\"tisort_yesil\",\"yesil_tisort\"],\"tisort_tek_001\",\"Mevcut sarı tişörtün aynı kısa kollu biçiminde yeşil çeşidi, yaka koyu yeşil. Dar/bol beden ilişkisi figürsüz kanıtlanmış sayılmaz.\"],[\"tisort_mavi_lekeli_001\",\"Tek kolu lekeli mavi tişört\",\"yardimci-nesneler/giyim/tisort\",\"10-12-filiz\",11,\"D5\",\"kolunda küçük bir leke vardı\",[\"tisort_mavi_lekeli\",\"tisort_lekeli\",\"lekeli_tisort\"],\"tisort_tek_001\",\"Aynı kısa kollu tişört mavi; görselin sağ kolunun yüzeyinde küçük düzensiz kahverengi tek leke. Yırtık/delik yok. Ders metnindeki mavi renk ve kol lekesi beraber temsil edilir; leke tek giysinin yüzey çizimi.\"],[\"ceket_kirmizi_001\",\"Tek kırmızı ceket\",\"yardimci-nesneler/giysi/ceket\",\"10-12-filiz\",11,\"D3\",\"Kırmızı ceketi mavi ceketle değiştirmek:\",[\"ceket_kirmizi\",\"kirmizi_ceket\"],\"ceket_tek_001\",\"Mevcut mor iki sarı düğmeli, iki cepli ceket kırmızı; yakalar açık kırmızı, iç astar koyu kırmızı. Aynı kalın lacivert kontur ve sol manşet kıvrımı korunur.\"],[\"ceket_mavi_001\",\"Tek mavi ceket\",\"yardimci-nesneler/giysi/ceket\",\"10-12-filiz\",11,\"D3\",\"Kırmızı ceketi mavi ceketle değiştirmek:\",[\"ceket_mavi\",\"mavi_ceket\"],\"ceket_tek_001\",\"Mevcut mor iki sarı düğmeli, iki cepli ceket mavi; yakalar açık mavi, iç astar koyu mavi. Yağmurluk/mont değil yakalı ceket.\"],[\"dis_fircasi_macunlu_001\",\"Tek macun sürülmüş diş fırçası\",\"yardimci-nesneler/bakim/dis-fircasi\",\"10-12-filiz\",1,\"D3\",\"Diş fırçasına biraz\",[\"dis_fircasi_macunlu\",\"macunlu_dis_fircasi\"],\"dis_fircasi_001\",\"D3 doğru cevap diş macunu. Mevcut kırmızı-lacivert fırçanın kılları üstünde küçük opak beyaz, açık turkuaz izli bağlı macun şeridi. Tüp/diş/eller/su yok; miktar veya sağlık tavsiyesi değil nesne kullanım pozu.\"],[\"tablet_sarji_bitmis_001\",\"Tek şarjı bitmiş tablet\",\"yardimci-nesneler/teknoloji/tablet\",\"10-12-filiz\",8,\"D8\",\"Şarjı bitti, şarja tak.\",[\"tablet_sarji_bitmis\",\"tablet_sarjsiz\",\"tablet_pil_bos\"],\"tablet_tek_001\",\"Mevcut mor çerçeveli tabletin ekranı koyu gri; ortada tek boş pil simgesi, küçük kırmızı son çizgi. Pil simgesi ekrana çizili, ayrı pil nesnesi değil. Gerçek şifre/uygulama/şarj kablosu yok.\"]]")
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/filiz_10_12_yedi_kaniti.json'
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
    item={'id':aid,'title':title,'category':cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':rel,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+pointer,'match':'exact_json_leaf' if value==term else 'substring_of_exact_json_leaf','leaf_sha256':hashlib.sha256(value.encode()).hexdigest()}],'felt_cards_preserved':cardids,'role':'missing pose of existing paper helper' if baseid else 'independent missing paper helper','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} records, {len(canonical)} canonical PNGs, {len(q["items"])} queue items','source_is_action_inference':True,'semantic_review':semantic+' Seçilen tam mevcut ders alanı okundu. Mevcut R/K kartlar ve temel yardımcı nesne dosyaları korunur. Üretim sonrası her PNG için ayrı teknik ve üç görünümde sanatsal QA gerekir; poz hizası/animasyon henüz doğrulanmış değildir. Tüm müfredat ayrıştırması bitmedi.'}
    if reference:item['pose_reference']=reference
    new.append(item)
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blobs_sha_verified':{k:v[1] for k,v in sources.items()},'base_references':[x['pose_reference'] for x in new if 'pose_reference' in x],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'records':len(h),'pngs':len(canonical)}))
