"""Append verified 10-12 Filiz and Fidan object queue after record/file reconciliation."""
import json,pathlib,hashlib,unicodedata,re,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
BASE=ROOT.parent.parent
REPO=BASE/'work/repository'
SOURCE=None
def read(p):return json.loads(p.read_text(encoding='utf8'))
def write(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
def norm(s):return re.sub('[^a-z0-9]+','_', ''.join(c for c in unicodedata.normalize('NFKD',s.casefold().replace('ı','i')) if not unicodedata.combining(c))).strip('_')
def matches(a,s):return ('_'+a+'_') in ('_'+norm(s)+'_')
def leaves(o,p=''):
    if isinstance(o,dict):
        for k,v in o.items():yield from leaves(v,p+'/'+k)
    elif isinstance(o,list):
        for k,v in enumerate(o):yield from leaves(v,p+'/'+str(k))
    else:yield p,o
specs=[
  [
    "sac_kurutma_makinesi_001",
    "Tek saç kurutma makinesi",
    "ev/sac-kurutma-makinesi",
    "10-12-filiz",
    1,
    "D6",
    "saç kurutma makinesi",
    [
      "sac_kurutma"
    ]
  ],
  [
    "gozluk_koruyucu_001",
    "Tek koruyucu gözlük",
    "bilim/koruyucu-gozluk",
    "10-12-filiz",
    4,
    "D4",
    "koruyucu gözlük",
    [
      "gozluk_koruyucu",
      "koruyucu_gozluk"
    ]
  ],
  [
    "onluk_laboratuvar_001",
    "Tek boş laboratuvar önlüğü",
    "giysi/laboratuvar-onlugu",
    "10-12-filiz",
    4,
    "D4",
    "önlük",
    [
      "onluk_laboratuvar",
      "laboratuvar_onlugu"
    ]
  ],
  [
    "ayakkabi_spor_tek_001",
    "Tek spor ayakkabısı",
    "giysi/spor-ayakkabisi",
    "10-12-filiz",
    4,
    "D6",
    "spor ayakkabısı",
    [
      "ayakkabi_spor",
      "spor_ayakkabisi"
    ]
  ],
  [
    "gazli_icecek_kutu_001",
    "Tek kapalı gazlı içecek kutusu",
    "yiyecek/gazli-icecek",
    "10-12-filiz",
    7,
    "D4",
    "gazlı içecek",
    [
      "gazli_icecek"
    ]
  ],
  [
    "oyun_konsolu_001",
    "Tek el oyun konsolu",
    "teknoloji/oyun-konsolu",
    "10-12-filiz",
    8,
    "D6",
    "oyun konsolu",
    [
      "oyun_konsolu"
    ]
  ],
  [
    "cizgi_roman_kapali_001",
    "Tek kapalı çizgi roman",
    "kirtasiye/cizgi-roman",
    "10-12-filiz",
    9,
    "D6",
    "çizgi roman",
    [
      "cizgi_roman"
    ]
  ],
  [
    "fis_alisveris_001",
    "Tek alışveriş fişi",
    "kirtasiye/alisveris-fisi",
    "10-12-filiz",
    11,
    "D2",
    "fiş",
    [
      "fis_alisveris",
      "alisveris_fisi"
    ]
  ],
  [
    "garanti_belgesi_001",
    "Tek örnek garanti belgesi",
    "kirtasiye/garanti-belgesi",
    "10-12-filiz",
    11,
    "D6",
    "garanti belgesi",
    [
      "garanti_belgesi"
    ]
  ],
  [
    "sapka_parti_001",
    "Tek koni parti şapkası",
    "kutlama/parti-sapkasi",
    "10-12-filiz",
    13,
    "D3",
    "parti şapkaları",
    [
      "sapka_parti",
      "parti_sapkasi"
    ]
  ],
  [
    "bebek_arabasi_bos_001",
    "Tek boş bebek arabası",
    "ev/bebek-arabasi",
    "10-12-filiz",
    15,
    "D4",
    "bebek arabası",
    [
      "bebek_arabasi"
    ]
  ],
  [
    "emzik_tek_001",
    "Tek emzik",
    "ev/emzik",
    "10-12-filiz",
    15,
    "D4",
    "emzik",
    [
      "emzik"
    ]
  ],
  [
    "fotograf_albumu_kapali_001",
    "Tek kapalı fotoğraf albümü",
    "kirtasiye/fotograf-albumu",
    "10-12-filiz",
    15,
    "D6",
    "fotoğraf albümü",
    [
      "fotograf_albumu"
    ]
  ],
  [
    "not_karti_tek_001",
    "Tek sunum not kartı",
    "kirtasiye/not-karti",
    "10-12-filiz",
    16,
    "D6",
    "not kartı",
    [
      "not_karti"
    ]
  ],
  [
    "karton_renkli_tek_001",
    "Tek renkli karton yaprağı",
    "kirtasiye/renkli-karton",
    "10-12-fidan",
    3,
    "D3",
    "renkli karton",
    [
      "karton_renkli",
      "renkli_karton"
    ]
  ],
  [
    "cetvel_tek_001",
    "Tek cetvel",
    "kirtasiye/cetvel",
    "10-12-fidan",
    3,
    "D3",
    "cetvel",
    [
      "cetvel"
    ]
  ],
  [
    "firin_tepsisi_bos_001",
    "Tek boş fırın tepsisi",
    "ev/firin-tepsisi",
    "10-12-fidan",
    3,
    "D4",
    "fırın tepsisi",
    [
      "firin_tepsisi"
    ]
  ],
  [
    "daktilo_tek_001",
    "Tek daktilo",
    "teknoloji/daktilo",
    "10-12-fidan",
    8,
    "D3",
    "daktilo",
    [
      "daktilo"
    ]
  ],
  [
    "plak_tek_001",
    "Tek plak",
    "muzik/plak",
    "10-12-fidan",
    8,
    "D3",
    "plak",
    [
      "plak"
    ]
  ],
  [
    "soba_odun_001",
    "Tek kapalı odun sobası",
    "ev/odun-sobasi",
    "10-12-fidan",
    8,
    "D4",
    "odun sobası",
    [
      "soba_odun",
      "odun_sobasi"
    ]
  ],
  [
    "radyo_tek_001",
    "Tek radyo",
    "teknoloji/radyo",
    "10-12-fidan",
    8,
    "D6",
    "radyo",
    [
      "radyo"
    ]
  ],
  [
    "izin_kagidi_001",
    "Tek örnek gezi izin kâğıdı",
    "kirtasiye/izin-kagidi",
    "10-12-fidan",
    10,
    "D1",
    "izin kâğıdı",
    [
      "izin_kagidi"
    ]
  ],
  [
    "sari_kart_hakem_001",
    "Tek hakem sarı kartı",
    "spor/sari-kart",
    "10-12-fidan",
    11,
    "D4",
    "sarı kart",
    [
      "sari_kart"
    ]
  ],
  [
    "kus_yemi_paketi_001",
    "Tek kapalı kuş yemi paketi",
    "hayvan-bakimi/kus-yemi",
    "10-12-fidan",
    13,
    "D6",
    "kuş yemi",
    [
      "kus_yemi"
    ]
  ]
]
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/filiz_fidan_10_12_kuyruk_kaniti.json'
if all(s[0] in oldids for s in specs):
    print(json.dumps({'already_appended':True,'proof_preserved':proof.exists()}));raise SystemExit(0)
cards=read(BASE/'work/source/kartlar.json')
sources={}
for tag in {s[3] for s in specs}:
    path='pusula/ders-pusulasi/'+tag+'.json'
    raw=(BASE/'work/source'/path).read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    expected=subprocess.check_output(['git','rev-parse','HEAD:'+path],cwd=REPO,text=True).strip()
    assert blob==expected, 'Source Git blob mismatch'
    sources[tag]=(path,blob,json.loads(raw))
h=read(ROOT/'denetim/uretim_kayitlari_eslestirme.json');records={x['record'] for x in h}
for f in (REPO/'stop-motion/uretim-kayitlari').glob('*.json'):
    rel=f.relative_to(REPO).as_posix()
    if rel in records:continue
    j=read(f);p=REPO/'stop-motion'/j['final_path']
    valid=p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==j['metrics']['sha256']
    assert valid,'Canonical binary missing or changed: '+rel
    h.append({'record':rel,'asset_name':j['id'],'declared_final_sha256':j['metrics']['sha256'],'historical_status':j['status'],'binary_revalidated_this_session':valid});records.add(rel)
canonical=[p.relative_to(REPO).as_posix() for p in (REPO/'stop-motion').rglob('*.png') if 'seri-uretim' not in p.parts]
new=[]
for aid,title,cat,tag,un,ln,term,aliases in specs:
    SOURCE,blob,source=sources[tag]
    if aid in oldids:continue
    ui=next(i for i,u in enumerate(source['uniteler']) if u['no']==un);u=source['uniteler'][ui]
    di=next(i for i,d in enumerate(u['dersler']) if d['kod']==ln);d=u['dersler'][di]
    locs=[p for p,v in leaves(d) if v==term];assert locs,aid+' missing source evidence'
    historical=[x['record'] for x in h if any(matches(a,x.get('asset_name','')+' '+x['record']) for a in aliases)]
    existing=[x['id'] for x in q['items']+new if any(matches(a,x['id']) for a in aliases)]
    files=[x for x in canonical if any(matches(a,x) for a in aliases)]
    assert not historical and not existing and not files, (aid,historical,existing,files)
    new.append({'id':aid,'title':title,'category':'yardimci-nesneler/'+cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':SOURCE,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+locs[0]}],'felt_cards_preserved':[c['id'] for c in cards if matches(norm(term),c['ad'])],'role':'independent paper helper; existing felt cards remain canonical','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} canonical records, {len(canonical)} canonical PNGs, and {len(q["items"])} live queue items','source_is_action_inference':False,'semantic_review':"Kaynak sözcük ve JSON konumu birebir doğrulandı. Laboratuvar önlüğü dersin açık laboratuvar cümlesine dayanır; mutfak önlüğü değildir. Koruyucu gözlük genel temsil; gerçek koruma standardı veya kullanım talimatı değildir. Spor ayakkabısı dans ayakkabısı ve patenden farklıdır. Gazlı içecek kapalı kutu, oyun konsolu düğmeli tek el cihazı olarak temsil edilir; biçimler tasarım kararıdır. Çizgi roman ve fotoğraf albümü mevcut masal/yemek/boyama kitaplarından ayrı işlevli nesnelerdir. Alışveriş fişi, örnek garanti belgesi ve boş gezi izin kağıdı gerçek belge veya hukuki taahhüt içermez. Parti şapkası koni biçimiyle siperli şapkadan farklıdır. Not kartı tek sunum hatırlatma kartı, renkli karton boş tabaka, hakem sarı kartı spor nesnesidir; liste veya joker kartı değildir. Fırın tepsisi düz dikdörtgen kap; tava ve tabaktan farklıdır. Daktilo, plak, odun sobası ve radyo eski teknoloji sözcükleridir; klavye/hoparlör/mangal yerine geçmez. Kuş yemi kapalı paketle temsil edilir; ambalaj kaynağın sözü değil tasarım kararıdır. Bebek arabası boş ve emzik tek nesne; bebek figürü eklenmez. R/K kartlar korunur; tüm müfredat ve poz ayrıştırması bitmedi."})
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blobs_sha_verified':{k:v[1] for k,v in sources.items()},'sources':[v[0] for v in sources.values()],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'historical_records':len(h),'canonical_pngs':len(canonical)}))
