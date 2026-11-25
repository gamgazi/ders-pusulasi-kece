"""Reconcile seven specific states after full Agac reading and reference inspection."""
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
specs=json.loads('[["soru_listesi_001", "Tek görüşme soruları listesi", "yardimci-nesneler/belgeler/soru-listesi", "10-12-agac", 6, "D4", "soru listesi", ["soru_listesi", "gorusme_sorulari", "roportaj_sorulari"], "gorev_listesi_001", "Görev listesinden farklı olarak görüşme öncesi soru kâğıdı. Tek sayfada SORULAR başlığı ve derste geçen üç soru okunur biçimde yazılır; ayrı kalem/el yok."], ["afis_mavi_001", "Tek mavi çevre afişi", "yardimci-nesneler/okul/afis", "10-12-agac", 9, "D2", "afiş mavi olacak", ["afis_mavi", "mavi_afis", "poster_mavi", "mavi_poster"], "afis_tek_001", "Mevcut TEMİZ PARK afişinin kâğıt yüzeyi mavi mürekkeple dolu çeşidi; metin açık beyaz, yaprak simgesi ve turuncu çerçeve korunur. Beyaz makas payı maviye boyanmaz."], ["sutun_grafik_okula_gelis_001", "Tek okula geliş sütun grafiği", "yardimci-nesneler/belgeler/sutun-grafik", "10-12-agac", 12, "D5", "on öğrenci arabayla, beş öğrenci yürüyerek, beş öğrenci de bisikletle", ["sutun_grafik_okula_gelis", "okula_gelis_grafigi", "ulasim_grafigi"], "sutun_grafik_sayfasi_001", "Tek kâğıtta ARABA 10, YAYA 5, BİSİKLET 5 sütunları. Ortak taban, eşit genişlik ve 2:1:1 yükseklik oranı, toplam 20. Kaynak metnin kesik devamı uydurulmaz; mevcut genel grafiğin sayısal durumu eksikti."], ["sutun_grafik_mevsimler_001", "Tek mevsim seçimi sütun grafiği", "yardimci-nesneler/belgeler/sutun-grafik", "10-12-agac", 12, "D8", "Yaz: 12 öğrenci. Kış: 6 öğrenci. İlkbahar: 4. Sonbahar: 2.", ["sutun_grafik_mevsimler", "mevsim_grafigi", "mevsim_secimi_grafigi"], "sutun_grafik_sayfasi_001", "Tek kâğıtta soldan YAZ 12, KIŞ 6, İLKBAHAR 4, SONBAHAR 2; ortak taban, eşit genişlik ve 6:3:2:1 yükseklik oranı. Sonbahar en kısa, yaz en uzun. Ayrı mevsim simgeleri yok."], ["cizgi_grafik_dusus_001", "Tek düşüş gösteren çizgi grafiği", "yardimci-nesneler/belgeler/cizgi-grafik", "10-12-agac", 12, "D6", "Bir sayı önce yüksek, sonra daha az olursa", ["cizgi_grafik_dusus", "dusus_grafigi", "azalis_grafigi"], "cizgi_grafik_sayfasi_001", "Tek sayfa DÜŞÜŞ başlığı, önce yüksek ve sonra düşük iki turuncu nokta arasında aşağı eğimli çizgi. ÖNCE/SONRA etiketleri. Kaynakta bulunmayan sayısal değer, ay veya sıcaklık eklenmez. Mevcut yükselen örnek korunur."], ["yapboz_iki_parca_eksik_001", "Tek iki parçası eksik yapboz tahtası", "yardimci-nesneler/oyun/yapboz", "10-12-filiz", 11, "D2", "Yapbozda iki parça yok", ["yapboz_iki_parca_eksik", "yapboz_eksik", "eksik_yapboz", "yapboz_tahtasi"], "yapboz_parcasi_tek_001", "Tek bağlı yapboz tahtası, tüm yüzeye yayılan turkuaz gökyüzü ve turuncu güneş resmi; iki ayrı iç parça yeri boş, bu iki yuvanın altında opak açık kahverengi tahta tabanı görünür. Etrafa dağılmış ayrı parçalar yok. Tahtadaki bağlantı deseni nesnenin kendi yapısıdır; çoklu varlık kolajı değildir."], ["arti_eksi_karsilastirma_sayfasi_001", "Tek artılar eksiler karşılaştırma sayfası", "yardimci-nesneler/belgeler/karsilastirma", "10-12-agac", 15, "D5", "artılarını ve eksilerini yazalım", ["arti_eksi_karsilastirma", "artilar_eksiler", "arti_eksi_sayfasi"], "gorev_listesi_001", "Tek kâğıt, SPOR KULÜBÜ başlığı ve ARTILAR/EKSİLER iki sütun. Kaynaktaki artılar Arkadaşlar / Hareket; eksi Cumartesi sabahı. İç çizgiler tek sayfanın tablosudur; ayrı kart veya kolaj değildir."]]')
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/agac_10_12_yedi_kaniti.json'
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
