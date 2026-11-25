"""Reconcile eight specific states after full Fidan 13-15 reading and reference inspection."""
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
specs=json.loads('[["saat_calar_09_30_001", "Tek 09.30 gösteren çalar saat", "yardimci-nesneler/esya/saat", "13-15-fidan", 5, "D8", "yeni saat dokuz buçuk", ["saat_calar_09_30", "saat_9_30", "saat_dokuz_bucuk"], "saat_calar_10_30_001", "Uzun yelkovan 6, kısa akrep 9 ile 10 ortasında. 10.30 temel çizimi korunur; tam açı kalibrasyonu ve animasyon hizası ayrı doğrulama gerektirir."], ["skor_tabelasi_2_1_001", "Tek 2–1 skor tabelası", "yardimci-nesneler/spor/skor-tabelasi", "13-15-fidan", 11, "D9", "2-1 kazandık", ["skor_tabelasi_2_1", "skor_2_1"], "skor_tabelasi_1_1_001", "Sarı başlık SKOR olur; eski BERABERE sözcüğü kaldırılır, büyük 2–1 skoru gösterilir. Takım adı veya gerçek maç sonucu yok."], ["telefon_sesli_mesaj_001", "Tek sesli mesaj ekranlı telefon", "yardimci-nesneler/esya/telefon", "13-15-fidan", 10, "D4", "sesli mesaj", ["telefon_sesli_mesaj", "sesli_mesaj_telefon"], "telefon_mobil_001", "Tek telefon ekranında SESLİ MESAJ, oynat simgesi ve ses dalgası. Ses dosyası, süre, arayan kişi veya gerçek mesaj yok."], ["telefon_dogrulama_kodu_001", "Tek doğrulama kodu ekranlı telefon", "yardimci-nesneler/esya/telefon", "13-15-fidan", 12, "D2", "Şifreden sonra bir de telefona kod gelmesi", ["telefon_dogrulama_kodu", "telefon_iki_asamali", "telefon_iki_adimli"], "telefon_mobil_001", "Ekranda DOĞRULAMA KODU ve altı boş kod alanı; kod uzunluğu sanatsal ekran tercihi, kaynak altı rakam söylemiyor. Gerçek kod veya kimlik bilgisi yok; tüm iki aşamalı işlem yapılmış sayılmaz."], ["telefon_kisi_engellendi_001", "Tek engellenmiş kişi ekranlı telefon", "yardimci-nesneler/esya/telefon", "13-15-fidan", 12, "D2", "artık sana mesaj atamasın", ["telefon_kisi_engellendi", "telefon_engellendi"], "telefon_mobil_001", "Ekranda KİŞİ ENGELLENDİ ve engel simgesi. İsimsiz ders durumu; gerçek kişi/hesap engelleme yapılmaz."], ["tisort_dikisi_sokulmus_001", "Tek dikişi sökülmüş tişört", "yardimci-nesneler/giyim/tisort", "13-15-fidan", 13, "D4", "Bu tişörtü dün aldım ama dikişi söküldü.", ["tisort_dikisi_sokulmus", "tisort_sokuk", "tisort_yirtik"], "tisort_tek_001", "Sarı temel tişörtün alt sağ yan dikişi açılır; sökülmüş çizgiler ve beyaz makas paylı dar açıklık aynı tek kâğıt giysiye bağlı kalır. Kaynak rengini belirtmediği için sarı tasarım seçimi."], ["gonullu_araniyor_ilani_001", "Tek gönüllü çağrısı ilanı", "yardimci-nesneler/belgeler/ilan", "13-15-fidan", 15, "D5", "Gönüllü arıyoruz! İlkokul öğrencilerine okuma ve ödev desteği.", ["gonullu_araniyor", "gonullu_ariyoruz", "gonulluluk_ilani"], "afis_tek_001", "Tek kâğıt ilanda kaynağın gönüllü çağrısı ve ilkokul öğrencilerine okuma/ödev desteği yazısı; iletişim bilgisi veya gerçek başvuru ilanı değil."], ["gonulluluk_belgesi_ornek_001", "Tek örnek gönüllülük belgesi", "yardimci-nesneler/belgeler/gonulluluk-belgesi", "13-15-fidan", 15, "D3", "gönüllülük belgesi", ["gonulluluk_belgesi", "gonullu_sertifikasi"], null, "Tek kâğıtta GÖNÜLLÜLÜK BELGESİ / ÖRNEK; Ad ve Tarih alanları boş. İmza, mühür, kurum, gerçek kişisel bilgi veya verilmiş resmî belge iddiası yok."]]')
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/fidan_13_15_sekiz_kaniti.json'
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
