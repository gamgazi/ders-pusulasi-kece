"""Read-only numeric check of a visually reviewed four-year graph. Never edits PNG."""
import argparse,json,pathlib,hashlib
import numpy as np
from PIL import Image
from scipy.ndimage import binary_closing,distance_transform_edt
p=argparse.ArgumentParser();p.add_argument('--png',required=True);p.add_argument('--x-centers',required=True);p.add_argument('--ticks-y',required=True);p.add_argument('--axis-x',required=True,type=int);p.add_argument('--output',required=True);a=p.parse_args()
f=pathlib.Path(a.png);im=np.array(Image.open(f).convert('RGBA'));r,g,b,alpha=[im[:,:,i].astype(float) for i in range(4)]
xs=list(map(float,a.x_centers.split(',')));ticks=list(map(float,a.ticks_y.split(',')));assert len(xs)==4 and len(ticks)==6
assert all(xs[i+1]>xs[i] for i in range(3)) and all(ticks[i+1]<ticks[i] for i in range(5))
# Tick order must be visually read as 0,1,2,3,4,5. Inputs are source-pixel coordinates.
approx_ticks=ticks.copy();navy=(alpha>240)&(r<75)&(g<75)&(b<160);ticks=[]
for y in approx_ticks:
    lo=max(0,int(y)-12);hi=min(im.shape[0],int(y)+13)
    rows=np.where(navy[lo:hi,a.axis_x-21:a.axis_x+22].mean(axis=1)>.70)[0]+lo
    assert len(rows),('No navy tick stroke near',y)
    runs=np.split(rows,np.where(np.diff(rows)>1)[0]+1)
    stroke=min(runs,key=lambda run:abs(float(np.median(run))-y))
    ticks.append(float(np.median(stroke)))
orange=(alpha>240)&(r>170)&(g>45)&(g<195)&(b<110)&(r>g*1.15)
orange[:max(0,int(ticks[-1])-35)]=False;orange[min(im.shape[0],int(ticks[0])+20):]=False
mask=binary_closing(orange,structure=np.ones((3,3)))
dist=distance_transform_edt(mask);dots=[]
unit=(ticks[0]-ticks[-1])/5;values=[3.2,3.4,4.1,4.8]
for i,cx in enumerate(xs):
    left=max(0,int(cx)-30);right=min(im.shape[1],int(cx)+31)
    region=dist[:,left:right];m=region.max();assert m>=4,('No substantial orange dot near x',cx,m)
    yy,xx=np.where(region>=m-.5);dy=float(np.median(yy));dx=float(np.median(xx)+left)
    observed=(ticks[0]-dy)/unit
    dots.append(dict(year=2023+i,expected_hours=values[i],x=dx,y=dy,observed_hours=observed,absolute_error_hours=abs(observed-values[i]),orange_radius_px=float(m)))
tick_error=max(abs(y-(ticks[0]-i*unit)) for i,y in enumerate(ticks))/unit
spacing=np.diff([d['x'] for d in dots]);spacing_error=float(max(abs(spacing/np.mean(spacing)-1)))
deltas=[dots[i+1]['observed_hours']-dots[i]['observed_hours'] for i in range(3)]
result=dict(source_png=f.name,source_sha256=hashlib.sha256(f.read_bytes()).hexdigest(),source_size=[im.shape[1],im.shape[0]],method='Visual approximate localization followed by median native-pixel navy tick strokes and orange-mask distance maxima; no image alteration',approximate_tick_inputs=approx_ticks,axis_x=a.axis_x,tick_coordinates_in_label_order_0_to_5=ticks,dots=dots,step_changes_hours=deltas,max_tick_error_hours=float(tick_error),max_x_spacing_relative_error=spacing_error,tolerances=dict(point_error_hours=.10,tick_error_hours=.06,x_spacing_relative_error=.05),visual_text_and_style_review_still_required=True)
result['numeric_pass']=all(d['absolute_error_hours']<=.10 for d in dots) and tick_error<=.06 and spacing_error<=.05 and all(d>0 for d in deltas) and abs(deltas[0]-.2)<=.10 and all(abs(d-.7)<=.10 for d in deltas[1:])
pathlib.Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
print(json.dumps(result,ensure_ascii=False));raise SystemExit(0 if result['numeric_pass'] else 2)
