"""Reconcile ten specific states after full Cinar/Orman13-15 and Tohum16-17 reading and reference inspection."""
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
specs=json.loads('[["saat_calar_07_30_001", "Tek07.30gösteren çalar saat", "yardimci-nesneler/esya/saat", "16-17-cinar", 14, "D5", "18.00–19.30", ["saat_calar_07_30", "saat_07_30"], "saat_calar_09_30_001", "Toplantı bitişi19.30analog07.30ile aynı poz. Temel saat gerçekten incelendi; yeni24saat kopyası yapılmaz."], ["tablet_goruntulu_arama_001", "Tek görüntülü arama ekranlı tablet", "yardimci-nesneler/teknoloji/tablet", "16-17-fidan", 12, "D5", "görüntülü konuşmayı", ["tablet_goruntulu", "goruntulu_arama_tablet", "tablet_video_arama"], "tablet_tek_001", "Kaynakta huzurevindeki kişinin elindeki tablet ve görüntülü görüşme açıkça var. Mor yatay tablet/turkuaz ekran/sağ düğme/sol alt kıvrım gerçekten incelendi. Telefona özgü ekranla aynı cihaz değildir."], ["mama_kabi_dolu_001", "Tek mamayla dolu kap", "yardimci-nesneler/esya/mama-kabi", "10-12-agac", 16, "D5", "Her hafta bir avuç mama bile yeter.", ["mama_kabi_dolu", "dolu_mama_kabi", "mama_kabi_mamali"], "mama_kabi_bos_001", "Mevcut mavi/turuncu kap gerçekten incelendi; kaynakta kaba mama koyma yardımından dolu durumu çıkarılır. Kuru mama çizimi kap içindedir, dışta ayrı taneler yok. Her hafta ifadesi beslenme yeterliliği tavsiyesi yapılmaz."], ["gomlek_beyaz_kirisik_001", "Tek kırışık beyaz gömlek", "yardimci-nesneler/giyim/gomlek", "16-17-filiz", 9, "D3", "Gömleğin kırış kırış", ["gomlek_beyaz_kirisik", "gomlek_kirisik", "gomlek_burusuk"], "gomlek_beyaz_001", "Mevcut beyaz kısa kollu beş düğmeli cepli gömlek gerçekten incelendi. Kâğıt kat izinden ayrı olarak çizilmiş giysi kırışıklıkları gerekir; kaynak kırış kırış diyor. Renk sanatsal olarak mevcut temel beyazdan korunur."], ["kazak_yirtik_001", "Tek yırtık turuncu kazak", "yardimci-nesneler/giyim/kazak", "16-17-filiz", 2, "D2", "Bu kazak ucuz ama ____ iyi değil; iki haftada yırtıldı.", ["kazak_yirtik", "yirtik_kazak"], "kazak_tek_001", "Mevcut turuncu/lacivert kazak gerçekten incelendi. Yırtılma kaynakta açık; tek bağlantılı kazakta bir yırtık açıklığı beyaz kesim payıyla temsil edilir. Ayrı kopmuş kumaş parçası yok."], ["telefon_alarm_05_00_001", "Tek05.00alarm ekranlı telefon", "yardimci-nesneler/teknoloji/telefon", "16-17-tohum", 4, "D5", "Sabah beşte alarm kuruyor", ["telefon_alarm_05_00", "telefon_05_00_alarm"], "telefon_mobil_001", "D5te05.00alarm,D6da telefonda saat ayarlamak var. Mevcut kırmızı/mavi telefon korunur. Analog05.00saat mevcut olsa da alarm ayarı farklı ekran işlevidir."], ["telefon_hava_hamburg_12_001", "Tek Hamburg12derece hava ekranlı telefon", "yardimci-nesneler/teknoloji/telefon", "16-17-tohum", 8, "D5", "Hamburg\'da hava kapalı ve nemli, yağmur da var.", ["telefon_hava_hamburg", "hava_hamburg_12", "telefon_hamburg_12"], "telefon_mobil_001", "Kaynakta telefondaHamburg/12derece/kapalı/nemli/yağmur var. Mevcut hafta sonu hava kağıdı gerçekten açıldı:Cumartesisağanak/şimşek,Pazargüneşli22derece; farklı veri/taşıyıcı. Bu dersin kurmaca ekranı,güncel hava tahmini değildir."], ["dis_macunu_bos_001", "Tek bitmiş diş macunu tüpü", "yardimci-nesneler/bakim/dis-macunu", "16-17-kok", 11, "D8", "Diş fırçam var, ama diş macunum bitti.", ["dis_macunu_bos", "dis_macunu_bitmis", "bos_dis_macunu"], "dis_macunu_kapali_001", "Mevcut yatay beyaz/turkuaz tüp,diş simgesi,sağ mavi kapak,sol üst kıvrım gerçekten açıldı. Biten tüp fiziksel olarak yassılaştırılıp kuyruktan kıvrılmış temsil edilir; bu temsil çıkarım. Ayrı kapak/macunsızıntısı yok."]]')
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/gunluk_poz_sekiz_kaniti.json'
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
