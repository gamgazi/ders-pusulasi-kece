"""Reconcile seven puzzle, season, switch, blank-paper and bulb states; historical lamp remains held."""
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
specs=json.loads('[["yapboz_tam_001", "Tek tamamlanmış güneşli yapboz tahtası", "yardimci-nesneler/oyun/yapboz", "4-6-orman", 19, "D2", "resim: tam yapboz", ["yapboz_tam", "tam_yapboz", "yapboz_tamamlanmis"], "yapboz_iki_parca_eksik_001", "Mevcut güneşli yapbozun ham çizimi görüldü: üst solda ve alt sağda iki kahverengi eksik yuva var. Bu iki yuva doldurulur; eksik parçalı kayıt korunur."], ["yapboz_bir_parca_eksik_001", "Tek bir parçası eksik güneşli yapboz tahtası", "yardimci-nesneler/oyun/yapboz", "4-6-orman", 19, "D2", "Bir parçası eksik yapboza dokun!", ["yapboz_bir_parca_eksik", "yapboz_tek_parca_eksik", "yapboz_1_parca_eksik"], "yapboz_iki_parca_eksik_001", "Kaynak bir eksik parça diyor; mevcut iki eksik parçalı yapboz eşdeğer değil. Yalnız alt sağ yuva tamamlanır, üst sol kahverengi yuva kalır."], ["yapboz_iki_parcali_tam_001", "Tek iki parçadan oluşan tamamlanmış yapboz", "yardimci-nesneler/oyun/yapboz", "4-6-orman", 6, "D1", "resim: iki parçalı yapboz", ["yapboz_iki_parcali_tam", "yapboz_iki_parcali", "yapboz_2_parcali"], "", "İki parçalı kolay yapboz, iki parçası eksik çok parçalı yapboz değildir. Tek taşıyıcı üzerinde bitişik iki parça; ayrı iki obje PNGsi yapılmaz."], ["mevsim_dongusu_cember_001", "Tek dört mevsim döngüsü çember posteri", "yardimci-nesneler/egitim/poster", "4-6-cinar", 7, "D1", "resim: dört mevsim çemberi", ["mevsim_dongusu", "mevsim_cemberi", "dort_mevsim_cember", "mevsimler_cember"], "", "Dört mevsim döngüsü, mevcut mevsim seçimi sütun grafiğinden farklı tek poster yüzeyidir. Mevsimler saat yönünde ilkbahar-yaz-sonbahar-kış, eşit alanlar nicel süre grafiği değildir."], ["isik_anahtari_kapali_001", "Tek kapalı duvar ışık anahtarı", "yardimci-nesneler/ev/isik-anahtari", "4-6-kok", 10, "D5", "Işığı kapat!", ["isik_anahtari", "duvar_anahtari", "elektrik_anahtari"], "", "Kapı anahtarı ve duvar prizi ışık anahtarı değildir. Kaynaktaki kapatma eylemi için tek rocker duvar anahtarı temsili; ışık/oda görüntüsü eklenmez. Masa lambası tarihsel PNG beklemesindedir, yeniden üretilmez."], ["kagit_duz_bos_001", "Tek düz boş çizim kâğıdı", "yardimci-nesneler/egitim/kagit", "4-6-cinar", 7, "D1", "resim: boş kâğıt", ["kagit_duz_bos", "kagit_bos", "bos_kagit", "kagit_yeni"], "", "Boş düz yaprak mevcut katlanmış kâğıt veya renkli kartonla aynı durum değildir. Nesne doğal olarak yazısız; yüzeyde çok açık krem geniş keçeli kalem izi, düzensiz beyaz kenar ve küçük kıvrım korunur."], ["ampul_yanan_001", "Tek yanan ampul çizimi", "yardimci-nesneler/ev/ampul", "4-6-kok", 10, "D5", "Işığı aç!", ["ampul_yanan", "ampul_acik", "yanan_ampul"], "ampul_sonuk_001", "Mevcut sönük ampul ham çizimi görüldü: açık mavi cam, gri spiral taban, gri tel, sağ alt kıvrım. Yanan poz sarı/turuncu yoğun mürekkeple yalnız ampul yüzeyinde; dış ışık halesi yok. Masa lambası kopyalanmaz."]]')
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/oyun_isik_yedi_kaniti.json'
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
