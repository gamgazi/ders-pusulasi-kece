"""Append verified 4-6 Cinar and 7-9 Orman object queue after record/file reconciliation."""
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
    "anahtar_tek_001",
    "Tek kapı anahtarı",
    "ev/anahtar",
    "4-6-cinar",
    2,
    "D4",
    "anahtar",
    [
      "anahtar"
    ]
  ],
  [
    "tahta_parcasi_001",
    "Tek ahşap tahta parçası",
    "bilim/tahta",
    "4-6-cinar",
    5,
    "D3",
    "tahta",
    [
      "tahta_parcasi"
    ]
  ],
  [
    "atas_tek_001",
    "Tek ataş",
    "kirtasiye/atas",
    "4-6-cinar",
    5,
    "D4",
    "ataş",
    [
      "atas"
    ]
  ],
  [
    "tuz_paketi_kapali_001",
    "Tek kapalı tuz paketi",
    "yiyecek/tuz",
    "4-6-cinar",
    5,
    "D5",
    "tuz",
    [
      "tuz"
    ]
  ],
  [
    "kum_yigini_001",
    "Tek bitişik kum yığını",
    "doga/kum-yigini",
    "4-6-cinar",
    5,
    "D5",
    "kum",
    [
      "kum_yigini"
    ]
  ],
  [
    "durbin_tek_001",
    "Tek dürbün",
    "bilim/durbin",
    "4-6-cinar",
    10,
    "D3",
    "dürbün",
    [
      "durbin"
    ]
  ],
  [
    "misket_tek_001",
    "Tek misket",
    "oyun/misket",
    "4-6-cinar",
    11,
    "D5",
    "misket",
    [
      "misket"
    ]
  ],
  [
    "televizyon_tek_001",
    "Tek televizyon",
    "teknoloji/televizyon",
    "4-6-cinar",
    11,
    "D5",
    "televizyon",
    [
      "televizyon"
    ]
  ],
  [
    "bayrak_tek_001",
    "Tek oyun bayrağı",
    "oyun/bayrak",
    "4-6-cinar",
    13,
    "D3",
    "bayrak",
    [
      "bayrak"
    ]
  ],
  [
    "madalya_tek_001",
    "Tek kurdeleli madalya",
    "oyun/madalya",
    "4-6-cinar",
    13,
    "D5",
    "madalya",
    [
      "madalya"
    ]
  ],
  [
    "cingirak_tek_001",
    "Tek halka bebek çıngırağı",
    "oyun/cingirak",
    "4-6-cinar",
    17,
    "D1",
    "çıngırak",
    [
      "cingirak"
    ]
  ],
  [
    "gunes_kremi_kapali_001",
    "Tek kapalı güneş kremi",
    "bakim/gunes-kremi",
    "4-6-cinar",
    18,
    "D4",
    "güneş kremi",
    [
      "gunes_kremi"
    ]
  ],
  [
    "sarj_aleti_001",
    "Tek kablolu şarj aleti",
    "teknoloji/sarj-aleti",
    "7-9-orman",
    7,
    "D3",
    "şarj aleti",
    [
      "sarj_aleti"
    ]
  ],
  [
    "gunes_paneli_001",
    "Tek güneş paneli",
    "teknoloji/gunes-paneli",
    "7-9-orman",
    7,
    "D3",
    "güneş paneli",
    [
      "gunes_paneli"
    ]
  ],
  [
    "turk_kahvesi_fincani_001",
    "Tek Türk kahvesi fincanı",
    "yiyecek/turk-kahvesi",
    "7-9-orman",
    8,
    "D3",
    "Türk kahvesi",
    [
      "turk_kahvesi"
    ]
  ],
  [
    "asure_kasesi_001",
    "Tek aşure kasesi",
    "yiyecek/asure",
    "7-9-orman",
    8,
    "D4",
    "aşure",
    [
      "asure"
    ]
  ],
  [
    "pet_sise_kapali_001",
    "Tek kapalı PET şişe",
    "ev/pet-sise",
    "7-9-orman",
    11,
    "D3",
    "pet şişe",
    [
      "pet_sise",
      "plastik_sise"
    ]
  ],
  [
    "pipet_tek_001",
    "Tek plastik pipet",
    "ev/pipet",
    "7-9-orman",
    11,
    "D3",
    "plastik pipet",
    [
      "pipet"
    ]
  ],
  [
    "astronot_yemegi_paket_001",
    "Tek kapalı astronot yemeği paketi",
    "uzay/astronot-yemegi",
    "7-9-orman",
    12,
    "D3",
    "astronot yemeği",
    [
      "astronot_yemegi"
    ]
  ],
  [
    "bagis_kutusu_kapali_001",
    "Tek kapalı bağış kutusu",
    "ev/bagis-kutusu",
    "7-9-orman",
    14,
    "D3",
    "bağış kutusu",
    [
      "bagis_kutusu"
    ]
  ],
  [
    "alisveris_listesi_001",
    "Tek alışveriş listesi",
    "kirtasiye/alisveris-listesi",
    "7-9-orman",
    17,
    "D3",
    "alışveriş listesi",
    [
      "alisveris_listesi"
    ]
  ],
  [
    "pompa_el_001",
    "Tek el hava pompası",
    "alet/pompa",
    "7-9-orman",
    4,
    "D3",
    "pompa",
    [
      "pompa"
    ]
  ],
  [
    "kardelen_tek_001",
    "Tek kardelen çiçeği",
    "doga/kardelen",
    "4-6-cinar",
    7,
    "D3",
    "kardelen",
    [
      "kardelen"
    ]
  ],
  [
    "koza_tek_001",
    "Tek kelebek pupası",
    "doga/koza",
    "4-6-cinar",
    7,
    "D5",
    "koza",
    [
      "koza",
      "pupa"
    ]
  ]
]
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/orman_cinar_ikinci_kuyruk_kaniti.json'
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
    new.append({'id':aid,'title':title,'category':'yardimci-nesneler/'+cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':SOURCE,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+locs[0]}],'felt_cards_preserved':[c['id'] for c in cards if matches(norm(term),c['ad'])],'role':'independent paper helper; existing felt cards remain canonical','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} canonical records, {len(canonical)} canonical PNGs, and {len(q["items"])} live queue items','source_is_action_inference':False,'semantic_review':"Kaynak sözcük ve JSON konumu birebir doğrulandı. Tahta küçük düz ahşap parçasıdır; sınıf tahtası ve odun tekrarı değildir. Kum tek bitişik yığın, mevcut kum havuzu ve kumdan kaleden farklıdır. Tuz ve astronot yemeği tek paketle temsil edilir; ambalaj tasarımı kaynağın sözü değil tasarım kararıdır. Bayrak genel oyun bayrağıdır. Çıngırak bebek halkası olarak marakadan ayrılır. Dürbün çift gözlüdür; teleskop değildir. Türk kahvesi küçük fincanda ve aşure taneli kasede; mevcut bitki çayı/çorbayla farklı içeriktedir. PET şişe nervürlü plastik gövde, mevcut cam şişe ve matara farklı nesnelerdir. Bağış kutusu kapalı yarıklı gövde; açık karton/kayıp eşya kutusunun tekrarı değildir. Alışveriş listesi somut alışveriş içeriği taşır; görev listesinden farklıdır. Pompa benzetme dersindeki sözcüğün nesnesidir; anatomi şeması değildir. Kardelen ve koza biçimleri üretim öncesi birincil kaynakla ayrıca denetlenecek. R/K kartlar korunur; tüm müfredat ve poz ayrıştırması bitmedi."})
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blobs_sha_verified':{k:v[1] for k,v in sources.items()},'sources':[v[0] for v in sources.values()],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'historical_records':len(h),'canonical_pngs':len(canonical)}))
