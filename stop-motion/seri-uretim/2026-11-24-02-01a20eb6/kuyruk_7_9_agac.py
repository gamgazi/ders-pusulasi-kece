"""Append verified 7-9 Ağaç object queue after record/file reconciliation."""
import json,pathlib,hashlib,unicodedata,re,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
BASE=ROOT.parent.parent
REPO=BASE/'work/repository'
SOURCE='pusula/ders-pusulasi/7-9-agac.json'
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
    "saksi_devrilmis_001",
    "Devrilmiş boş saksı pozu",
    "doga/saksi",
    1,
    "D5",
    "Saksı devrilmiş, rüzgâr esmiş.",
    [
      "saksi_devrilmis"
    ]
  ],
  [
    "miknatis_at_nali_001",
    "At nalı mıknatıs",
    "deney/miknatis",
    4,
    "D4",
    "mıknatıs",
    [
      "miknatis"
    ]
  ],
  [
    "civi_tek_001",
    "Tek demir çivi",
    "deney/civi",
    4,
    "D4",
    "Mıknatıs çiviyi çekti, çünkü çivi demirden.",
    [
      "civi"
    ]
  ],
  [
    "mektup_acik_001",
    "Açık mektup kâğıdı",
    "iletisim/mektup",
    7,
    "D1",
    "mektup",
    [
      "mektup"
    ]
  ],
  [
    "zarf_kapali_001",
    "Kapalı zarf",
    "iletisim/zarf",
    7,
    "D3",
    "zarf",
    [
      "zarf"
    ]
  ],
  [
    "pul_tek_001",
    "Tek posta pulu",
    "iletisim/pul",
    7,
    "D3",
    "pul",
    [
      "pul"
    ]
  ],
  [
    "posta_kutusu_001",
    "Posta kutusu",
    "iletisim/posta-kutusu",
    7,
    "D4",
    "posta kutusu",
    [
      "posta_kutusu"
    ]
  ],
  [
    "kartpostal_tek_001",
    "Tek kartpostal",
    "iletisim/kartpostal",
    7,
    "D4",
    "kartpostal",
    [
      "kartpostal"
    ]
  ],
  [
    "piyon_tek_001",
    "Tek oyun piyonu",
    "oyun/piyon",
    9,
    "D1",
    "piyon",
    [
      "piyon"
    ]
  ],
  [
    "joker_karti_tek_001",
    "Tek joker oyun kartı",
    "oyun/joker-karti",
    9,
    "D3",
    "joker",
    [
      "joker"
    ]
  ],
  [
    "oyun_tahtasi_001",
    "Tek oyun tahtası",
    "oyun/oyun-tahtasi",
    9,
    "D5",
    "oyun tahtası",
    [
      "oyun_tahtasi"
    ]
  ],
  [
    "musluk_kapali_001",
    "Kapalı musluk",
    "ev/musluk",
    12,
    "D4",
    "musluk",
    [
      "musluk"
    ]
  ],
  [
    "kus_evi_001",
    "Tek kuş evi",
    "doga/kus-evi",
    12,
    "D5",
    "kuş evi",
    [
      "kus_evi"
    ]
  ],
  [
    "cop_masasi_001",
    "Çöp toplama maşası",
    "temizlik/cop-masasi",
    12,
    "D7",
    "çöp maşası",
    [
      "cop_masasi"
    ]
  ],
  [
    "cop_torbasi_bagli_001",
    "Bağlı çöp torbası",
    "temizlik/cop-torbasi",
    12,
    "D7",
    "çöp torbası",
    [
      "cop_torbasi"
    ]
  ],
  [
    "corap_tek_001",
    "Tek kışlık çorap",
    "giysi/corap",
    13,
    "D3",
    "yünlü çorap",
    [
      "corap"
    ]
  ],
  [
    "ari_kovani_001",
    "Tek arı kovanı",
    "doga/ari-kovani",
    17,
    "D2",
    "kovan",
    [
      "kovan",
      "ari_kovani"
    ]
  ],
  [
    "nar_butun_001",
    "Bütün nar",
    "yiyecek/nar",
    8,
    "D4",
    "Cevabı nar!",
    [
      "nar"
    ]
  ],
  [
    "zamanlayici_001",
    "Mutfak zamanlayıcısı",
    "esya/zamanlayici",
    18,
    "D4",
    "zamanlayıcı",
    [
      "zamanlayici"
    ]
  ],
  [
    "kunefe_dilim_001",
    "Tek künefe dilimi",
    "yiyecek/kunefe",
    19,
    "D2",
    "künefe",
    [
      "kunefe"
    ]
  ],
  [
    "odul_kupasi_001",
    "Ödül kupası",
    "esya/odul-kupasi",
    6,
    "D3",
    "ödül",
    [
      "odul_kupasi"
    ]
  ],
  [
    "afis_tek_001",
    "Tek çevre afişi",
    "okul/afis",
    12,
    "D2",
    "afiş",
    [
      "afis"
    ]
  ],
  [
    "pizza_butun_001",
    "Bütün pizza",
    "yiyecek/pizza",
    15,
    "D1",
    "Bir pizza sipariş etmek istiyorum.",
    [
      "pizza"
    ]
  ],
  [
    "tost_tek_001",
    "Tek tost",
    "yiyecek/tost",
    11,
    "D5",
    "Burada kahvaltıda tost yiyoruz, oysa Türkiye'de simit yiyoruz.",
    [
      "tost"
    ]
  ]
]
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/agac_7_9_kuyruk_kaniti.json'
if all(s[0] in oldids for s in specs):
    print(json.dumps({'already_appended':True,'proof_preserved':proof.exists()}));raise SystemExit(0)
