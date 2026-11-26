"""Reconcile five food process and comparison states against actual sources and accepted assets."""
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
specs=json.loads('[["peynir_rendelenmis_yigin_001", "Tek rendelenmiş peynir yığını", "yardimci-nesneler/yiyecek/peynir", "4-6-fidan", 9, "D3", "resim: peynir rendeleyen Pingucan", ["peynir_rendelenmis", "rendelenmis_peynir", "rende_peynir", "peynir_rende_yigini"], "peynir_dilim_001", "Mevcut sarı peynir dilimi r03 ham PNG görüldü: sarı/oker yoğun mürekkep, açık delik çizimleri, üst sağ kıvrım. Rendeleme eyleminin sonuç durumu tek bağlantılı sarı peynir yığınıdır. Rende ve karakter ayrı mevcut katmanlardır. Yığın çevresinde bağımsız peynir şeritleri olmayacak."], ["nar_yarim_001", "Tek kesilmiş yarım nar", "yardimci-nesneler/yiyecek/nar", "7-9-agac", 8, "D6", "Kırmızı taneleri var", ["nar_yarim", "yarim_nar", "nar_kesilmis", "kesilmis_nar", "nar_ici_acik"], "nar_butun_001", "Mevcut kırmızı bütün narın üç uçlu tacı, yoğun kırmızı geniş mürekkebi ve sol alt kıvrımı görüldü. Bilmecenin kırmızı taneler ipucunu görünür kılmak için tek kesik yarım nar durumuna geçilir; kaynakta kesme eylemi varmış gibi gösterilmez. Taneler meyvenin kesik yüzeyinde, ayrı dağınık parçalar değildir."], ["sut_dokulmus_birikinti_001", "Tek dökülmüş süt birikintisi", "yardimci-nesneler/yiyecek/sut", "7-9-agac", 1, "D3", "Süt de yere dökülmüş.", ["sut_dokulmus", "dokulmus_sut", "sut_birikintisi", "sut_birikinti"], "su_birikintisi_001", "Mevcut su birikintisi r01 ham PNG görüldü: turkuaz loblu yayvan siluet, üç koyu iç kavis, sağ alt kıvrım. Süt durumu opak beyaz olmalıdır; koyu iç su dalgaları yerine az sayıda çok açık gri-mavi çizgi. Mevcut su dosyası korunur; bardak, kedi, ayak izi veya zemin eklenmez."], ["kurabiye_kutusu_bos_001", "Tek açık boş kurabiye kutusu", "yardimci-nesneler/mutfak/kurabiye-kutusu", "7-9-agac", 1, "D6", "kurabiye kutusu boşalmış!", ["kurabiye_kutusu", "kurabiye_kabi", "biskuvi_kutusu", "kurabiye_teneke"], "", "Kaynak açıkça boşalan kurabiye kutusunu belirtir. Oyuncak kutusu, kayıp eşya kutusu ve süt kutusuyla işlev/biçim farkı vardır. Tek menteşeli kapağı gövdeye bağlı açık metal kutu, boş iç yüzey; kurabiye kimliği kapağın üstündeki tek düz kurabiye çiziminden okunur. İçeride ayrı kurabiye veya kırıntı yok."], ["corba_sicak_buharli_001", "Tek buharlı sıcak çorba kâsesi", "yardimci-nesneler/yiyecek/corba", "4-6-orman", 19, "D3", "resim: sıcak çorba", ["corba_sicak", "sicak_corba", "corba_buharli", "buharli_corba"], "corba_kasesi_001", "Mevcut çorba kâsesi r01 ham PNG görüldü: mavi gövde, beyaz zikzak bant, turuncu çorba yüzeyi, sol alt kıvrım; buhar yok. Kaynaktaki sıcak-soğuk ayrımı için sıcak duruma kâse kenarına bağlı tek beyaz kâğıt taşıyıcı içinde üç yükselen çizimli buhar şeridi eklenir; ayrı kopuk duman parçaları üretilemez. Soğuk seçenek mevcut buharsız kâseyle karşılanır, ölçülen sıcaklık iddiası yok."]]')
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/mutfak_surec_bes_kaniti.json'
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
