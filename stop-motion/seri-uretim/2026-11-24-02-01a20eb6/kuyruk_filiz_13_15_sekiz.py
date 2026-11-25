"""Reconcile eight specific states after full Filiz 13-15 reading and reference inspection."""
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
specs=json.loads('[["termometre_39_001", "Tek 39 derece gösteren termometre", "yardimci-nesneler/saglik/termometre", "13-15-filiz", 7, "D1", "termometre 39 diyor", ["termometre_39", "ates_olcer_39"], "termometre_tek_001", "Mevcut iki çizgili ekran yerine 39 °C; kaynak dersin kurmaca değeridir, ölçüm veya tıbbi öneri değildir."], ["telefon_yeni_mesaj_001", "Tek yeni mesaj bildirimli telefon", "yardimci-nesneler/esya/telefon", "13-15-filiz", 8, "D2", "Yeni mesaj!", ["telefon_yeni_mesaj", "telefon_bildirim"], "telefon_mobil_001", "Ekranda yalnız Yeni mesaj! bildirimi; isim, numara ve gerçek mesaj içeriği yok."], ["telefon_hesap_gizli_001", "Tek gizli hesap ekranlı telefon", "yardimci-nesneler/esya/telefon", "13-15-filiz", 8, "D2", "Hesabını gizli yapmalısın.", ["telefon_hesap_gizli", "telefon_gizlilik"], "telefon_mobil_001", "Ekranda HESAP GİZLİ ve kapalı kilit simgesi. Ders kavramının görsel temsili, gerçek hesap ayarı değişikliği değildir."], ["gorev_cizelgesi_pazartesi_sali_001", "Tek iki günlük görev çizelgesi", "yardimci-nesneler/belgeler/gorev-cizelgesi", "13-15-filiz", 9, "D8", "Pazartesi: Eylül bulaşık, Ahmet çöp. Salı: Ahmet bulaşık, Eylül çamaşır.", ["gorev_cizelgesi", "ev_isi_cizelgesi"], "gorev_listesi_001", "Kaynağın iki günlük görev ve kurmaca kişi eşleşmeleri tek kâğıtta; eski iki onay kutulu görev listesi korunur."], ["hava_tahmini_hafta_sonu_001", "Tek hafta sonu hava tahmini kâğıdı", "yardimci-nesneler/belgeler/hava-tahmini", "13-15-filiz", 11, "D8", "Cumartesi sağanak ve şimşek olacakmış. Pazar güneşli ve 22 derece.", ["hava_tahmini_hafta_sonu", "hafta_sonu_hava_tahmini"], "gorev_listesi_001", "Tek kâğıt üzerinde Cumartesi / Sağanak ve şimşek ile Pazar / Güneşli, 22 °C; kaynak kurmaca ders tahmini, güncel hava verisi değil."], ["gezi_ertelendi_duyurusu_001", "Tek gezi erteleme duyurusu", "yardimci-nesneler/belgeler/duyuru", "13-15-filiz", 15, "D8", "Cuma günkü gezi pazartesiye ertelendi.", ["gezi_ertelendi_duyurusu", "gezi_erteleme_notu"], "not_karti_tek_001", "Tek sarı kâğıtta GEZİ / Cuma → Pazartesi / ERTELENDİ. Cuma günü iptal değil pazartesiye ertelendiği doğru korunur. İzin kâğıdı ayrıca mevcut."], ["sinav_gunu_degisti_notu_001", "Tek sınav günü değişiklik notu", "yardimci-nesneler/belgeler/not", "13-15-filiz", 15, "D9", "Sınav salıdan perşembeye değişti", ["sinav_gunu_degisti", "sinav_gunu_degisiklik"], "not_karti_tek_001", "Tek sarı not SINAV / Salı → Perşembe / DEĞİŞTİ. Saat veya gerçek sınav tarihi uydurulmaz."], ["tarcin_cubugu_tek_001", "Tek tarçın çubuğu", "yardimci-nesneler/yiyecek/tarcin", "13-15-filiz", 14, "D5", "tarçınla süslediler", ["tarcin", "cinnamon"], null, "Tarçın sözcüğünün tek çubuk temsili; kaynak toz/çubuk biçimi belirtmiyor, çubuk bir sanatsal nesne seçimi. Tek kabuk silindiri, demet, kâse veya ek baharat yok."]]')
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/filiz_13_15_sekiz_kaniti.json'
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
