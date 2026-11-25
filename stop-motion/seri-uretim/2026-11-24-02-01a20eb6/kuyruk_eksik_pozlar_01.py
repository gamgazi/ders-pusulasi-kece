"""Append missing curriculum-supported poses, preserving and linking original assets."""
import json,pathlib,hashlib,subprocess,unicodedata,re
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
specs=[
  [
    "balon_mavi_patlamis_001",
    "Mavi balonun patlamış tek parça pozu",
    "oyuncak/balon",
    "4-6-agac",
    8,
    "D4",
    "Üzüldüm, çünkü balonum patladı.",
    [
      "balon_mavi_patlamis"
    ],
    "balon_mavi_saglam_001"
  ],
  [
    "balon_mavi_sonuk_001",
    "Mavi balonun havası boşalmış pozu",
    "oyuncak/balon",
    "7-9-orman",
    4,
    "D6",
    "Eylül bir balonu şişirdi, sonra havasını boşalttı.",
    [
      "balon_mavi_sonuk"
    ],
    "balon_mavi_saglam_001"
  ],
  [
    "zarf_acik_001",
    "Zarfın boş açık kapak pozu",
    "kirtasiye/zarf",
    "7-9-filiz",
    11,
    "D4",
    "resim: zarf açan çocuk",
    [
      "zarf_acik"
    ],
    "zarf_kapali_001"
  ],
  [
    "buzdolabi_acik_001",
    "Buzdolabının boş açık kapak pozu",
    "mutfak/buzdolabi",
    "4-6-agac",
    3,
    "D6",
    "yeni dondurmasını hemen buzdolabına koydu.",
    [
      "buzdolabi_acik"
    ],
    "buzdolabi_kapali_001"
  ],
  [
    "kalem_kursun_kirik_001",
    "Kurşun kalemin kırık uç pozu",
    "kirtasiye/kalem",
    "4-6-kok",
    15,
    "D6",
    "kalemin ucu kırık",
    [
      "kalem_kursun_kirik"
    ],
    "kalem_kursun_001"
  ],
  [
    "valiz_acik_bos_001",
    "Valizin boş açık pozu",
    "ulasim/valiz",
    "16-17-kok",
    5,
    "D5",
    "Defne valizini kapattı",
    [
      "valiz_acik"
    ],
    "valiz_kapali_001"
  ]
]
q=read(ROOT/'uretim_kuyrugu.json');oldids={x['id'] for x in q['items']}
proof=ROOT/'denetim/eksik_pozlar_01_kuyruk_kaniti.json'
if all(s[0] in oldids for s in specs):
    print(json.dumps({'already_appended':True,'proof_preserved':proof.exists()}));raise SystemExit(0)
sources={}
for tag in {s[3] for s in specs}:
    rel='pusula/ders-pusulasi/'+tag+'.json';raw=(BASE/'work/source'/rel).read_bytes()
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    expected=subprocess.check_output(['git','rev-parse','HEAD:'+rel],cwd=REPO,text=True).strip()
    assert blob==expected,rel
    sources[tag]=(rel,blob,json.loads(raw))
h=read(ROOT/'denetim/uretim_kayitlari_eslestirme.json');seen={x['record'] for x in h};canonical_records={}
for f in (REPO/'stop-motion/uretim-kayitlari').glob('*.json'):
    j=read(f);rel=f.relative_to(REPO).as_posix()
    if j.get('final_accepted'):
        assert sha(REPO/'stop-motion'/j['final_path'])==j['metrics']['sha256']
        canonical_records[j['id']]=j
    if rel not in seen:
        assert j.get('final_accepted') and j['id'] in canonical_records
        h.append({'record':rel,'asset_name':j['id'],'declared_final_sha256':j['metrics']['sha256'],'historical_status':j['status'],'binary_revalidated_this_session':True});seen.add(rel)
