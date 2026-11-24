"""Append exact Fidan source evidence after canonical record/file reconciliation."""
import json,pathlib,hashlib,unicodedata,re,subprocess
ROOT=pathlib.Path(__file__).resolve().parent
BASE=ROOT.parent.parent
REPO=BASE/'work/repository'
SOURCE='pusula/ders-pusulasi/4-6-filiz.json'
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
    "cekmece_bos_001",
    "Boş çekmece",
    "ev/cekmece",
    2,
    "D3",
    "çekmece",
    [
      "cekmece"
    ]
  ],
  [
    "lif_banyo_001",
    "Banyo lifi",
    "bakim/banyo-lifi",
    2,
    "D3",
    "banyo lifi",
    [
      "lif_banyo",
      "banyo_lifi"
    ]
  ],
  [
    "dus_jeli_kapali_001",
    "Kapalı duş jeli tüpü",
    "bakim/dus-jeli",
    2,
    "D3",
    "duş jeli",
    [
      "dus_jeli"
    ]
  ],
  [
    "sampuan_kapali_001",
    "Kapalı şampuan şişesi",
    "bakim/sampuan",
    2,
    "D3",
    "şampuan",
    [
      "sampuan"
    ]
  ],
  [
    "kaykay_tek_001",
    "Kaykay",
    "oyun/kaykay",
    3,
    "D2",
    "kaykay",
    [
      "kaykay"
    ]
  ],
  [
    "yara_bandi_tek_001",
    "Tek yara bandı",
    "bakim/yara-bandi",
    8,
    "D2",
    "yara bandı",
    [
      "yara_bandi"
    ]
  ],
  [
    "termometre_tek_001",
    "Termometre",
    "bakim/termometre",
    8,
    "D5",
    "termometre",
    [
      "termometre"
    ]
  ],
  [
    "surup_sisesi_001",
    "Kapalı şurup şişesi",
    "bakim/surup",
    8,
    "D7",
    "şurup",
    [
      "surup"
    ]
  ],
  [
    "brokoli_tek_001",
    "Brokoli",
    "yiyecek/brokoli",
    10,
    "D1",
    "brokoli",
    [
      "brokoli"
    ]
  ],
  [
    "catal_tek_001",
    "Tek çatal",
    "mutfak/catal",
    10,
    "D2",
    "çatal",
    [
      "catal"
    ]
  ],
  [
    "kofte_tek_001",
    "Tek köfte",
    "yiyecek/kofte",
    10,
    "D3",
    "köfte",
    [
      "kofte"
    ]
  ],
  [
    "zeytin_tek_001",
    "Tek zeytin",
    "yiyecek/zeytin",
    10,
    "D4",
    "zeytin",
    [
      "zeytin"
    ]
  ],
  [
    "tencere_kapali_001",
    "Kapalı tencere",
    "mutfak/tencere",
    10,
    "D5",
    "tencere",
    [
      "tencere"
    ]
  ],
  [
    "tava_bos_001",
    "Boş tava",
    "mutfak/tava",
    10,
    "D5",
    "tava",
    [
      "tava"
    ]
  ],
  [
    "kek_dilim_001",
    "Kek dilimi",
    "yiyecek/kek",
    10,
    "D5",
    "kek",
    [
      "kek"
    ]
  ],
  [
    "balkabagi_butun_001",
    "Bütün balkabağı",
    "yiyecek/balkabagi",
    11,
    "D3",
    "balkabağı",
    [
      "balkabagi"
    ]
  ],
  [
    "deniz_kabugu_tek_001",
    "Tek deniz kabuğu",
    "doga/deniz-kabugu",
    15,
    "D3",
    "deniz kabuğu",
    [
      "deniz_kabugu"
    ]
  ],
  [
    "can_simidi_001",
    "Can simidi",
    "oyun/can-simidi",
    15,
    "D5",
    "can simidi",
    [
      "can_simidi"
    ]
  ],
  [
    "pusula_tek_001",
    "Pusula",
    "kamp/pusula",
    17,
    "D3",
    "pusula",
    [
      "pusula"
    ]
  ],
  [
    "termos_kapali_001",
    "Kapalı termos",
    "kamp/termos",
    17,
    "D3",
    "termos",
    [
      "termos"
    ]
  ],
  [
    "sirt_cantasi_kapali_001",
    "Kapalı sırt çantası",
    "kamp/sirt-cantasi",
    17,
    "D3",
    "sırt çantası",
    [
      "sirt_cantasi"
    ]
  ],
  [
    "matara_kapali_001",
    "Kapalı matara",
    "kamp/matara",
    17,
    "D3",
    "matara",
    [
      "matara"
    ]
  ],
  [
    "mantar_tek_001",
    "Tek mantar",
    "doga/mantar",
    17,
    "D5",
    "mantar",
    [
      "mantar"
    ]
  ],
  [
    "gitar_tek_001",
    "Akustik gitar",
    "muzik/gitar",
    19,
    "D1",
    "gitar",
    [
      "gitar"
    ]
  ]
]
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/filiz_kuyruk_kaniti.json'
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
    new.append({'id':aid,'title':title,'category':'yardimci-nesneler/'+cat,'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':SOURCE,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+locs[0]}],'felt_cards_preserved':[c['id'] for c in cards if matches(norm(term),c['ad'])],'role':'independent paper helper; existing felt cards remain canonical','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} canonical records, {len(canonical)} canonical PNGs, and {len(q["items"])} live queue items','source_is_action_inference':False,'semantic_review':'Kaynakta nesne sözcüğü birebir doğrulandı. Boş çekmece tek mobilya modülü; mevcut dolap yeniden üretilmez. Duş jeli tüpü, şampuan şişesi, şurup şişesi, termos ve matara işlev ve gövde yapılarıyla ayrılır; yalnız renk varyantı değildir. Kek dilimi kremalı pastadan farklıdır; lif gerçek kumaş olarak değil keçeli kalem kâğıt çizimi olarak üretilir. Can simidi gıda simidinden farklıdır; pusula adında depo başlığıyla yanlış eşleşme önlenir. Tüm ürünler tek nesne, kişisizdir.'})
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'source_blob_sha_verified':blob,'source':SOURCE,'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'historical_records':len(h),'canonical_pngs':len(canonical)}))
