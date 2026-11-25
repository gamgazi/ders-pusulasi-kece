import json,pathlib,hashlib
import numpy as np
from PIL import Image
root=pathlib.Path('outputs/RootsTalks_Seri_Uretim_02')
asset='sutun_grafik_ekran_suresi_001'
src=root/'adaylar'/asset/'r07'/(asset+'_r07.png')
a=np.array(Image.open(src).convert('RGBA'))
navy=(a[:,:,0]<75)&(a[:,:,1]<75)&(a[:,:,2]<150)&(a[:,:,3]>240)
# Native reference visually located: leftmost portion of five axis ticks.
rows=np.flatnonzero(navy[330:750,447:456].mean(axis=1)>.70)+330
runs=np.split(rows,np.where(np.diff(rows)>1)[0]+1)
ticks=[float(np.median(x)) for x in runs if len(x)>=3]
assert len(ticks)==5,ticks
ticks=ticks[::-1]
steps=np.subtract(ticks[:-1],ticks[1:])
mean_step=float(np.mean(steps))
spacing_error=max(abs(steps/mean_step-1))
bar=json.loads((root/'denetim'/(asset+'_r07_sayisal_olcum.json')).read_text(encoding='utf8'))
readings=[(ticks[0]-b['outline_top_y'])/mean_step*10 for b in bar['bars']]
value_errors=[abs(x/b['value']-1) for x,b in zip(readings,bar['bars'])]
result={'id':asset,'revision':'r07','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'method':'Native RGBA navy tick strokes x447:456 y330:750; median contiguous stroke rows, visually located strip. No image changes.','tick_values':[0,10,20,30,40],'tick_y':ticks,'step_px':steps.tolist(),'max_relative_spacing_error':float(spacing_error),'bar_values_from_axis':readings,'relative_bar_value_errors':value_errors,'tolerance':.05,'pass':bool(spacing_error<=.05 and max(value_errors)<=.05),'manual_lettering_and_visual_review_required':True}
(root/'denetim'/(asset+'_r07_eksen_olcumu.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(result,ensure_ascii=False))
raise SystemExit(0 if result['pass'] else 2)
