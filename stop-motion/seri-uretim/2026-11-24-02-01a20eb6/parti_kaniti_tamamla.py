"""Close only an already individually reviewed batch, never grant artistic acceptance."""
import hashlib,json,pathlib,sys
R=pathlib.Path(__file__).resolve().parent
p=R/'denetim'/sys.argv[1]
j=json.loads(p.read_text(encoding='utf8'))
q=json.loads((R/'uretim_kuyrugu.json').read_text(encoding='utf8'))
byid={x['id']:x for x in q['items']};accepted=[]
for aid in j['new_ids']:
    i=byid[aid];assert i['state']=='FINAL_ACCEPTED',aid
    rev=i['accepted_revision'];qa=json.loads((R/'adaylar'/aid/rev/'qa.json').read_text(encoding='utf8'))
    assert qa['final_accepted'] and qa['status']=='FINAL_ACCEPTED',aid
    final=R/i['category']/(aid+'.png')
    sh=hashlib.sha256(final.read_bytes()).hexdigest()
    assert sh==i['final_sha256']==qa['metrics']['sha256'],aid
    accepted.append({'id':aid,'revision':rev,'sha256':sh})
j.update(accepted_after_visual_review=accepted,selected_batch_complete=True,
    local_total_accepted_after_batch=sum(x['state']=='FINAL_ACCEPTED' for x in q['items'])+6,
    library_complete=False,native_4k_detail_claim=False,animation_pose_alignment_verified=False)
p.write_text(json.dumps(j,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps({'batch_verified':len(accepted),'total_accepted':j['local_total_accepted_after_batch']}))