canonical=[p.relative_to(REPO).as_posix() for p in (REPO/'stop-motion').rglob('*.png') if 'seri-uretim' not in p.parts]
new=[]
for aid,title,unused_cat,tag,un,ln,term,aliases,baseid in specs:
    if aid in oldids:continue
    rel,blob,s=sources[tag];ui=next(i for i,u in enumerate(s['uniteler']) if u['no']==un);u=s['uniteler'][ui]
    di=next(i for i,d in enumerate(u['dersler']) if d['kod']==ln);d=u['dersler'][di]
    hits=[(p,v) for p,v in leaves(d) if isinstance(v,str) and term in v];assert hits,aid
    pointer,value=hits[0]
    historical=[x['record'] for x in h if any(matches(a,x.get('asset_name','')+' '+x['record']) for a in aliases)]
    existing=[x['id'] for x in q['items']+new if any(matches(a,x['id']) for a in aliases)]
    files=[x for x in canonical if any(matches(a,x) for a in aliases)]
    assert not historical and not existing and not files,(aid,historical,existing,files)
    b=canonical_records[baseid];png=REPO/'stop-motion'/b['final_path']
    reference={'base_id':baseid,'base_revision':b['revision'],'canonical_png':'stop-motion/'+b['final_path'],'sha256':sha(png),'base_preserved':True}
    # Native original reference is preferred to avoid shrinking an already padded 4K canvas.
    srcsha=b.get('technical_processing',{}).get('source_sha256')
    if b.get('batch_path'):
        for f in (REPO/b['batch_path']/'adaylar'/baseid).glob('*/qa.json'):
            r=read(f)
            if r.get('metrics',{}).get('sha256')==srcsha:
                rp=REPO/b['batch_path']/r['candidate_path'];assert sha(rp)==srcsha
                reference.update(native_reference_png=rp.relative_to(REPO).as_posix(),native_reference_sha256=srcsha)
    new.append({'id':aid,'title':title,'category':pathlib.PurePosixPath(b['final_path']).parent.as_posix(),'state':'READY_MISSING_IN_RECORDS','source_evidence':[{'source':rel,'source_blob_sha':blob,'unit':un,'unit_title':u['ad'],'lesson':ln,'evidence':term,'json_pointer':f'/uniteler/{ui}/dersler/{di}'+pointer,'match':'substring_of_exact_json_leaf','leaf_sha256':hashlib.sha256(value.encode()).hexdigest()}],'felt_cards_preserved':b.get('felt_cards_preserved',[]),'role':'missing state of existing paper helper; base asset remains canonical','historical_name_matches':historical,'dedup_aliases':aliases,'dedup_scope':f'{len(h)} records, {len(canonical)} canonical PNGs, {len(q["items"])} queue items','source_is_action_inference':True,'pose_reference':reference,'semantic_review':'Seçili dersin tam mevcut alanı okundu. Balonun patlaması ve havasının boşalması iki ayrı durumdur; her PNG tek bağlı balon parçası içerir, dağılmış parça kolajı yapılmaz. Açık zarf ders görselindeki açma eyleminden; boş açık buzdolabı nesne koyma eyleminden; kırık kalem ucu doğrudan hikâyeden; açık valiz kapatma eyleminin önceki durumundan çıkarılır. Ana nesnenin renk, tasarım ve yönü gerçek kaynak PNG referansıyla korunur. Kaynakta bulunan başka kişiler/nesneler eklenmez. Kapaklar nesneye bağlı kalır. Mevcut sağlam/kapalı PNG yeniden üretilmez ve üzerine yazılmaz. Bu kayıt poz ihtiyacını doğrular; pozun sanatsal kabulü veya animasyon hizası henüz doğrulanmış değildir. Her üretim sonrası ayrı QA gerekir. Tüm müfredat ve poz ayrıştırması bitmedi.'})
q['items'].extend(new);write(ROOT/'uretim_kuyrugu.json',q);write(ROOT/'denetim/uretim_kayitlari_eslestirme.json',h)
state=read(ROOT/'DEVAM_KAYDI.json');state['ready_verified_items']=len(q['items']);write(ROOT/'DEVAM_KAYDI.json',state)
write(proof,{'new_ids':[x['id'] for x in new],'sources_sha_verified':{k:v[1] for k,v in sources.items()},'base_references':[x['pose_reference'] for x in new],'historical_records_compared':len(h),'canonical_pngs_compared':len(canonical),'existing_queue_preserved':len(oldids),'total_queue':len(q['items']),'complete_curriculum_decomposition':False})
print(json.dumps({'appended':len(new),'total_queue':len(q['items']),'records':len(h),'pngs':len(canonical)}))
