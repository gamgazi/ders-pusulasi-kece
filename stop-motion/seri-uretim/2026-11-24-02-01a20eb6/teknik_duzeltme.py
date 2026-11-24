"""User-authorized alpha-only cleanup and non-upscaled 3840x2160 placement.
Run only for an inspected one-piece opaque-paper object. Never for transparent glass
or an asset whose intentional paper openings have not been inspected.
"""
import argparse,hashlib,json,pathlib
import numpy as np
from PIL import Image
from scipy import ndimage

def main():
    p=argparse.ArgumentParser();p.add_argument('source');p.add_argument('target');p.add_argument('--baseline',type=int,default=1620);p.add_argument('--alpha-threshold',type=int,choices=[16,32,64,128,192],default=16);a=p.parse_args()
    source=pathlib.Path(a.source);target=pathlib.Path(a.target)
    if target.exists():raise SystemExit('Destination exists; refusing overwrite')
    im=Image.open(source).convert('RGBA');rgba=np.array(im);alpha=rgba[:,:,3].copy()
    labels,n=ndimage.label(alpha>=a.alpha_threshold,structure=np.ones((3,3)))
    areas=np.bincount(labels.ravel());areas[0]=0
    if not areas.max():raise SystemExit('No paper silhouette')
    mask=labels==areas.argmax()
    if any([mask[0].any(),mask[-1].any(),mask[:,0].any(),mask[:,-1].any()]):raise SystemExit('Visible paper touches source canvas edge; reject clipped source instead of padding it')
    interior=ndimage.binary_erosion(mask,structure=np.ones((3,3)))
    if ndimage.label(interior,structure=np.ones((3,3)))[1]!=1:raise SystemExit('Thin/disconnected silhouette needs individual alpha treatment')
    # RGB values never change. One-pixel partial-alpha perimeter, opaque paper interior.
    clean=np.zeros_like(alpha);clean[mask]=128;clean[interior]=255
    rgba[:,:,3]=clean
    yy,xx=np.where(mask);bbox=[int(xx.min()),int(yy.min()),int(xx.max()+1),int(yy.max()+1)]
    w,h=bbox[2]-bbox[0],bbox[3]-bbox[1]
    if w>3600 or h>2000:raise SystemExit('Native artwork does not fit with safe margins; no scaling performed')
    x=(3840-w)//2;y=a.baseline-h
    if y<64 or y+h>2096:raise SystemExit('Baseline produces insufficient canvas margin')
    canvas=Image.new('RGBA',(3840,2160),(0,0,0,0))
    crop=Image.fromarray(rgba,'RGBA').crop(tuple(bbox));canvas.paste(crop,(x,y))
    target.parent.mkdir(parents=True,exist_ok=True);canvas.save(target)
    report={'authorization':'User 2026-11-24: Yerel teknik düzeltmeyi uygula','source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'output_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'source_dimensions':list(im.size),'native_crop_dimensions':[w,h],'canvas_dimensions':[3840,2160],'native_4k':False,'upscaled':False,'rgb_of_retained_pixels_unchanged':True,'alpha_algorithm':'largest 8-connected alpha>=16 silhouette; preserve silhouette; opaque interior; one-pixel alpha128 perimeter; no RGB editing; native-size translation only','removed_low_alpha_or_island_pixels':int(((alpha>0)&~mask).sum()),'changed_alpha_pixels':int((alpha!=clean).sum()),'bbox_in_canvas':[x,y,x+w,y+h],'baseline':a.baseline}
    report['alpha_algorithm']=report['alpha_algorithm'].replace('alpha>=16','alpha>='+str(a.alpha_threshold))
    report['alpha_threshold']=a.alpha_threshold
    report['source_crop_bbox']=bbox
    target.with_suffix('.processing.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False))
if __name__=='__main__':main()
