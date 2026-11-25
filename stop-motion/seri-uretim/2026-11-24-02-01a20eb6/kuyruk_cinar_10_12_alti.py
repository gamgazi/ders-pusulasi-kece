"""Reconcile six specific objects after full Cinar reading and reference inspection."""
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
specs=json.loads('[["vazo_catlak_001", "Tek çatlak bütün vazo", "yardimci-nesneler/ev/vazo", "10-12-cinar", 16, "D5", "çatlak bir vazoyu", ["vazo_catlak", "catlak_vazo"], "vazo_bos_001", "Mevcut mavi/turkuaz vazonun dış biçimi ve ağzı bütündür; gövde üzerinde tek ince düzensiz lacivert çatlak çizgisi. Mevcut vazo_kirik_001 ağzı/omzu eksilmiş farklı durumu gösterir. Ayrı kırık parça veya delik yok."], ["kullanim_kilavuzu_001", "Tek kullanım kılavuzu kitapçığı", "yardimci-nesneler/belgeler/kullanim-kilavuzu", "10-12-cinar", 8, "D2", "Bir cihazın nasıl kullanılacağını anlatan kitapçık", ["kullanim_kilavuzu", "kilavuz_kitapcigi", "cihaz_kilavuzu"], "masal_kitabi_kapali_001", "Tek ince kapalı kırmızı kitapçık; kapağında KULLANIM KILAVUZU ve küçük dişli çizimi. Mevcut masal kitabı korunur; yönerge/cihaz güvenliği metni veya gerçek kullanım talimatı uydurulmaz."], ["muze_kurallari_levhasi_001", "Tek örnek müze kuralları levhası", "yardimci-nesneler/belgeler/muze-kurallari", "10-12-cinar", 8, "D5", "Müzemiz pazartesi günleri ziyarete kapalıdır.", ["muze_kurallari", "muze_uyari", "muze_tabela", "muze_pazartesi_kapali"], "gorev_listesi_001", "Dersin kurgusal müze tabelası tek kâğıt nesne: MÜZE KURALLARI / Pazartesi kapalı. / Flaş kullanmayın. / Eserlere dokunmayın. Aynı derste üç kural açıkça var. Gerçek müzenin güncel kuralları iddiası değil; tek levhada okunaklı üç satır, ek nesne yok."], ["heykel_anne_bebek_001", "Tek anne ve bebeğini betimleyen heykel", "yardimci-nesneler/sanat/heykel", "10-12-cinar", 9, "D5", "Bir anne bebeğine sarılmıştı.", ["heykel_anne_bebek", "anne_bebek_heykeli", "annelik_heykeli"], "heykel_tek_001", "Tek kaideli bütün heykel; anne ve sarıldığı küçük bebeği tek yekpare turuncu heykel yüzeyinde betimlenir, bağlı mavi kaide. İki ayrı karakter kesiti değil. Mevcut soyut S biçimi bu betimlemeyi karşılamıyor; R/K figür kartları üretilmez."], ["tablo_denizde_kayik_001", "Tek karanlık deniz ve kayık resmi", "yardimci-nesneler/sanat/tablo", "10-12-cinar", 9, "D5", "karanlık bir deniz ve uzakta tek bir kayık", ["tablo_denizde_kayik", "kayikli_deniz_resmi", "karanlik_deniz_resmi"], "kartpostal_manzarali_on_001", "Tek yatay sanat resmi kâğıdının yüzeyinde karanlık deniz ve uzakta yalnız bir küçük kayık çizimi. Deniz/kayık ayrı fiziksel PNG nesneleri değil aynı sanat eserinin içeriği; onaylı arka plan ve tarihi kayık dosyası tekrar üretilmez."], ["tablo_kirmizi_lale_001", "Tek mavi mor zeminli kırmızı lale resmi", "yardimci-nesneler/sanat/tablo", "10-12-cinar", 9, "D8", "Eserde mavi ve mor renkler var. Ortada kırmızı bir lale.", ["tablo_kirmizi_lale", "lale_resmi", "mavi_mor_lale_tablosu"], "kartpostal_manzarali_on_001", "Tek kâğıt sanat eseri: mavi-mor boyalı yüzeyin ortasında bir kırmızı lale çizimi. Beyaz kâğıt makas payı ve kıvrım korunur; saksı/vazo veya bağımsız lale parçası yok. Tarihi lale varlığı yerine geçen yeniden üretim değil dersin resim nesnesi."]]')
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/cinar_10_12_alti_kaniti.json'
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
    if aid.startswith('tablo_'):cat='yardimci-nesneler/sanat/tablo'
    if aid=='kullanim_kilavuzu_001':cat='yardimci-nesneler/belgeler/kullanim-kilavuzu'
    if aid=='muze_kurallari_levhasi_001':cat='yardimci-nesneler/belgeler/muze-kurallari'
    item={'id':aid,'title':title,'category':cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':rel,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+pointer,'match':'exact_json_leaf' if value==term else 'substring_of_exact_json_leaf','leaf_sha256':hashlib.sha256(value.encode()).hexdigest()}],'felt_cards_preserved':cardids,'role':'missing pose of existing paper helper' if baseid else 'independent missing paper helper','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} records, {len(canonical)} canonical PNGs, {len(q["items"])} queue items','source_is_action_inference':True,'semantic_review':semantic+' Seçilen tam mevcut ders alanı okundu. Mevcut R/K kartlar ve temel yardımcı nesne dosyaları korunur. Üretim sonrası her PNG için ayrı teknik ve üç görünümde sanatsal QA gerekir; poz hizası/animasyon henüz doğrulanmış değildir. Tüm müfredat ayrıştırması bitmedi.'}
    if reference:item['pose_reference']=reference
    new.append(item)
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blobs_sha_verified':{k:v[1] for k,v in sources.items()},'base_references':[x['pose_reference'] for x in new if 'pose_reference' in x],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'records':len(h),'pngs':len(canonical)}))