raw=(BASE/'work/source'/SOURCE).read_bytes()
blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
expected=subprocess.check_output(['git','rev-parse','HEAD:'+SOURCE],cwd=REPO,text=True).strip()
assert blob==expected, 'Source Git blob mismatch'
source=json.loads(raw);cards=read(BASE/'work/source/kartlar.json')
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
for aid,title,cat,un,ln,term,aliases in specs:
    if aid in oldids:continue
    ui=next(i for i,u in enumerate(source['uniteler']) if u['no']==un);u=source['uniteler'][ui]
    di=next(i for i,d in enumerate(u['dersler']) if d['kod']==ln);d=u['dersler'][di]
    locs=[p for p,v in leaves(d) if v==term];assert locs,aid+' missing source evidence'
    historical=[x['record'] for x in h if any(matches(a,x.get('asset_name','')+' '+x['record']) for a in aliases)]
    existing=[x['id'] for x in q['items']+new if any(matches(a,x['id']) for a in aliases)]
    files=[x for x in canonical if any(matches(a,x) for a in aliases)]
    assert not historical and not existing and not files, (aid,historical,existing,files)
    new.append({'id':aid,'title':title,'category':'yardimci-nesneler/'+cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':SOURCE,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+locs[0]}],'felt_cards_preserved':[c['id'] for c in cards if matches(norm(term),c['ad'])],'role':'independent paper helper; existing felt cards remain canonical','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} canonical records, {len(canonical)} canonical PNGs, and {len(q["items"])} live queue items','source_is_action_inference':False,'semantic_review':"Kaynak sözcük/cümle birebir doğrulandı. Saksı yeni devrilmiş pozdur: mevcut kabul edilmiş saksı_bos_001 referans alınır; dik poz tekrar üretilmez. Mıknatıs, çivi ve musluk tek bağımsız nesnedir. Ödülün kupa biçimi ve zamanlayıcının mutfak tipi tasarım tercihidir, kaynakta bu alt biçim verilmez. Arı kovanında arı bulunmaz. Çöp torbası bağlı biçimiyle açık market poşetinden ayrılır. Kuş evi, dal yuvasından ayrı kapalı yapı nesnesidir. Oyun tahtası, afiş ve kartlardaki şekiller aynı kâğıdın çizimidir; çok nesneli kolaj üretilmez. Keçe kartlar korunur, ana hedef figürü yerine yardımcı kâğıt üretildiği açık tutulur. Tüm müfredat/poz ayrıştırması henüz tamamlanmadı."})
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blob_sha_verified':blob,'source':SOURCE,'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'historical_records':len(h),'canonical_pngs':len(canonical)}))
