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
specs=json.loads("[[\"rende_tek_001\",\"Tek mutfak rendesi\",\"yardimci-nesneler/mutfak/rende\",\"10-12-kok\",2,\"D3\",\"rendele\",[\"rende\",\"rende_tek\"],null,\"Rendele eyleminden araç gereksinimi çıkarımı; kaynakta rende adı değil fiil var. Tek düz el rendesi: turuncu bağlı tutamak, gri metal yüzeyde küçük çizili delik/diş işaretleri. Delikler kâğıt üzeri opak resim; yalnız tutamak iç açıklığı gerçek alfa. Yiyecek veya ayrı parça yok.\"],[\"klozet_kapali_001\",\"Tek kapalı klozet\",\"yardimci-nesneler/ev/klozet\",\"10-12-kok\",3,\"D3\",\"klozet\",[\"klozet\"],null,\"Tek kapalı kapaklı krem klozet; bağlı rezervuar, küçük sifon düğmesi, kapalı oval kapak ve kaide. Banyo arka planı, insan, tuvalet kâğıdı yok. Beyaz yüzey opak çizilmiş kâğıt.\"],[\"kumanda_televizyon_001\",\"Tek televizyon kumandası\",\"yardimci-nesneler/teknoloji/kumanda\",\"10-12-kok\",3,\"D6\",\"kumanda\",[\"kumanda\"],null,\"Tek uzun mavi televizyon kumandası, üstte kırmızı güç düğmesi, merkezde yön halkası, altta küçük düğmeler. Oyun kolu/telefon değil; ekran, marka, sayılar veya televizyon yok.\"],[\"ayakkabilik_bos_001\",\"Tek boş ayakkabılık\",\"yardimci-nesneler/ev/ayakkabilik\",\"10-12-kok\",3,\"D6\",\"ayakkabılık\",[\"ayakkabilik\"],null,\"Tek alçak iki katlı açık ayakkabılık; turuncu ahşap yan dikmeler ve iki mavi geniş ayakkabı rafı, boş. Genel duvar rafından ayrı ayaklı alçak eşya. Aralıklar gerçek alfa, iç kenarlar beyaz makas paylı; ayakkabı yok.\"],[\"kemer_giysi_001\",\"Tek giysi kemeri\",\"yardimci-nesneler/giyim/kemer\",\"10-12-kok\",6,\"D6\",\"kemer\",[\"kemer_giysi\",\"giysi_kemeri\",\"bel_kemeri\"],null,\"Tek kahverengi giysi kemeri yumuşak açık kıvrımda; bağlı gri dikdörtgen toka ve kısa toka dili, sivri uçta delik işaretleri. Emniyet kemerinden farklı bel giysisi. İnsan veya pantolon yok.\"],[\"esofman_alti_001\",\"Tek eşofman altı\",\"yardimci-nesneler/giyim/esofman\",\"10-12-kok\",6,\"D6\",\"eşofman\",[\"esofman\"],null,\"Kaynak eşofman sözcüğü tek parça eşofman altı ile temsil edilir; takımın ikinci giysisi yok. Mavi bel lastikli uzun spor pantolon, iki paça ve yanlarda beyaz çizgi; kumaş/örgü değil yoğun marker kâğıt resmi.\"],[\"polis_arabasi_yandan_001\",\"Tek polis arabası\",\"yardimci-nesneler/ulasim/polis-arabasi\",\"10-12-kok\",7,\"D2\",\"polis arabası\",[\"polis_arabasi\",\"polis_araci\"],null,\"Tek beyaz/mavi sedan yandan, iki görünür tekerlek, bağlı kırmızı-mavi tepe lambası ve POLİS yazısı. Genel görev aracı, resmî logo/plaka/kişi/silah yok; taksi ve oyuncak arabasından görev farklı.\"],[\"denizalti_yandan_001\",\"Tek denizaltı\",\"yardimci-nesneler/ulasim/denizalti\",\"10-12-kok\",7,\"D2\",\"denizaltı\",[\"denizalti\"],null,\"Tek sarı basit denizaltı yandan; yuvarlak gövde, üç mavi lomboz, üstte bağlı periskop ve arkada bağlı küçük pervane. Su/baloncuk/insan/silah yok; mühendislik şeması değil genel anlatı aracı.\"],[\"metro_vagon_001\",\"Tek metro vagonu\",\"yardimci-nesneler/ulasim/metro\",\"10-12-kok\",7,\"D4\",\"metro\",[\"metro_vagon\",\"metro\"],null,\"Tek metro sürücü vagonu yandan, kısa ön kabin ve uzun dikdörtgen gövde, sürgülü çift kapı ve mavi camlar, dört küçük tekerlek. Ray/tünel/istasyon veya ikinci vagon yok. METRO yazısı; belirli şehir/model kopyası değil.\"],[\"tramvay_vagon_001\",\"Tek tramvay\",\"yardimci-nesneler/ulasim/tramvay\",\"10-12-kok\",7,\"D4\",\"tramvay\",[\"tramvay\"],null,\"Tek kırmızı krem nostaljik tramvay vagonu; dik ön/arka uç, uzun cam sırası, iki tekerlek grubu ve gövdeye bağlı üst akım kolu. TRAMVAY yazısı. Ray/tel/şehir/kişi/ikinci vagon yok; model kopyası değil.\"],[\"merhem_tupu_kapali_001\",\"Tek kapalı merhem tüpü\",\"yardimci-nesneler/saglik/merhem\",\"10-12-kok\",10,\"D6\",\"merhem\",[\"merhem\"],null,\"Tek kapalı turkuaz tüp, bağlı turuncu vidalı kapak ve MERHEM yazısı. İlaç adı/doz/uygulama/iyileştirme iddiası veya sağlık amblemi yok. Genel ders aksesuarı.\"],[\"toz_bezi_katli_001\",\"Tek katlı toz bezi\",\"yardimci-nesneler/temizlik/toz-bezi\",\"10-12-kok\",13,\"D3\",\"toz bezi\",[\"toz_bezi\"],null,\"Tek katlanmış sarı temizlik bezi, üst üste bağlı kıvrımlar; havlu veya peçeteden renk/biçim/işlev ayrı. Fotoğrafik tekstil değil yoğun keçeli kalem kâğıt resmi; toz bulutu veya el yok.\"],[\"deterjan_sisesi_kapali_001\",\"Tek kapalı deterjan şişesi\",\"yardimci-nesneler/temizlik/deterjan\",\"10-12-kok\",13,\"D3\",\"deterjan\",[\"deterjan\"],null,\"Tek turuncu çamaşır deterjanı şişesi, bağlı mavi vidalı kapak, yanda gövdeye bağlı kavrama deliği ve DETERJAN yazısı. Delik gerçek alfa ve beyaz iç paylı; sıvı/çamaşır/marka/etiket iddiası yok.\"],[\"supurge_el_001\",\"Tek el süpürgesi\",\"yardimci-nesneler/temizlik/supurge\",\"10-12-kok\",13,\"D3\",\"süpürge\",[\"supurge_el\",\"el_supurgesi\",\"calı_supurgesi\"],null,\"Tek uzun saplı kuru yer süpürgesi; turuncu sap, bağlı mavi boyun ve sarı geniş kıllı başlık. Elektrikli süpürgeden ayrı; faraş/toz/elin olmadığı tek nesne. Çizili kıllar tek bağlı kâğıt silüette.\"],[\"elektrik_supurgesi_001\",\"Tek elektrik süpürgesi\",\"yardimci-nesneler/temizlik/elektrik-supurgesi\",\"10-12-kok\",13,\"D7\",\"elektrik süpürgesi\",[\"elektrik_supurgesi\",\"elektrikli_supurge\"],null,\"Tek dik kablosuz elektrikli süpürge; turkuaz sap/gövde, turuncu motor haznesi ve bağlı geniş mavi zemin başlığı. Hortumlu ikinci gövde, gevşek kablo, toz veya kişi yok. Genel model; performans iddiası değil.\"]]")
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/kok_10_12_kuyruk_kaniti.json'
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
    item={'id':aid,'title':title,'category':cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':rel,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+pointer,'match':'exact_json_leaf' if value==term else 'substring_of_exact_json_leaf','leaf_sha256':hashlib.sha256(value.encode()).hexdigest()}],'felt_cards_preserved':cardids,'role':'missing pose of existing paper helper' if baseid else 'independent missing paper helper','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} records, {len(canonical)} canonical PNGs, {len(q["items"])} queue items','source_is_action_inference':aid in {'rende_tek_001'},'semantic_review':semantic+' Seçilen tam mevcut ders alanı okundu. Mevcut R/K kartlar ve temel yardımcı nesne dosyaları korunur. Üretim sonrası her PNG için ayrı teknik ve üç görünümde sanatsal QA gerekir; poz hizası/animasyon henüz doğrulanmış değildir. Tüm müfredat ayrıştırması bitmedi.'}
    if reference:item['pose_reference']=reference
    new.append(item)
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blobs_sha_verified':{k:v[1] for k,v in sources.items()},'base_references':[x['pose_reference'] for x in new if 'pose_reference' in x],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'records':len(h),'pngs':len(canonical)}))
