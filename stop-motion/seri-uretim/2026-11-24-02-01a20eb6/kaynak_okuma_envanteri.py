"""Validate existing human-read records against source bytes; never infer semantic completion."""
import json,pathlib,hashlib,subprocess,collections
R=pathlib.Path(__file__).resolve().parent;B=R.parent.parent;REPO=B/'work/repository'
def read(p):return json.loads(p.read_text(encoding='utf8'))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
proofs={}
for p in (R/'denetim').glob('*tam_okuma*.json'):
    j=read(p)
    if j.get('all_present_fields_read') is True and isinstance(j.get('source'),str):
        proofs[j['source']]=(p,j)
assert len(proofs)==35,len(proofs)
q=read(R/'uretim_kuyrugu.json');accepted={x['id']:x for x in read(R/'ilerleme_manifesti.json')['assets'] if x['status']=='FINAL_ACCEPTED'}
mapping=collections.defaultdict(set)
for a in q['items']:
    for e in a.get('source_evidence',[]):
        if 'source' in e and 'unit' in e and 'lesson' in e:mapping[(e['source'],e['unit'],e['lesson'])].add(a['id'])
out=[];total_units=0;total_lessons=0;linked_lessons=0
for source,(p,proof) in sorted(proofs.items()):
    f=B/'work/source'/source;raw=f.read_bytes();s=json.loads(raw);digest=sha(f)
    assert digest==proof.get('source_sha256',proof.get('sha256')),source
    blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    assert blob==subprocess.check_output(['git','rev-parse','HEAD:'+source],cwd=REPO,text=True).strip(),source
    units=[u['no'] for u in s['uniteler']];lessons=sum(len(u['dersler']) for u in s['uniteler'])
    assert units==proof.get('units_read',proof.get('units')),source
    assert lessons==proof.get('lessons_read',proof.get('lesson_count')),source
    rows=[]
    for u in s['uniteler']:
        for d in u['dersler']:
            ids=sorted(mapping[(source,u['no'],d['kod'])]);linked_lessons+=bool(ids)
            rows.append({'unit':u['no'],'lesson':d['kod'],'all_present_fields_read':True,'explicit_queue_links':ids,'linked_final_accepted_ids':[a for a in ids if a in accepted],'all_scene_requirements_reconciled':False})
    total_units+=len(units);total_lessons+=lessons
    out.append({'source':source,'source_sha256':digest,'git_blob_sha':blob,'read_proof':p.relative_to(R).as_posix(),'read_proof_sha256':sha(p),'unit_count':len(units),'lesson_count':lessons,'lessons':rows})
assert total_units==616 and total_lessons==5040,(total_units,total_lessons)
summary={'full_source_files_read':35,'units_read':total_units,'lessons_read':total_lessons,'explicitly_linked_lessons':linked_lessons,'full_curriculum_decomposition_complete':False,'library_complete':False,'note':'Okuma kayıtları kaynak SHA ve tam ünite/ders sayılarıyla doğrulandı. Açık kuyruk bağlantısı olmayan ders eksik asset demek değildir; R/K, ortam, tekrar kullanım veya henüz ayrıştırılmamış içerik olabilir. Bağlantı bulunan ders de tüm sahne gereksinimleri tamamlanmış sayılmaz.','sources':out}
(R/'denetim/tum_kaynaklar_okuma_ve_eslesme_manifesti.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({k:v for k,v in summary.items() if k not in ['note','sources']},ensure_ascii=False))
