"""Measure rendered bar outlines; does not modify images or grant artistic acceptance."""
import argparse,hashlib,json,pathlib
import numpy as np
from PIL import Image
ROOT=pathlib.Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--id',required=True);p.add_argument('--values',required=True);p.add_argument('--colors',required=True);p.add_argument('--revision',default='r01');p.add_argument('--centers');a=p.parse_args()
src=ROOT/'adaylar'/a.id/a.revision/(a.id+'_'+a.revision+'.png')
im=np.array(Image.open(src).convert('RGBA'));r,g,b,alpha=[im[:,:,i].astype(float) for i in range(4)]
valid=alpha>240
colors={'turquoise':valid&(r<130)&(g>125)&(b>115)&(g>r*1.3),'orange':valid&(r>180)&(g>50)&(g<190)&(b<100),'purple':valid&(r>90)&(r<220)&(g<90)&(b>150),'green':valid&(g>115)&(r<150)&(b<130)&(g>r*1.3),'blue':valid&(b>145)&(r<90)&(g>75)&(g<170)}
navy=valid&(r<75)&(g<75)&(b<150)
bars=[]
centers=list(map(int,a.centers.split(','))) if a.centers else None
for index,(color,value) in enumerate(zip(a.colors.split(','),map(float,a.values.split(',')))):
    mask=colors[color].copy()
    if centers:
        left=0 if index==0 else (centers[index-1]+centers[index])//2
        right=im.shape[1] if index==len(centers)-1 else (centers[index]+centers[index+1])//2
        mask[:,:left]=False;mask[:,right:]=False
    # User-facing chart content is below title and above bottom labels.
    mask[:int(im.shape[0]*.30),:]=False
    mask[int(im.shape[0]*.84):,:]=False
    ys,xs=np.where(mask);assert len(xs)>500,color
    # Hue-specific sparse edge pixels do not set geometry.
    x0,x1=np.quantile(xs,[.01,.99]).round().astype(int);y0,y1=np.quantile(ys,[.005,.995]).round().astype(int)
    cx=int(np.median(xs));half=max(10,int((x1-x0)*.20))
    def line_near(y):
        lo=max(0,y-25);hi=min(im.shape[0],y+26)
        counts=navy[lo:hi,cx-half:cx+half+1].mean(axis=1)
        rows=np.where(counts>.70)[0]+lo
        assert len(rows),('outline missing',color,y)
        # Numerals above a short bar may also enter the window. Select the
        # contiguous dark stroke nearest the colored fill, not both strokes.
        runs=np.split(rows,np.where(np.diff(rows)>1)[0]+1)
        stroke=min(runs,key=lambda run:float(np.min(np.abs(run-y))))
        return float(np.median(stroke))
    top=line_near(y0);bottom=line_near(y1)
    bars.append({'color':color,'value':value,'color_bbox':[int(x0),int(y0),int(x1),int(y1)],'outline_top_y':top,'outline_bottom_y':bottom,'height':bottom-top})
unit=sum(x['height']/x['value'] for x in bars)/len(bars)
for x in bars:x['relative_ratio_error']=abs(x['height']/(unit*x['value'])-1)
result={'id':a.id,'revision':a.revision,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'method':'hue bounds constrained to visually identified columns when centers supplied; median of nearest contiguous navy outline stroke in central 40 percent of bar width; separate numeral strokes excluded; native unscaled pixels','column_centers':centers,'bars':bars,'height_ratio_tolerance':.05,'common_baseline_tolerance_px':5,'max_baseline_spread':max(x['outline_bottom_y'] for x in bars)-min(x['outline_bottom_y'] for x in bars),'height_ratio_pass':all(x['relative_ratio_error']<=.05 for x in bars),'visual_review_still_required':True}
result['common_baseline_pass']=result['max_baseline_spread']<=5
(ROOT/'denetim'/(a.id+'_'+a.revision+'_sayisal_olcum.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(result,ensure_ascii=False))
raise SystemExit(0 if result['height_ratio_pass'] and result['common_baseline_pass'] else 2)
